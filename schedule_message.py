import schedule
import time
import telebot
from rss_feed import get_anime
from os import getenv
from dotenv import load_dotenv

load_dotenv()
print("Loaded dotenv.")
bot = telebot.TeleBot(getenv("API_KEY"), parse_mode=None)
chat_id = getenv("CHAT_ID")

def send_anime_daily():

    bot.send_message(chat_id, get_anime(), parse_mode="MarkdownV2")
    print("Sent anime list at {} on {}.".format(time.strftime("%X"), time.strftime("%x")))

#schedule.every(1).minutes.do(send_anime_daily)
print("Scheduled process send anime daily.")
schedule.every().day.at("06:00").do(send_anime_daily)

while True:
    schedule.run_pending()
    time.sleep(1)

