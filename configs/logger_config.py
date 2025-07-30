import logging
import os

log_dir = "log"
os.makedirs(log_dir, exist_ok=True)  

log_path = os.path.join(log_dir, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler() 
    ]
)

