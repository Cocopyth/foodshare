import logging

from telegram.ext import Updater

from foodshare.handlers.cook_conversation.cook_handler import cook_handler
from foodshare.handlers.error_handler import error_handler

# activate logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def main():
    # create the updater
    updater = Updater(
        '921706886:AAE8KrSbCPMr1lB1VFZINP_M1s8wibaMkTE', use_context=True
    )

    # get the dispatcher
    dispatcher = updater.dispatcher

    # add the `ConversationHandler` handler to the dispatcher, it will be
    # used to handle the updates
    dispatcher.add_handler(cook_handler)

    # log all errors
    dispatcher.add_error_handler(error_handler)

    # start the bot
    updater.start_polling()

    # run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
