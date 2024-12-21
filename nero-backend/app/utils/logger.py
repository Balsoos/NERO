import logging
import os

# Get log level from environment variables or set default to DEBUG
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# Set up logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create logger
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log", mode="a", encoding="utf-8")  # Log to file
    ]
)

logger = logging.getLogger("NERO")

""" 
import logging

# Configure the logger
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def log_info(message: str):
    logging.info(message)

def log_warning(message: str):
    logging.warning(message)

def log_error(message: str):
    logging.error(message)
"""

