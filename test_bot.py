import telebot
import re
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from os import listdir, getenv
from rss_feed import get_news, get_anime
from updater import updater
from dotenv import load_dotenv
from scan_network import scan_devices

# Loading the environmental variables
load_dotenv()

# Setup the bot and several important variables
bot = telebot.TeleBot(getenv("API_KEY"), parse_mode=None)
note_folder = "notes/"
news_source = ["abc.net.au", "thestar.com.my", "bbc.com", "r/news"]
chat_id = getenv("CHAT_ID")
version_id ="0.0.6_alpha"

# Startup greeting
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_user(message): return

    bot.reply_to(message, "Hello Mark!\n\nRobot Mark Version : " + version_id)

# Updater Script
@bot.message_handler(commands=['update'])
def updating(message):
    if not check_user(message): return

    bot.send_message(chat_id, "Updating Robot Mark ...")

    update_code = updater()
    if update_code == 124:
        bot.send_message(chat_id, "Robot Mark update failed ... \nRequires manual intervention.")
    else:
        bot.send_message(chat_id, "Robot Mark at latest version. \nUpdate Code : {}\n\nRebooting in 5 seconds ...".format(update_code))
        bot.stop_polling()
        bot.stop_bot()
        return

# Grabbing Top 10 news articles provided by RSS
@bot.message_handler(commands=['news'])
def send_news(message):
    if not check_user(message): return

    news_select = InlineKeyboardMarkup(row_width=1)
    #news_select.add(InlineKeyboardButton(news_source[0], callback_data="0"),
    #                InlineKeyboardButton(news_source[1], callback_data="1"),
    #                InlineKeyboardButton(news_source[2], callback_data="2"))
    [news_select.add(InlineKeyboardButton(item, callback_data="{}".format(news_source.index(item)))) for item in news_source]

    bot.send_message(chat_id, "Pick a news source :", reply_markup=news_select)

@bot.callback_query_handler(func=lambda reply: True)
def select_news_source(reply):
    if not check_user(reply): return

    reply_index = int(reply.data)
    if not reply_index in range(0, len(news_source)):
        return
    
    bot.send_message(chat_id, get_news(reply_index, news_source[reply_index]), parse_mode="MarkdownV2")

# Grabbing yesterday/ today's recently aired anime
@bot.message_handler(commands=['anime'])
def send_news(message):
    if not check_user(message): return

    bot.reply_to(message, get_anime(), parse_mode="MarkdownV2")

@bot.message_handler(commands=['ctd_devices'])
def send_connected_devices(message):
    devices = scan_devices()
    if devices != "":

        bot.reply_to(message, "New Devices found on network since last scan: \n" + devices, parse_mode="MarkdownV2")
    else:

        bot.reply_to(message, "No new devices found on network since last scan.")

# Section WIP
# Note method still undecided
@bot.message_handler(commands=['note'])
def store_note(message):
    if not check_user(message): return

    contents = message.text.replace("/note", "")
    filename = message.text.split()[1] + ".txt"
    file = open(note_folder + filename, "a")
    file.write(contents + " \n")
    file.close()

    bot.reply_to(message, "Wrote into {} : \n `{}`".format(re.escape(filename), re.escape(contents)), parse_mode="MarkdownV2")

@bot.message_handler(commands=['show_note'])
def show_note(message):
    if not check_user(message): return

    notes = ""
    for item in listdir(note_folder):
        notes += " - " + item.replace(".txt","") + "\n"

    bot.reply_to(message, notes)

# When all else fails, send a message
@bot.message_handler(func=lambda message: True)
def final_handler(message):
    if not check_user(message): return

    bot.send_message(chat_id, "I'm not sure I understand what you're saying.")

# Simple check to verify owner before code execution
def check_user(msg):
    # Always check if the excecution was by the owner
    return 1 if str(msg.from_user.id) == chat_id else 0

bot.polling()
