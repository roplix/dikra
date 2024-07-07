import discord
import asyncio
import random
import os
from flask import Flask
from keep_alive import keep_alive
from settings import (
    is_prize_value_above_threshold,
    is_pool_value_above_threshold,
    is_pool_value_above_threshold_1,
    is_enters_value_at_most_4,
    is_pool_per_enters_above_threshold,
    extract_text_between_parentheses,
    is_pool_per_enters_worth_risk,
    is_prize_value_above_threshold1
)

emoji_options = ['❤', '💙', '🚀', '🔥']

responses = [
    "thx",
    "ty",
    "thanks",
    "thank you",
    "tysm",
    "thankss",
    "thnks",
    "tq",
    "tnx",
    "thank u",
    "thx a lot",
    "thx so much",
    "many thanks",
    "cheers",
    "thnx"
]

keep_alive()

# Flask setup
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Discord client setup
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

client = MyClient()

# Function to check previous messages
async def check_previous_messages(channel, new_message):
    async for message in channel.history(limit=100):
        if message.content == new_message:
            return True
    return False

# Function to get a unique response
async def get_unique_response(channel):
    unique_response = random.choice(responses)
    while await check_previous_messages(channel, unique_response):
        unique_response = random.choice(responses)
    return unique_response

# Event: Message received
@client.event
async def on_message(message):
    if message.author.id == 1150448986264698980 and message.guild.id != 1102183639791452242:
        print("Message from bot.")

        # Processing raffle ended messages
        for embed in message.embeds:
            if client.user.mentioned_in(message) and embed and embed.description and "Raffle ended" in embed.description:
                response = await get_unique_response(message.channel)
                extracted_text = extract_text_between_parentheses(embed.description)

                if extracted_text:
                    print(f"Extracted text: {extracted_text}")

                await asyncio.sleep(random.randint(2, 4))
                async with message.channel.typing():
                    await asyncio.sleep(random.randint(2, 4))
                    await message.channel.send(response)

                try:
                    random_emoji = random.choice(emoji_options)
                    await asyncio.sleep(random.randint(5, 8))
                    await message.add_reaction(random_emoji)
                except Exception as e:
                    print(f"Failed to add reaction: {e}")

                # Example of sending to another channel
                channel_id = 1252625826109722664
                channel = client.get_channel(channel_id)

                if channel and extracted_text:
                    await asyncio.sleep(random.randint(2, 5))
                    await channel.send(f"<@740547277164249089> hmdlh rb7t {extracted_text}")

        # Example of handling different conditions for entering raffles or airdrops
        for embed in message.embeds:
            if embed and embed.description and "Raffle created" in embed.description:
                if is_prize_value_above_threshold(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await child.click()
                elif is_prize_value_above_threshold1(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await asyncio.sleep(random.randint(3, 6))
                                await child.click()
                else:
                    print("Conditions not met for any action, skipping")

# Run the client
if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
