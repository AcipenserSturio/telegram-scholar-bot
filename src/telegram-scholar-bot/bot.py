from telegram import Update  # класс для обновления в чате
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from scholarly import scholarly

from .utils import peek


AUTHOR = """<b>{name}</b>
{affiliation}

E-mail: {email}
Cited {cited} times
<a href="{image}">&#8205;</a>
"""


class Bot():
    def __init__(self, token: str):
        self.app = ApplicationBuilder().token(token).write_timeout(30).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("search_author", self.search_author))

    @staticmethod
    async def start(
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
        ):

        print(update.effective_chat)
        print(update.effective_user)
        print(update.effective_message)
        print(update.effective_message.text)

        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "I'm a bot!",
        )

    @staticmethod
    async def search_author(
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
        ):
        author = " ".join(context.args)
        print(author)
        query = scholarly.search_author(author)

        if not (query := peek(query)):
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = f"No author found by searching \"{author}\"",
            )
            return

        first_author = query[0]
        print(first_author)

        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            parse_mode = "html",
            text = AUTHOR.format(
                name = first_author["name"],
                affiliation = first_author["affiliation"],
                email = first_author["email_domain"],
                cited = first_author["citedby"],
                image = first_author["url_picture"],
            ),
        )

