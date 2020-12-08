import logging, sys
from pathlib import Path

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
_logger = logging.getLogger(__name__)

class Logger:
    @staticmethod
    def set_level(level: int):
        _logger.setLevel(level)

    @staticmethod
    def log(msg: str, *args: list):
        _logger.info(msg, *args)

    @staticmethod
    def debug(msg: str, *args: list):
        _logger.debug(msg, *args)

    @staticmethod
    def warn(msg: str, *args: list):
        _logger.warning(msg, *args)

    @staticmethod
    def error(msg: str, *args: list):
        _logger.error(msg, *args)

    @staticmethod
    def critical(msg: str, *args: list):
        _logger.critical(msg, *args)
