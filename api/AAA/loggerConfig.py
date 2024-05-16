import logging
import logging.handlers
from config import Config
import colorlog

def appendToLogger(filePath = ''):
    # Define the log format
    formatter = '%(asctime)s - [%(levelname)s][%(name)s-%(lineno)d:%(thread)d] %(message)s'
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s" + formatter,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    if (Config.DEBUG):
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO

    handlers = []

    if filePath:
        # Create a file handler
        file_handler = logging.FileHandler(filePath)
        file_handler.setLevel(logLevel)
        file_handler.setFormatter(logging.Formatter(formatter))
        handlers.append(file_handler)

    # Create a console handler
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logLevel if Config.DEBUG else logging.WARNING)
    console_handler.setFormatter(color_formatter)
    handlers.append(console_handler)

    logging.basicConfig(
        level=logLevel,
        handlers=handlers
    )
