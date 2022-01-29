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

def checkUsername(username):

    if username.username == "markkmarkmark" and username.id == "974308491":
        return True
    else:
        return False


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user 

    if not checkUsername(user): return

    update.message.reply_markdown_v2(
        fr'Hello {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def main():
    updater = Updater(config["TOKEN"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
