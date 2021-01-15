import os
from dotenv import load_dotenv

load_dotenv()

# Bot setup
BOT_TOKEN = os.getenv("BOT_TOKEN")

#  Database settings
# Settings format:
# For postgres postgres:*user*:*password*:*host*:*database*
# For sqlite: sqlite:*name*
DB_SETTINGS = os.getenv("DB_SETTINGS")

#  Updater settings
request_each = 10  # in seconds
