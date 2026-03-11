from .logging_config import logger, setup_logger
from .settings import config

setup_logger()

__all__ = ["logger", "config"]