from dotenv import load_dotenv
from os import getenv

from scholarly import (
    ProxyGenerator,
    scholarly,
)

load_dotenv()
TOKEN = getenv("TOKEN")

from .bot import Bot

if __name__ == "__main__":

    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)

    bot = Bot(TOKEN)
    print("Bot started")
    bot.app.run_polling()
