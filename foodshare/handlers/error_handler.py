import logging

logger = logging.getLogger(__name__)


def error_handler(update, context):
    """Log errors caused by updates."""
    logger.warning(f'Update {update} caused error {context.error}.')
