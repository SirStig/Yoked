import logging
import os
from logging.handlers import RotatingFileHandler

# Get environment (default to development)
ENV = os.getenv("ENV", "development")

# Logging levels based on environment
LOG_LEVEL = logging.DEBUG if ENV == "development" else logging.INFO
LOG_FILE = "project_yoked.log"

# Logging format
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),  # Console output
        RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)  # Rotating log file
    ],
)

# Convenience function to create loggers
def get_logger(name):
    logger = logging.getLogger(name)
    return logger
