from dotenv import load_dotenv
import os 

load_dotenv()

#Database access
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

#Telegram
TELEGRAM_BOT_TOKEN = os.getenv("Telegram_BOT_TOKEN")