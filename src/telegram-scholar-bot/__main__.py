from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv("TOKEN")

class Bot():
    def __init__(self, token):
        self.app = ApplicationBuilder().token(TOKEN).build()


if __name__ == "__main__":
    print('Работаем!\n')
    bot = Bot(TOKEN)
    bot.app.run_polling()
