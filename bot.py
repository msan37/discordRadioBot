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
# Define radio stream URL from environment variable.
STREAM_URL = os.getenv("STREAM_URL")
# Define Bot Token from environment variable.
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Define a default volume.
DEFAULT_VOLUME = os.getenv("DEFAULT_VOLUME", 1.0)
# Define a default volume offset.
DEFAULT_VOLUME_OFFSET = os.getenv("DEFAULT_VOLUME_OFFSET", 1.0)
# Define a settings file to keep track of variables.
SETTINGS_FILE = "settings.json"


# Handle missing environment variables that are required.
if not STREAM_URL:
    raise ValueError("STREAM_URL environment variable is not set!")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# --------------------
# Define some Functions
# --------------------
def start_radio(useDefaultVolume):
    # Handle if user isn't in a voice channel.  
    if not ctx.author.voice:
        await ctx.send("I can only join a voice channel if you're already in one. Please join a voice channel then try again.")
        return

    # Join the command issuer's channel.
    channel = ctx.author.voice.channel
    vc = await channel.connect()

    # Calculate the corrected volume based on the default and the offset.
    if useDefaultVolume == true:
        actual_volume = settings["default_volume"] * settings["volume_offset"]
    else:
        actual_volume = settings["current_volume"] * settings["volume_offset"]
    
    # Start streaming the radio. Log if the remote stream ends (normally shouldn't happen).
    vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(STREAM_URL), volume=actual_volume), after=lambda e: print(f"Stream ended: {e}"))
    await ctx.send(f"Now playing the radio in {channel.name}!")
    print(f"Now playing the radio in {channel.name}.")

# Load the settings JSON file and return its parsed contents.
def load_settings():
    # Check that settings file exists.
    if os.path.exists(SETTINGS_FILE):
        # Open the settings file in read mode and assign to f variable.
        with open(SETTINGS_FILE, "r") as f:
            # Parse the JSON within the file and return it.
            return json.load(f)
    # If it doesn't exist, return some default settings.
    return {"volume_offset": DEFAULT_VOLUME, "default_volume": DEFAULT_VOLUME_OFFSET, "current_volume": 1.0}

# Save the current settings to the settings JSON file.
def save_settings(settings):
    # Open the settings file in write mode and assign to f variable.
    with open(SETTINGS_FILE, "w") as f:
        # Dump the current settings as JSON into the settings file.
        json.dump(settings, f)

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
    start_radio(true)

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
            ctx.voice_client.source.volume = volume / 100
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
            start_radio(false)
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
        print(f"Set the default volume to {settings["default_volume"]}.")
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
    if member == bot.user and after.channel is None and before.channel is not None:
        if before.channel.guild.voice_client:
            await before.channel.guild.voice_client.disconnect()

# Run the bot!
bot.run(BOT_TOKEN)
