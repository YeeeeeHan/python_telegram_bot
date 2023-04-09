import logging
import math
import os
from enum import Enum
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

user_state = {}


class Interests(Enum):
    MUSUEM = "museum"
    TOURISM = "tourism"
    HISTORICSITES = "historicsites"
    HAWKERCENTRE = "hawkercentre"
    COMMUNITYCLUBS = "communityclubs"
    HEALTHIERDINING = "healthierdining"


@bot.message_handler(commands=['start'])
def handle_museum(message):
    bot.send_message(
        message.chat.id, f"🤖 *Welcome to MyBot!*\n\n"
        "I'm here to help you discover interesting places in your city. Here's a list of commands I can handle:\n\n"
        "/museum - Find museums nearby\n"
        "/tourism - Discover tourist attractions nearby\n"
        "/historicsites - Explore historic sites nearby\n"
        "/hawkercentre - Locate hawker centres nearby\n"
        "/communityclubs - Search for community clubs nearby\n"
        "/healthierdining - Find healthier dining options nearby\n\n"
        "If you have any questions or suggestions, feel free to ask!", parse_mode='Markdown')


@ bot.message_handler(commands=[Interests.MUSUEM.value])
def handle_museum(message):
    user_state[message.from_user.id] = 'asking_museum'
    bot.send_message(
        message.chat.id, f"Send your location and we will let you know the nearest {print_command(Interests.MUSUEM.value)}!")


@ bot.message_handler(commands=[Interests.TOURISM.value])
def handle_tourism(message):
    user_state[message.from_user.id] = 'asking_tourism'
    bot.send_message(
        message.chat.id, f"Send your location and we will let you know the nearest {print_command(Interests.TOURISM.value)}!")


@ bot.message_handler(commands=[Interests.HISTORICSITES.value])
def handle_historicsites(message):
    user_state[message.from_user.id] = 'asking_historicsites'
    bot.send_message(
        message.chat.id, f"Send your location and we will let you know the nearest {print_command(Interests.HISTORICSITES.value)}!")


@ bot.message_handler(commands=[Interests.HAWKERCENTRE.value])
def handle_hawkercentre(message):
    user_state[message.from_user.id] = 'asking_hawkercentre'
    bot.send_message(
        message.chat.id, f"Send your location and we will let you know the nearest {print_command(Interests.HAWKERCENTRE.value)}!")


@ bot.message_handler(commands=[Interests.COMMUNITYCLUBS.value])
def handle_communityclubs(message):
    user_state[message.from_user.id] = 'asking_communityclubs'
    bot.send_message(
        message.chat.id, f"Send your location and we will let you know the nearest {print_command(Interests.COMMUNITYCLUBS.value)}!")


@ bot.message_handler(commands=[Interests.HEALTHIERDINING.value])
def handle_healthierdining(message):
    user_state[message.from_user.id] = 'asking_healthierdining'
    bot.send_message(
        message.chat.id, f"Send your location and we will let you know the nearest {print_command(Interests.HEALTHIERDINING.value)}!")


def haversine_distance(user_latlong, item_latlong):
    # Radius of the Earth in kilometers
    R = 6371

    # Convert latitude and longitude to radians
    lat1, lon1 = math.radians(user_latlong[0]), math.radians(user_latlong[1])
    lat2, lon2 = math.radians(item_latlong[0]), math.radians(item_latlong[1])

    # Calculate the differences between latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance


# Handle location messages
@ bot.message_handler(content_types=['location'])
def handle_location(message):
    user_latlong = (message.location.latitude, message.location.longitude)
    command = ""

    user_id = message.from_user.id
    if user_id in user_state:
        if user_state[user_id] == 'asking_museum':
            command = 'museum'
            user_state[user_id] = None
        if user_state[user_id] == 'asking_tourism':
            command = 'tourism'
            user_state[user_id] = None
        if user_state[user_id] == 'asking_historicsites':
            command = 'historicsites'
            user_state[user_id] = None
        if user_state[user_id] == 'asking_hawkercentre':
            command = 'hawkercentre'
            user_state[user_id] = None
        if user_state[user_id] == 'asking_communityclubs':
            command = 'communityclubs'
            user_state[user_id] = None
        if user_state[user_id] == 'asking_healthierdining':
            command = 'healthierdining'
            user_state[user_id] = None

    else:
        bot.send_message(
            message.chat.id, "To start a conversation, please type /musuem, /tourism or /historicsites")
        # Why is this return important?
        return

    # Define the URL for the request
    url = f"https://developers.onemap.sg/privateapi/themesvc/retrieveTheme?queryName={command}&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwMTYxLCJ1c2VyX2lkIjoxMDE2MSwiZW1haWwiOiJsaW15ZWVoYW5AZ21haWwuY29tIiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNjgwOTczNDQxLCJleHAiOjE2ODE0MDU0NDEsIm5iZiI6MTY4MDk3MzQ0MSwianRpIjoiMzdjNWZhNjM2M2M5NDZmZTI5ZGNlZjY1MDA2ZWFlZDAifQ.WaefQMWiWZKU9QJG1GJvGZ0Mo-l0aJZwOF4tI14Ren8"
    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        minDist = 1000000
        minName = ""
        minDescription = ""
        minAddress = ""

        for result in data["SrchResults"][1:]:         # Why need [1:]?
            latitude, longitude = map(float, result['LatLng'].split(','))
            location_tuple = (latitude, longitude)
            dist = haversine_distance(
                user_latlong, location_tuple)

            if dist < minDist:
                # Why can't this chunk of code work?
                '''
                minName = result['NAME']
                minDescription = result['DESCRIPTION']
                minAddress = result['ADDRESSBLOCKHOUSENUMBER'] + \
                    result['ADDRESSSTREETNAME'] + result['ADDRESSPOSTALCODE']
                '''

                # What happens if you don't have this line?
                minDist = dist
                # Why is null_if_not_present() needed?
                minName = null_if_not_present(result, 'NAME')
                minDescription = null_if_not_present(result, 'DESCRIPTION')
                minAddress = null_if_not_present(result, 'ADDRESSBLOCKHOUSENUMBER') +\
                    null_if_not_present(result, 'ADDRESSBUILDINGNAME') + \
                    null_if_not_present(
                        result, 'ADDRESSSTREETNAME') + null_if_not_present(result, 'ADDRESSPOSTALCODE')

        bot.reply_to(
            # Why do you need round?
            message, f"*Nearest {print_command(command)}:*\n🏡:  {minName} \n❓:  {minDescription} \n📍:  {minAddress} \n📐:  {round(minDist, 2)}km", parse_mode='Markdown'
        )

    else:
        print(f"Error: {response.status_code}")
        bot.send_message(
            message.chat.id, f"Error: {response.status_code}")


# Why do you need this function?
def null_if_not_present(object, key):
    if key in object:
        # Why do you need " "?
        return object[key] + "  "
    else:
        return ""


def print_command(command):
    if command == Interests.MUSUEM.value:
        return 'museum'
    if command == Interests.TOURISM.value:
        return 'tourism'
    if command == Interests.COMMUNITYCLUBS.value:
        return 'community club'
    if command == Interests.HEALTHIERDINING.value:
        return 'healthier dining'
    if command == Interests.HISTORICSITES.value:
        return 'historical site'
    if command == Interests.HAWKERCENTRE.value:
        return 'hawker centre'


bot.polling()
