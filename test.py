import discord
import os
from dotenv import load_dotenv # type: ignore (default in python library ;)

load_dotenv()  # Test .env
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Test the token

intents = discord.Intents.default()  # Use default intents to avoid unassigned intent issues
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(BOT_TOKEN)
