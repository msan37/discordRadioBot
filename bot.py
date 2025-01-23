# Prerequisites
import discord
from discord.ext import commands
import json
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="radio!", intents=intents)

# --------------------
# Variable Setup
# --------------------
# Define OVERWRITE_STATIONS variable from environment variable.
OVERWRITE_STATIONS = os.getenv("OVERWRITE_STATIONS")
# Define Bot Token from environment variable.
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Define a default volume.
DEFAULT_VOLUME = float(os.getenv("DEFAULT_VOLUME", 1.0))
# Define a default volume offset.
DEFAULT_VOLUME_OFFSET = float(os.getenv("DEFAULT_VOLUME_OFFSET", 1.0))
# Define a settings file to keep track of variables.
settings_file = "settings.json"

# Handle missing environment variables that are required.
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# --------------------
# Define some Functions
# --------------------
async def start_radio(ctx, useDefaultVolume, station_name=None):
    # Handle if user isn't in a voice channel.  
    if not ctx.author.voice:
        await ctx.send("I can only join a voice channel if you're already in one. Please join a voice channel then try again.")
        return

    # If we are already in a voice channel, disconnect.
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    # Join the command issuer's channel.
    channel = ctx.author.voice.channel
    vc = await channel.connect()

    # Calculate the corrected volume based on the default and the offset.
    # If we want to start the radio with the default volume...
    if useDefaultVolume == True:
        # Readjust the current volume to match the default.
        settings["current_volume"] = settings["default_volume"]
        save_settings(settings)
        # Set the actual volume to be the default adjusted by the offset.
        actual_volume = settings["default_volume"] * settings["volume_offset"]
    else:
        # If we don't want the default, just readjust the current volume against the offset.
        actual_volume = settings["current_volume"] * settings["volume_offset"]
    
    # If a station name was provided...
    if station_name:
        # And that name can be found in the "stations" list...
        if station_name in settings["stations"]:
            # Set the stream_url to match the station's URL.
            stream_url = settings["stations"][station_name]
            # Update the last_station to match.
            settings["last_station"] = station_name
            # Save our change to last_station.
            save_settings(settings)
        # If the name can't be found, let the user know.
        else:
            await ctx.send(f"Sorry, I've never heard of `{station_name}`.")
            break
    # If no station name was provided...
    else:
        # And the last_station exists and can be found in the "stations" list
        if settings["last_station"] and settings["last_station"] in settings["stations"]:
            # Then set the stream_url to the URL of the last_station.
            stream_url = settings["stations"][settings["last_station"]]
        # And last_station can't be found...
        else:
            # Let the user know. This might be indicative of no stations being set yet.
            await ctx.send("Uh oh. You didn't specify a station and I can't recall the last station I played. This normally shouldn't happen, but just try specifying a station for me to play.")
            break

    # Start streaming the radio. Log if the remote stream ends (normally shouldn't happen).
    vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(stream_url), volume=actual_volume), after=lambda e: print(f"Stream ended: {e}"))
    await ctx.send(f"Now playing the radio in {channel.name}!")
    print(f"Now playing the radio in {channel.name}.")

# Load the settings JSON file and return its parsed contents.
def load_settings():
    # Check that settings file exists.
    if os.path.exists(settings_file):
        # Open the settings file in read mode and assign to f variable.
        with open(settings_file, "r") as f:
            # Parse the JSON within the file and return it.
            return json.load(f)
    else:
        settings = {
            "stations": {},
            "last_station": None,
            "volume_offset": DEFAULT_VOLUME,
            "default_volume": DEFAULT_VOLUME_OFFSET,
            "current_volume": 1.0
        }

    # Check if OVERWRITE_STATIONS is set.
    if OVERWRITE_STATIONS:
        # If it is, put it in the stations variable.
        try:
            stations = json.loads(OVERWRITE_STATIONS)
            # If this new variable contains a stations list like we expect...
            if isinstance(stations, dict):
                # Overwrite "stations" in settings with the new values.
                settings["stations"] = stations
                # Set last_station to the first station.
                settings["last_station"] = list(stations.keys())[0]
            # Otherwise, give an error.
            else:
                raise ValueError("OVERWRITE_STATIONS isn't in the correct format! Check the documentation.")
        # If json.loads couldn't parse OVERWRITE_STATIONS, give an error.
        except:
            raise ValueError("OVERWRITE_STATIONS couldn't be parsed as JSON! Please make sure it is formatted correctly. Check the documentation.")
    if not settings.get("stations"):
        raise ValueError("No stations have been configured. Try using the OVERWRITE_STATIONS environment variable or manually editing settings.json file. Check the documentation.")
    
    # Return our finished settings JSON.
    return settings

# Save the current settings to the settings JSON file.
def save_settings(settings):
    # Open the settings file in write mode and assign to f variable.
    with open(settings_file, "w") as f:
        # Dump the current settings as JSON into the settings file.
        json.dump(settings, f, indent=4)

# Initialize the settings.
settings = load_settings()

