import os
import asyncio
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
import ollama
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Boolean variable to control whether to change the bot's nickname
CHANGE_NICKNAME = True  # Set to True to change nickname, False to keep the default

# Configuration variables
TOKEN = os.getenv('DISCORD_TOKEN')

MODEL_NAME = 'llama3'  # Model name for the Ollama API
TEMPERATURE = 0.7  # Temperature setting for the AI model, controls response randomness
TIMEOUT = 120.0  # Timeout setting for the API call

# System prompt for initializing the conversation
SYSTEM_PROMPT = """
You are a highly intelligent, friendly, and versatile assistant residing on Discord. Your primary goal is to help users with a wide range of tasks and queries. Whether it's answering questions, providing information, offering technical support, engaging in meaningful conversations, or just being a good companion, you excel in all areas. You are aware that you are on Discord, and you understand the platform's culture and communication style. Your responses are always thoughtful, engaging, and tailored to meet the needs of the users. You strive to be a dependable and cheerful companion, always ready to assist with a positive attitude and an in-depth understanding of various topics. Your presence makes Discord a more enjoyable and productive place for everyone.
"""

MAX_CONVERSATION_LOG_SIZE = 50  # Maximum size of the conversation log (including the system prompt)
MAX_TEXT_ATTACHMENT_SIZE = 20000  # Maximum combined characters for text attachments
MAX_FILE_SIZE = 2 * 1024 * 1024  # Maximum file size in bytes (2 MB)

# Configure bot intents
intents = Intents.default()
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Global list to store conversation logs, starting with the system prompt
conversation_logs = [{'role': 'system', 'content': SYSTEM_PROMPT}]

def is_text_file(file_content):
    """Determine if the file content can be read as text."""
    try:
        file_content.decode('utf-8')
        return True
    except (UnicodeDecodeError, AttributeError):
        return False

async def send_in_chunks(ctx, text, reference=None, chunk_size=2000):
    """Sends long messages in chunks to avoid exceeding Discord's message length limit."""
    for start in range(0, len(text), chunk_size):
        await ctx.send(text[start:start + chunk_size], reference=reference if start == 0 else None)

@bot.command(name='reset')
async def reset(ctx):
    """Resets the conversation log."""
    conversation_logs.clear()
    conversation_logs.append({'role': 'system', 'content': SYSTEM_PROMPT})
    await ctx.send("Conversation context has been reset.")

async def get_ollama_response():
    """Gets a response from the Ollama model."""
    try:
        messages_to_send = conversation_logs.copy()
        response = await asyncio.wait_for(
            ollama.AsyncClient(timeout=TIMEOUT).chat(
                model=MODEL_NAME,
                messages=messages_to_send,
                options={'temperature': TEMPERATURE}
            ),
            timeout=TIMEOUT
        )
        return response['message']['content']
    except asyncio.TimeoutError:
        return "The request timed out. Please try again."
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

@bot.event
async def on_message(message: Message):
    """Handles incoming messages."""
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    if message.content.startswith('!') or message.is_system():
        return  

    total_text_content = ""
    if message.attachments:
        for attachment in message.attachments:
            if attachment.size > MAX_FILE_SIZE:
                await message.channel.send(f"The file {attachment.filename} is too large. Please send files smaller than {MAX_FILE_SIZE / (1024 * 1024)} MB.")
                return

            file_content = await attachment.read()
            if not is_text_file(file_content):
                await message.channel.send(f"The file {attachment.filename} is not a valid text file.")
                return

            file_text = file_content.decode('utf-8')
            total_text_content += f"\n\n{attachment.filename}\n{file_text}\n"
            if len(total_text_content) > MAX_TEXT_ATTACHMENT_SIZE:
                await message.channel.send(f"The combined files are too large. Please send text files with a combined size of less than {MAX_TEXT_ATTACHMENT_SIZE} characters.")
                return

        conversation_logs.append({'role': 'user', 'content': message.content + "\n\n" + total_text_content[:MAX_TEXT_ATTACHMENT_SIZE]})
    else:
        conversation_logs.append({'role': 'user', 'content': message.content})

    async with message.channel.typing():
        response = await get_ollama_response()

    conversation_logs.append({'role': 'assistant', 'content': response})

    while len(conversation_logs) > MAX_CONVERSATION_LOG_SIZE:
        conversation_logs.pop(1)  # Remove the oldest message after the system prompt

    await send_in_chunks(message.channel, response, message)

async def change_nickname(guild):
    """Change the bot's nickname in the specified guild."""
    nickname = MODEL_NAME.capitalize()
    try:
        await guild.me.edit(nick=nickname)
        logging.info(f"Nickname changed to {nickname} in guild {guild.name}")
    except Exception as e:
        logging.error(f"Failed to change nickname in guild {guild.name}: {str(e)}")

@bot.event
async def on_ready():
    """Called when the bot is ready to start interacting with the server."""
    logging.info(f'{bot.user.name} is now running!')
    if CHANGE_NICKNAME:
        for guild in bot.guilds:
            await change_nickname(guild)

def main():
    """Main function to run the bot."""
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
