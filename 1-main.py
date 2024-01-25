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


# Define all available content types
all_content_types = [
    'text', 'audio', 'document', 'photo', 'sticker', 'video',
    'video_note', 'voice', 'location', 'contact', 'new_chat_members',
    'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo',
    'group_chat_created', 'supergroup_chat_created', 'channel_chat_created',
    'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message',
    'invoice', 'successful_payment', 'connected_website', 'passport_data'
]


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


def pretty_print_telebot_callback_query(call: telebot.types.CallbackQuery):
    call_data = {
        'data': call.data,
        'from_user': {
            'id': call.from_user.id,
            'first_name': call.from_user.first_name,
            'last_name': call.from_user.last_name,
            'username': call.from_user.username,
        },
        'id': call.id,
        'message': {
            'chat': {
                'id': call.message.chat.id,
                'type': call.message.chat.type,
                'title': call.message.chat.title,
                'username': call.message.chat.username,
            },
            'date': call.message.date,
            'from_user': {
                'id': call.message.from_user.id,
                'first_name': call.message.from_user.first_name,
                'last_name': call.message.from_user.last_name,
                'username': call.message.from_user.username,
            },
            'message_id': call.message.message_id,
            'text': call.message.text,
        },
    }

    pprint(call_data)


# Handle /send command
@bot.message_handler(commands=['send'])
def handle_hello(message):
    print(
        f"Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")
    bot.send_message(
        message.chat.id, f"Howdy, how are you doing, message_id:{message.message_id}")


# Handle /reply command
@bot.message_handler(commands=['reply'])
def handle_start(message):
    print(
        f"Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")
    bot.reply_to(message, "Replying to your message")


# Handle /delete command
@bot.message_handler(commands=['delete'])
def handle_delete(message):
    print(
        f"Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")
    bot.reply_to(message, "Deleting message...")
    bot.delete_message(message.chat.id, message.message_id)


# Handle /delete command
@bot.message_handler(commands=['edit'])
def handle_edit(message):
    print(
        f"Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")
    print(f"Is replying to: {message.reply_to_message.message_id}")
    bot.edit_message_text("edited", message.chat.id,
                          message.reply_to_message.message_id)


# Handle voice messages
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    print(
        f"Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")
    bot.send_message(message.chat.id, "Lovely voice message!")


# Handle photo messages
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    print(message)
    print(
        f"Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")
    bot.send_message(message.chat.id, "Lovely photo!")


# Handle location messages
@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, f"Received your location: {message.location.latitude}, {message.location.longitude}")


# Handle contact messages
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, f"Received your contact: {message.contact.first_name} {message.contact.last_name}, {message.contact.phone_number}")


# Start a poll
@bot.message_handler(commands=['poll'])
def handle_poll(message):
    print(
        f"Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")
    question = "What's your favorite programming language?"
    options = ["Python", "JavaScript", "Java"]
    bot.send_poll(message.chat.id, question, options)


# Start an option quiz
@bot.message_handler(commands=['inlinekeyboard_options'])
def send_options(message):
    chat_id = message.chat.id
    text = "Choose an option:"

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button1 = telebot.types.InlineKeyboardButton(
        "Option 1", callback_data="options_1")
    button2 = telebot.types.InlineKeyboardButton(
        "Option 2", callback_data="options_2")
    button3 = telebot.types.InlineKeyboardButton(
        "Option 3", callback_data="options_3")

    markup.add(button1, button2)
    markup.add(button3)

    bot.send_message(chat_id, text, reply_markup=markup)


# Handle all callback queries starting with "options_"
@bot.callback_query_handler(func=lambda call: call.data.startswith("options_"))
def handle_callback_query(call):
    # pretty_print_telebot_callback_query(call)
    response_text = ""
    if call.data == "options_1":
        response_text = "You chose Option 1!"
    elif call.data == "options_2":
        response_text = "You chose Option 2!"
    elif call.data == "options_3":
        response_text = "You chose Option 3!"
    else:
        response_text = "You chose something else!"
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, response_text)
    bot.answer_callback_query(call.id, response_text)


# Start an option quiz
@bot.message_handler(commands=['inlinekeyboard_quiz'])
def send_options(message):
    chat_id = message.chat.id
    text = "What is 1 + 1:"

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button1 = telebot.types.InlineKeyboardButton(
        "1", callback_data="quiz_1")
    button2 = telebot.types.InlineKeyboardButton(
        "2", callback_data="quiz_2")

    markup.add(button1, button2)

    bot.send_message(chat_id, text, reply_markup=markup)


# Handle all callback queries starting with "quiz_"
@bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_"))
def handle_callback_query(call):
    # pretty_print_telebot_callback_query(call)
    response_text = ""
    if call.data == "quiz_1":
        response_text = "Wrong!"
    elif call.data == "quiz_2":
        response_text = "Right!"
    else:
        response_text = "You chose something else!"
    bot.send_message(call.message.chat.id, response_text)
    bot.answer_callback_query(call.id, response_text)


# Handle /start command
@bot.message_handler(commands=['keyboard'])
def send_keyboard(message):
    chat_id = message.chat.id
    text = "Please share your location or contact information."

    markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=3)
    text_button = telebot.types.KeyboardButton("Say Hello")
    location_button = telebot.types.KeyboardButton(
        "Share Location", request_location=True)
    contact_button = telebot.types.KeyboardButton(
        "Share Contact", request_contact=True)

    markup.add(location_button, contact_button)
    markup.add(text_button)
    bot.send_message(chat_id, text, reply_markup=markup)


# Handle forwarded messages
@bot.message_handler(func=lambda message: message.forward_from is not None)
def handle_forwarded_message(message):
    print("This message was forwarded.")
    bot.send_message(message.chat.id, "You've forwarded a message.")


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

        bot.send_message(
            chat_id,
            f"**{data_YTeeth['yt']['proName']}**\n" +
            f"APY: {round(data_YTeeth['impliedApy']* 100, 3)}%\n" +
            f"\n**{data_YTrseth['yt']['proName']}**\n" +
            f"APY: {round(data_YTrseth['impliedApy']* 100, 3)}%\n",
            parse_mode='Markdown')
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")


# Schedule the message
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
