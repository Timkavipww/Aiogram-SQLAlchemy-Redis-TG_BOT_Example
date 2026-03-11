import logging
import sys

logger = logging.getLogger("bot_logger")

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        stream=sys.stdout
    )
    
    logger.setLevel(logging.INFO)
    
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)