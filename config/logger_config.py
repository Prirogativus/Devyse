import logging
import os

"""
This module serves only to configure a program logger.
Its main function - setup_loger should be called only once in the main.py
"""

log_dir = "log"
os.makedirs(log_dir, exist_ok=True)  

log_path = os.path.join(log_dir, "app.log")

def setup_logger():
    """Configure logging to write messages to file and console.

    Logging level is set to INFO. Messages are formatted with timestamp,
    severity level, and the log text. Logs are written to a file at log_path
    (in overwrite mode, UTF-8 encoding) and simultaneously printed to stdout.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, mode='w', encoding="utf-8"),
            logging.StreamHandler() 
        ]
    )

