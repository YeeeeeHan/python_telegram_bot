import logging
import os
import time
from pprint import pprint

import requests
import telebot
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the bot token from .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Enable TeleBot logging
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


# Why is this function necessary?
def send_long_message(bot, chat_id, text, max_length=4096):
    if len(text) <= max_length:
        bot.send_message(chat_id, text)
    else:
        parts = []
        while len(text) > 0:
            if len(text) > max_length:
                part = text[:max_length]
                last_space = part.rfind(' ')

                if last_space != -1:
                    part = part[:last_space]

                parts.append(part)
                text = text[len(part):]
            else:
                parts.append(text)
                break

        for part in parts:
            bot.send_message(chat_id, part)


# Handle voice messages
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # Where is the best place to put this?
    bot.send_message(message.chat.id, "Transcribing...")

    # How do we know there's such a function?
    file_info = bot.get_file_url(message.voice.file_id)

    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": file_info
    }
    headers = {
        "authorization": "f0d2f3df22fc499e90085f96f902b3cd",
    }
    response = requests.post(endpoint, json=json, headers=headers)

    status = ""
    text = ""
    endpoint = f"https://api.assemblyai.com/v2/transcript/{response.json()['id']}"
    headers = {
        "authorization": "f0d2f3df22fc499e90085f96f902b3cd",
    }
    # Polling vs Push
    while status != "completed":
        response = requests.get(endpoint, headers=headers)
        status = response.json()['status']
        text = response.json()['text']
        # wait 2 seconds
        time.sleep(2)

    send_long_message(bot, message.chat.id, text)


bot.polling()
