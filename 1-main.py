import logging
import os
import threading
import time
from pprint import pprint

import requests
import schedule
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


# Handle all uncaught messages
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    # pretty_print_telebot_message(message)
    print(
        f"[ChatID: {message.chat.id}]Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")


def fetch_and_send_api_data():
    chat_id = -4186339791
    # Replace with your API endpoint
    url_YTrseth = 'https://api-v2.pendle.finance/core/v1/1/markets/0x4f43c77872db6ba177c270986cd30c3381af37ee'
    url_YTeeth = 'https://api-v2.pendle.finance/core/v1/1/markets/0xf32e58f92e60f4b0a37a69b95d642a471365eae8'
    try:
        response_YTrseth = requests.get(url_YTrseth)
        response_YTrseth.raise_for_status()
        data_YTrseth = response_YTrseth.json()

        response_YTeeth = requests.get(url_YTeeth)
        response_YTeeth.raise_for_status()
        data_YTeeth = response_YTeeth.json()

        if data_YTeeth['impliedApy'] < 0.285:
            bot.send_message(
                chat_id,
                f"**{data_YTeeth['yt']['proName']}**\n" +
                f"APY: {round(data_YTeeth['impliedApy']* 100, 3)}%\n",
                parse_mode='Markdown')
        if data_YTrseth['impliedApy'] < 0.285:
            bot.send_message(
                chat_id,
                f"**{data_YTrseth['yt']['proName']}**\n" +
                f"APY: {round(data_YTrseth['impliedApy']* 100, 3)}%\n",
                parse_mode='Markdown')

    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")


# Schedule the message
fetch_and_send_api_data()
schedule.every().hour.do(fetch_and_send_api_data)


# Create a separate thread for the schedule loop
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the schedule checker thread
schedule_thread = threading.Thread(target=schedule_checker)
schedule_thread.start()


bot.polling()
