from telegram.ext import (
    Updater,
)
import logging
from foodshare.commands.cook import conv_handler_cook,error

d = 1

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)





def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("921706886:AAE8KrSbCPMr1lB1VFZINP_M1s8wibaMkTE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'


    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler_cook)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
