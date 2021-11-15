# # -*- coding: utf-8 -*-
# """Logger"""
import logging

########### uncomment when run local "##############

from sys import stdout
from logging import Formatter, getLogger, FileHandler, StreamHandler
from rainbow_logging_handler import RainbowLoggingHandler

LOGGER_STREAM_FORMAT = "[%(asctime)s] - [%(levelname)s] - [%(name)s] - [%(pathname)s:%(lineno)d] - %(message)s"
LOGGER_STREAM_FORMAT = "[%(asctime)s] - [%(levelname)s] - %(message)s"
LOGGER_FILE_FORMAT = "[%(asctime)s] - %(message)s"
LOGGER_DEFAULT_LEVEL = 'WARNING'
LOGGER_LEVEL = 'DEBUG'
LOGGER_FILE_NAME = 'fssm.log'

def __get_file_logger_handler(formatter: Formatter, log_level: str) -> StreamHandler:
    handler = FileHandler(LOGGER_FILE_NAME, mode='a')
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    return handler


def __get_stream_logger_handler(formatter: Formatter, log_level: str) -> StreamHandler:
    handler = RainbowLoggingHandler(
        stdout,
        color_asctime=('cyan', None, True),
        color_levelname=('cyan', None, True),
        color_message_debug=('blue', None, False),
        color_message_info=('green', None, False),
        color_message_warning=('yellow', None, False),
        color_message_error=('red', None, False),
        color_message_critical=('magenta', None, False)
    )
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    return handler


def __setup_logger(logger, log_level: str, handlers):
    del logger.handlers[:]
    for handler in handlers:
        logger.addHandler(handler)
    logger.setLevel(log_level)
    logger.propagate = False

def __get_root_logger():
    # file_handler = __get_file_logger_handler(Formatter(LOGGER_FILE_FORMAT), LOGGER_LEVEL)
    stream_handler = __get_stream_logger_handler(Formatter(LOGGER_STREAM_FORMAT), LOGGER_LEVEL)
    # handlers = [file_handler, stream_handler]
    handlers = [stream_handler]
    root_logger = getLogger()

    __setup_logger(root_logger, LOGGER_LEVEL, handlers)

    for logger in (
        getLogger('chardet.charsetprober'),
        getLogger('urllib3'),
        getLogger('botocore'),
        getLogger('boto3.resources')
    ):
        __setup_logger(logger, LOGGER_DEFAULT_LEVEL, handlers)

    return root_logger


LOGGER = __get_root_logger()
