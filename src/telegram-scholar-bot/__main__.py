from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv("TOKEN")

from .bot import Bot

if __name__ == "__main__":
    bot = Bot(TOKEN)
    print("Bot started")
    bot.app.run_polling()
