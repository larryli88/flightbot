#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nluchat
from nluchat import send_message

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, this is flight bot~\nI can help you to search for the best deal and help you check in.')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Hi, this is flight bot~\nI can help you to search for the best deal and help you check in.')

def respond(bot, update):
    """respond the user message."""
    # Initialize params dictionary
    nluchat.state_global, nluchat.params_global, response = send_message(update.message.text, nluchat.state_global, nluchat.params_global)
    update.message.reply_text(text=response, parse_mode=ParseMode.HTML)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    # request_kwargs to use socks 5 proxy
    #updater = Updater("961802444:AAHcW7PT0QakR4g6CEJmX_r4pmuoAacxCGg", request_kwargs={'proxy_url': 'http://127.0.0.1:1087/'})
    updater = Updater("961802444:AAHcW7PT0QakR4g6CEJmX_r4pmuoAacxCGg")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # respond other user input
    dp.add_handler(MessageHandler(Filters.text, respond))

    # log all errors
    dp.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()