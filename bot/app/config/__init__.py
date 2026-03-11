from .logging_config import logger, setup_logger
from .settings import Config

setup_logger()
config = Config()
config.validate_config()
__all__ = ["logger", "config"]