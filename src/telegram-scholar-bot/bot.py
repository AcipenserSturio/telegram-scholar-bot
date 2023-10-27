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

PUB = """<b>{name}</b>
by {authors} in {year}

{abstract}
<b><a href="{link}">[read full]</a></b>
"""


class Bot():
    def __init__(self, token: str):
        self.app = ApplicationBuilder().token(token).write_timeout(30).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("search_author", self.search_author))
        self.app.add_handler(CommandHandler("search_pub", self.search_pub))

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
        first_author, message = await common_interaction(
            update,
            context,
            " ".join(context.args),
            "Please wait as I search for <i>\"{}\"</i>...",
            "No author found by searching \"{}\"",
            scholarly.search_author,
        )
        await message.edit_text(
            parse_mode = "html",
            text = AUTHOR.format(
                name = first_author["name"],
                affiliation = first_author["affiliation"],
                email = first_author["email_domain"],
                cited = first_author["citedby"],
                image = first_author["url_picture"],
            ),
        )

    @staticmethod
    async def search_pub(
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
        ):
        first_pub, message = await common_interaction(
            update,
            context,
            " ".join(context.args),
            "Please wait as I search for <i>\"{}\"</i>...",
            "No publications found by searching \"{}\"",
            scholarly.search_pubs,
        )
        await message.edit_text(
            parse_mode = "html",
            disable_web_page_preview=True,
            text = PUB.format(
                link = first_pub["pub_url"],
                name = first_pub["bib"]["title"],
                authors = "; ".join(first_pub["bib"]["author"]),
                year = first_pub["bib"]["pub_year"],
                abstract = first_pub["bib"]["abstract"],
            ),
        )

async def common_interaction(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        query: str,
        wait_message: str,
        fail_message: str,
        api: callable,
    ):
    # Unites common user handling of "authors" and "publications"
    # Useful to catch weird behaviour in both
    # Returns a response (dict) and a message (to be edited)

    message = await context.bot.send_message(
        chat_id = update.effective_chat.id,
        parse_mode = "html",
        text = wait_message.format(query),
    )

    # Catch empty queries
    if not len(query.strip()):
        await message.edit_text(
            text = fail_message.format(query)
        )
        return

    response = api(query)

    # Catch empty responses
    if not (response := peek(response)):
        await message.edit_text(
            text = fail_message.format(query)
        )
        return

    first_response = response[0]
    print(first_response)
    return first_response, message
