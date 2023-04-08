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
        return_string.append("You are near:\n")

        for result in data["GeocodeInfo"]:
            return_string.append(
                f"{result['BLOCK']} {result['ROAD']} {result['BUILDINGNAME']}, S({result['POSTALCODE']})\n")
    else:
        print(f"Error: {response.status_code}")

    result = "".join(return_string)

    bot.reply_to(
        message, "".join(result)
    )


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


# Handle all uncaught messages
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    print(
        f"Received message from user {message.from_user.username} ({message.from_user.id}): {message.text}")


bot.polling()
