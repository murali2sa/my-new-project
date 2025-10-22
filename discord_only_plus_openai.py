import os
import asyncio
from dotenv import load_dotenv
import discord
import openai
from asyncio import Semaphore

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Set DISCORD_TOKEN and OPENAI_API_KEY in .env")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True  # required to read message content

# Limit concurrent OpenAI calls to avoid bursts
OPENAI_CONCURRENCY = 3
openai_sem = Semaphore(OPENAI_CONCURRENCY)

# Optional: prefix trigger
TRIGGER_PREFIX = "!pirate"

# System prompt ensures pirate-style responses
SYSTEM_PROMPT = (
    "You are a spirited pirate of the high seas. Reply in a colorful, pirate-y voice: "
    "use plenty of nautical imagery, old-fashioned pirate words (arr, matey, ye, scallywag), "
    "short wisecracks, and occasionally insult-playfully when appropriate. Keep responses "
    "friendly and safe. Don't reveal anything about being an AI. Keep responses to a reasonable length (<= 250 words)."
)

class PirateBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.bg_tasks = set()

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} (id: {self.user.id})")

    async def on_message(self, message: discord.Message):
        # ignore messages from bots (including self)
        if message.author.bot:
            return

        content = message.content.strip()

        # Trigger: message starts with "!pirate" OR bot is mentioned
        invoked = False
        user_prompt = ""
        if content.lower().startswith(TRIGGER_PREFIX):
            invoked = True
            user_prompt = content[len(TRIGGER_PREFIX):].strip() or "Say something pirate-y!"
        elif self.user in message.mentions:
