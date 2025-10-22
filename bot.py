# bot_env.py
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Logged in as {self.user} (id: {self.user.id})")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.lower() == "!ping":
            await message.channel.send("Pong!")

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
            
client = MyClient(intents=intents)
client.run(TOKEN)
