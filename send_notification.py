import logging

from dotenv import dotenv_values
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Loading the environmental variables
config = dotenv_values(".env")

# Enable logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def checkUsername(username) -> bool:

    if username.username == "markkmarkmark" and username.id == "974308491":
        return True
    else:
        return False

def main():
    updater = Updater(config["TOKEN"])

    dispatcher = updater.dispatcher



if __name__ == '__main__':
    main()
