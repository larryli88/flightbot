#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nluchat
from nluchat import startNLU

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
    update.message.reply_text('Hi! This is Flight Bot. \nYou can search by flight number or search by destination and origin~')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def respond(bot, update):
    """respond the user message."""
    # Initialize params dictionary
    response, nluchat.params_global = respond(update.message.text, nluchat.params_global)
    update.message.reply_text(response)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("961802444:AAHcW7PT0QakR4g6CEJmX_r4pmuoAacxCGg", request_kwargs={'proxy_url': 'http://127.0.0.1:1087/'})

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