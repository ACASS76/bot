import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 0))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
DEFAULT_AFFILIATE_LINK = os.getenv("DEFAULT_AFFILIATE_LINK")