# --------------------
# Define Bot Behavior
# --------------------
# Log when we connect to Discord.
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Define a join command.
@bot.command()
async def join(ctx):
    """Joins the voice channel you're in."""
    await start_radio(ctx, True)

# Define a generic switch command
@bot.command(aliases=['play','station'])
async def switch(ctx, station_name: str = None):
    """Switch to the specified radio station."""
    await start_radio(ctx, True, station_name)

# --------------------
# Volume Shenanigans
# --------------------
# Define a volume command.
@bot.command()
async def volume(ctx, volume: int):
    """Adjust the radio volume between 1 and 100."""
    # Handle if bot isn't in a voice channel.
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel!")
        return

    # Check if requested volume is valid.
    if 1 <= volume <= 100:
        # If we are currently playing audio...
        if ctx.voice_client.is_playing():
            # Set the new volume into the settings JSON.
            settings["current_volume"] = volume / 100
            # Call the save settings function to persist the new setting.
            save_settings(settings)
            # Actually change the current output volume.
            ctx.voice_client.source.volume = (volume / 100) * settings["volume_offset"]
            await ctx.send(f"Volume set to {volume}%.")
            print(f"Volume changed to: {ctx.voice_client.source.volume}")  # Debugging line
        else:
            await ctx.send("Hmm...I don't think I'm playing any audio right now, so I can't change the volume.")
    else:
        await ctx.send("The requested volume must be a number between 1 and 100.")

# Define a volume offset command.
@bot.command()
async def volumeoffset(ctx, offset: int):
    """Set an offset percentage for the volume."""
    # Check if requested volume offset is valid.
    if 1 <= offset <= 100:
        # Set the new volume offset into the settings JSON.
        settings["volume_offset"] = offset / 100
        # Call the save settings function to persist the new setting.
        save_settings(settings)
        # If we are streaming audio...
        if ctx.voice_client:
            # Restart the stream without using the default volume.
            await start_radio(ctx, False)
            await ctx.send(f"The volume offset is now {offset}%. Restarted the radio to apply the change.")
            print(f"Volume offset changed to: {settings['volume_offset']}%. Restarted stream to apply change.")
        else:
            await ctx.send(f"The volume offset is now {offset}%.")
            print(f"Volume offset changed to {settings['volume_offset']}%.")
    else:
        await ctx.send("The volume offset must be a number between 1 and 100.")

# Define a default volume command.
@bot.command()
async def defaultvolume(ctx, volume: int):
    """Set a default volume to use when starting the radio."""
    # Check if requested default volume is valid.
    if 1 <= volume <= 100:
        # Set the new default volume into the settings JSON.
        settings["default_volume"] = volume / 100
        # Call the save settings function to persist the new setting.
        save_settings(settings)
        await ctx.send(f"The default volume is now {volume}%.")
        print(f"Set the default volume to {settings['default_volume']}.")
    else:
        await ctx.send("The default volume must be a number between 1 and 100.")

# Define a pause command.
@bot.command(aliases=['mute'])
async def pause(ctx):
    """Pauses the radio stream."""
    # Handle if bot isn't in a voice channel.
    if not ctx.voice_client:
        await ctx.send("Hey, I'm not in a voice channel!")
        return

    # Check that the radio is unpaused.
    if not ctx.voice_client.is_paused():
        # Pause the audio.
        ctx.voice_client.pause()
        await ctx.send("The radio is now pasued.")
        print("Radio paused")  # Debugging line
    else:
        await ctx.send("The radio is already paused. If you're still hearing audio, cry.")

# Define an unpause command.
@bot.command(aliases=['unmute'])
async def unpause(ctx):
    """Unpauses the radio stream."""
    # Handle if bot isn't in a voice channel.
    if not ctx.voice_client:
        await ctx.send("Hey, I'm not in a voice channel!")
        return

    # Check that the radio was already paused.
    if ctx.voice_client.is_paused():
        # Resume audio playback if the bot was paused.
        ctx.voice_client.resume()
        await ctx.send("The radio is now unpaused. Enjoy the music!.")
        print("Bot resumed")  # Debugging line
    else:
        await ctx.send("The radio is already unpaused. If you can't hear anything, try changing the volume or making me rejoin.")

# Define a leave command.
@bot.command()
async def leave(ctx):
    """Leaves the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Okay, I've left the voice channel. See you later!")
    else:
        await ctx.send("Hey, I'm not in a voice channel!")

# Automatically leave if everyone else leaves a voice channel.
@bot.event
async def on_voice_state_update(member, before, after):
    """Auto disconnect if no one is left in the channel."""
    # Stop if a bot triggered the event.
    if member.bot:
        return
    # Find an instance of ourself where we are connected to the voice channel where this event occured.
    bot_client_info = discord.utils.get(bot.voice_clients, guild=member.guild)
    # If we are in a voice channel and that channel matches the one that was left by the event-triggering user...
    if bot_client_info and before.channel == bot_client_info.channel:
        #...and we are the last one in the voice channel...
        if len(bot_client_info.channel.members) == 1:
            # ...then leave.
            await bot_client_info.disconnect()

# Run the bot!
bot.run(BOT_TOKEN)
