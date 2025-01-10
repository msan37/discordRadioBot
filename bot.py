# Prerequisites
import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="radio!", intents=intents)

# Define radio stream URL from environment variable.
STREAM_URL = os.getenv("STREAM_URL")
# Define Bot Token from environment variable.
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Handle missing environment variables.
if not STREAM_URL:
    raise ValueError("STREAM_URL environment variable is not set!")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Log when we connect to Discord.
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Define a join command.
@bot.command()
async def join(ctx):
    """Joins the voice channel you're in."""
    # Handle if user isn't in a voice channel.  
    if not ctx.author.voice:
        await ctx.send("I can only join a voice channel if you're already in one. Please join a voice channel then try again.")
        return

    # Join the issuer's channel.
    channel = ctx.author.voice.channel
    vc = await channel.connect()

    # Start streaming the radio. Log if the remote stream ends (normally shouldn't happen).
    vc.play(discord.FFmpegPCMAudio(STREAM_URL), after=lambda e: print(f"Stream ended: {e}"))
    await ctx.send(f"Now playing the radio in {channel.name}!")

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
        # Convert from 0 - 100 to 0 - 2 and set volume.
        new_volume = volume / 50
        if ctx.voice_client.is_playing():
            ctx.voice_client.source.volume = new_volume
            await ctx.send(f"Volume set to {volume}%.")
            print(f"Volume changed to: {ctx.voice_client.source.volume}")  # Debugging line
        else:
            await ctx.send("Hmm...something is not right. I don't think I'm playing any audio right now, so I can't change the volume.")
    else:
        await ctx.send("The requested volume must be a number between 1 and 100.")

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
