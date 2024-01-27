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

chat_id = -1002118351015

last_check = {
    "yt_eeth_apy": 0,
    "yt_rseth_apy": 0
}

PROFILE_MESSAGE = """*_YT eETH_*
APY: {apy_eeth}% \({diff_apy_eeth}% {up_or_down_eeth}\)

*_YT rsETH_*
APY: {apy_rseth}% \({diff_apy_rseth}% {up_or_down_rseth}\)
"""

# Pretty print a telebot message


def pretty_print_telebot_message(message: telebot.types.Message):
    message_data = {
        'message_id': message.message_id,
        'text': message.text,
        'from_user': {
            'id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'username': message.from_user.username,
        },
        'date': message.date,
        'chat': {
            'id': message.chat.id,
            'type': message.chat.type,
            'title': message.chat.title,
            'username': message.chat.username,
        },
    }

    pprint(message_data)


# Find and replace all '.' with '\.'
def formatDecimals(number):
    return str(number).replace('.', '\.').replace('-', '\-')


def formatMessage(yt_eeth_apy, yt_rseth_apy):
    return PROFILE_MESSAGE.format(
        apy_eeth=formatDecimals(yt_eeth_apy),
        diff_apy_eeth=formatDecimals(calculateDifference(
            yt_eeth_apy, last_check["yt_eeth_apy"])),
        up_or_down_eeth=render_up_or_down(calculateDifference(
            yt_eeth_apy, last_check["yt_eeth_apy"])),
        apy_rseth=formatDecimals(yt_rseth_apy),
        diff_apy_rseth=formatDecimals(calculateDifference(
            yt_rseth_apy, last_check["yt_rseth_apy"])),
        up_or_down_rseth=render_up_or_down(calculateDifference(
            yt_rseth_apy, last_check["yt_rseth_apy"]))

    )


def calculateDifference(new_apy, old_apy):
    difference = new_apy - old_apy
    return round(difference, 3)


def render_up_or_down(value):
    if value > 0:
        return "📈"
    elif value < 0:
        return "📉"
    else:
        return "🔷"


def get_data():
    # Replace with your API endpoint
    url_YTrseth = 'https://api-v2.pendle.finance/core/v1/1/markets/0x4f43c77872db6ba177c270986cd30c3381af37ee'
    url_YTeeth = 'https://api-v2.pendle.finance/core/v1/1/markets/0xf32e58f92e60f4b0a37a69b95d642a471365eae8'
    try:
        # get YT rsEth APY
        response_YTrseth = requests.get(url_YTrseth)
        response_YTrseth.raise_for_status()
        data_YTrseth = response_YTrseth.json()
        yt_rseth_apy = round(data_YTrseth['impliedApy'] * 100, 3)

        # get YT eETH APY
        response_YTeeth = requests.get(url_YTeeth)
        response_YTeeth.raise_for_status()
        data_YTeeth = response_YTeeth.json()
        yt_eeth_apy = round(data_YTeeth['impliedApy'] * 100, 3)

        return yt_eeth_apy, yt_rseth_apy
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")


def price_alert():
    data_YTeeth, data_YTrseth = get_data()


    message = formatMessage(data_YTeeth, data_YTrseth)
    # bot.send_message(
    #     chat_id,
    #     "Yeeeee Haaawwwnn",
    #     parse_mode='MarkdownV2')
    
    if data_YTeeth < 0.285 or data_YTrseth < 0.285:
        bot.send_message(
            chat_id,
            message,
            parse_mode='MarkdownV2')

        if data_YTeeth < 0.285:
            bot.send_message(
                chat_id,
                "YT eETH IS LESS THAN 0.285% APY. WE GOT FUCKED BY HEEHAWN. SELL SELL SELL.",
                parse_mode='MarkdownV2')

        if data_YTrseth < 0.285:
            bot.send_message(
                chat_id,
                "YT rsETH IS LESS THAN 0.285% APY. WE GOT FUCKED BY HEEHAWN. SELL SELL SELL.",
                parse_mode='MarkdownV2')


# Handle /check command
@bot.message_handler(commands=['check'])
def price_check(message):
    data_YTeeth, data_YTrseth = get_data()

    message = formatMessage(data_YTeeth, data_YTrseth)
    last_check["yt_eeth_apy"] = data_YTeeth
    last_check["yt_rseth_apy"] = data_YTrseth
    print(message)

    bot.send_message(
        chat_id,
        message,
        parse_mode='MarkdownV2')


# Handle all uncaught messages
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    pretty_print_telebot_message(message)
    print(
        f"[ChatID: {message.chat.id}]Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")


# Schedule the message
price_alert()
schedule.every().minute.do(price_alert)


# Create a separate thread for the schedule loop
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the schedule checker thread
schedule_thread = threading.Thread(target=schedule_checker)
schedule_thread.start()


bot.polling()
