import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

IS_TO_FILE = os.getenv("IS_TO_FILE", "False")
ROTATION = os.getenv("ROTATION", "1 day")
RETENTION = os.getenv("RETENTION", "30 days")
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | <cyan>{name}</cyan>:"
    "<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

logger.remove()
if IS_TO_FILE == "True":
    logger.add(
        "./auth_microservice/logs/auth_microservice.log",
        rotation=ROTATION,
        retention=RETENTION,
        format=LOG_FORMAT,
        level="DEBUG",
        enqueue=True,
    )
else:
    logger.add(
        sys.stderr,
        format=LOG_FORMAT,
        level="DEBUG",
        enqueue=True,
    )
base_logger = logger

# logger.debug("This is a debug message.")

# logger.info("This is an info message.")

# logger.success("This is a success message.")

# logger.warning("This is a warning message.")

# logger.error("This is an error message.")

# logger.critical("This is a critical message.")
