import logging
import os
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


# Handle location messages
@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    # Define the URL for the request
    url = f"https://developers.onemap.sg/privateapi/commonsvc/revgeocode?location={message.location.latitude},{message.location.longitude}&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwMTYxLCJ1c2VyX2lkIjoxMDE2MSwiZW1haWwiOiJsaW15ZWVoYW5AZ21haWwuY29tIiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNjgwOTczNDQxLCJleHAiOjE2ODE0MDU0NDEsIm5iZiI6MTY4MDk3MzQ0MSwianRpIjoiMzdjNWZhNjM2M2M5NDZmZTI5ZGNlZjY1MDA2ZWFlZDAifQ.WaefQMWiWZKU9QJG1GJvGZ0Mo-l0aJZwOF4tI14Ren8"

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        return_string = []
        return_string.append("You are at:\n")

        for result in data["GeocodeInfo"]:
            return_string.append(
                f"{result['BLOCK']} {result['ROAD']} {result['BUILDINGNAME']}, S({result['POSTALCODE']})\n")
    else:
        print(f"Error: {response.status_code}")

    result = "".join(return_string)

    bot.reply_to(
        message, "".join(result)
    )


bot.polling()
