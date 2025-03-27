import discord
import requests
import os
from dotenv import load_dotenv


# Load API keys from .env
load_dotenv()
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.environ.get("AI_API")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def text_to_emoji(text):
    """Converts text into emojis using OpenRouter AI."""
    payload = {
        "model": "openai/gpt-4o",
        "messages": [{"role": "user", "content": f"Translate this into emojis: {text}"}]
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "❌ Error: Couldn't process request"

def aiconvert(text):
    """Converts text into emojis using OpenRouter AI."""
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": f": {text}"}]
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "❌ Error: Couldn't process request"


def insultai(text):
    """Converts text into emojis using OpenRouter AI."""
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": f" Make up a creative funny insult about the following thing, make only 1 insult, being offensive is okay: {text}"}]
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "❌ Error: Couldn't process request"    

# Discord Bot Setup
intents = discord.Intents.default()
intents.messages = True  # Allows bot to read messages
intents.message_content = True  # Required to read message content

class EmojiBot(discord.Client):
    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:  # Ignore bot's own messages
            return

        if message.content.startswith("!emoji"):
            text = message.content.replace("!emoji ", "", 1)
            emoji_translation = text_to_emoji(text)
            await message.channel.send(f"🎨 **Emoji Translation:** {emoji_translation}")

        if message.content.startswith("!whoisgay"):
            await message.channel.send("Luke Thistlewaite is a gay boy, he likes dick")

        if message.content.startswith("!ai"):
                    text = message.content.replace("!ai ", "", 1)
                    ai_text = aiconvert(text)
                    await message.channel.send("AI: " + ai_text)

        if message.content.startswith("!insult"):
                    text = message.content.replace("!insult ", "", 1)
                    insult_text = insultai(text)
                    await message.channel.send("Insult: " + insult_text)            




# Run the bot
bot = EmojiBot(intents=intents)
bot.run(DISCORD_BOT_TOKEN)

