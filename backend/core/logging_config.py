import logging
import os
from logging.handlers import RotatingFileHandler

# Get environment (default to development)
ENV = os.getenv("ENV", "development")

# Logging levels based on environment
LOG_LEVEL = logging.DEBUG if ENV == "development" else logging.INFO
LOG_FILE = os.path.join(os.getcwd(), "project_yoked.log")

# Logging format
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"

# Configure logging
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)
root_logger.handlers = []  # Clear existing handlers

# Add StreamHandler for console logs
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
root_logger.addHandler(console_handler)

# Add RotatingFileHandler for file logs
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
root_logger.addHandler(file_handler)

# Convenience function to create loggers
def get_logger(name):
    return logging.getLogger(name)
