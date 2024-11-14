import sys
from loguru import logger

logger.remove()


logger.add(
    sys.stderr,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | <cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    ),
    level="DEBUG",
)
base_logger = logger

# logger.debug("This is a debug message.")

# logger.info("This is an info message.")

# logger.success("This is a success message.")

# logger.warning("This is a warning message.")

# logger.error("This is an error message.")

# logger.critical("This is a critical message.")
