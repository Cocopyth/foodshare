import logging
import os

from telegram.ext import Updater

from foodshare.handlers.cook_conversation.cook_handler import cook_handler
from foodshare.handlers.error_handler import error_handler

# activate logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


class BotTokenUndefined(Exception):
    pass


def main():
    # get the bot token from the `TELEGRAM_BOT_TOKEN` environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if bot_token is None:
        raise BotTokenUndefined(
            'Please set the TELEGRAM_BOT_TOKEN environment variable'
        )

    # create the updater
    updater = Updater(bot_token, use_context=True)

    # get the dispatcher
    dispatcher = updater.dispatcher

    # add a handler to the dispatcher, it will be used to handle the updates
    dispatcher.add_handler(cook_handler)

    # log all errors
    dispatcher.add_error_handler(error_handler)

    # start the bot
    updater.start_polling()

    # run the bot until it is stopped (by hitting Ctrl-C for example)
    updater.idle()


if __name__ == '__main__':
    main()
