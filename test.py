import discord
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()  # Loads settings from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Ensure your .env uses the correct key

intents = discord.Intents.default()  # Use default intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(BOT_TOKEN)
