import logging

# Configure the logging system
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# Creating a logger instance
logger = logging.getLogger(__name__)

# Logging messages at different severity levels
# logger.debug("This is a debug message")  # For debugging details
# logger.info("This is an info message")   # General information
# logger.warning("This is a warning message")  # Warning about potential problems
# logger.error("This is an error message")  # Errors that occur
# logger.critical("This is a critical message")  # Severe errors

# try:
#     x = 1 / 0  # This will raise a ZeroDivisionError
# except ZeroDivisionError:
#     logger.exception("An error occurred due to division by zero")

# logger.info("I told you so")
# logger.warning("watch out!")
logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
logging.warning('%s before you %s', 'Look', 'leap!')