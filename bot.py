# Prerequisites
import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
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
