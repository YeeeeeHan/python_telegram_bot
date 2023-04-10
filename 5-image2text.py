import logging
import os
from io import BytesIO
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


# Handle voice messages
@bot.message_handler(content_types=['photo'])
def handle_voice_message(message):
    bot.send_message(message.chat.id, "Coverting image to text...")

    # Get the Telegram file URL
    file_info = bot.get_file_url(message.photo[-1].file_id)

    # Download the image from the Telegram file URL
    response = requests.get(file_info)

    # Save the image content to a file-like object (BytesIO)
    image_file_descriptor = BytesIO(response.content)

    api_url = 'https://api.api-ninjas.com/v1/imagetotext'
    files = {'image': image_file_descriptor}
    headers = {
        "X-Api-Key": "NGCmhJQbwwnWMaxXjlr0Kw==jc52IjuLeM9bAg9p",
    }

    r = requests.post(api_url, files=files, headers=headers)

    sentence = []
    for result in r.json():
        sentence.append(result['text'])

    bot.send_message(message.chat.id, " ".join(sentence))


bot.polling()
