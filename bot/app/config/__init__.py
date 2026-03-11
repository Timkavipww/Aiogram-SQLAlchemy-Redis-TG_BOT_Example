from .logging_config import logger, setup_logger
from .settings import Config

setup_logger()
config = Config()

__all__ = ["logger", "config"]