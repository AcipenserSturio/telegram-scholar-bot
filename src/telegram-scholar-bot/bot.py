from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

from scholarly import scholarly

from .utils import first


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

HELP = """Hello\! I am a bot that lets you search authors and publications on Google Scholar\.
Try the following commands\:
`/search_author` "Author Name"
`/search_pub` "Publication Name"
"""


class Bot():
    def __init__(self, token: str):
        self.app = ApplicationBuilder().token(token).write_timeout(30).build()
        self.app.add_handler(CommandHandler("help", help_message))
        self.app.add_handler(CommandHandler("search_author", search_author))
        self.app.add_handler(CommandHandler("search_pub", search_pub))
        self.app.add_handler(CallbackQueryHandler(button))


async def help_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
    message = await context.bot.send_message(
        chat_id = update.effective_chat.id,
        parse_mode = "MarkdownV2",
        text = HELP,
    )


async def search_author(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
    query = " ".join(context.args)
    message = await send_wait_message(update, context, f"Please wait as I search for <i>\"{query}\"</i>...")
    if await is_empty_query(message, query, "This is an empty query. Try adding text!"):
        return
    response = scholarly.search_author(query)
    # Catch empty responses
    if not (response := first(response)):
        await message.edit_text(f"No author found by searching \"{query}\"")
        return
    await message.edit_text(
        parse_mode = "html",
        text = format_author(response),
    )


async def search_pub(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
    index = 0
    query = " ".join(context.args)
    message = await send_wait_message(update, context, f"Please wait as I search for <i>\"{query}\"</i>...",)
    if await is_empty_query(message, query, "This is an empty query. Try adding text!"):
        return
    response = scholarly.search_pubs(query, start_index=index)
    # Catch empty responses
    if not (response := first(response)):
        await message.edit_text(f"No publications found by searching \"{query}\"")
        return
    await message.edit_text(
        parse_mode = "html",
        disable_web_page_preview=True,
        text = format_publication(response),
        reply_markup = get_keyboard(query, index),
    )

async def button(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:

    query, index = update.callback_query.data.split("|")
    index = int(index)
    print(query, index)
    response = scholarly.search_pubs(query, start_index=index)
    # Catch empty responses
    if not (response := first(response)):
        await message.edit_text(f"No publications found by searching \"{query}\"")
        return
    await update.callback_query.edit_message_text(
        parse_mode = "html",
        disable_web_page_preview=True,
        text = format_publication(response),
        reply_markup = get_keyboard(query, index),
    )


async def send_wait_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        wait_message: str,
    ):
    return await context.bot.send_message(
        chat_id = update.effective_chat.id,
        parse_mode = "html",
        text = wait_message,
    )


async def is_empty_query(
        message,
        query: str,
        fail_message: str,
    ):

    # Catch empty queries
    if not len(query.strip()):
        await message.edit_text(fail_message)
        return True


def format_publication(response: dict) -> str:
    return PUB.format(
            link = response["pub_url"],
            name = response["bib"]["title"],
            authors = "; ".join(response["bib"]["author"]),
            year = response["bib"]["pub_year"],
            abstract = response["bib"]["abstract"],
        )

def format_author(response: dict) -> str:
    return AUTHOR.format(
            name = response["name"],
            affiliation = response["affiliation"],
            email = response["email_domain"],
            cited = response["citedby"],
            image = response["url_picture"],
        )

def get_keyboard(query: str, index: int):
    if not index:
        return InlineKeyboardMarkup([[
            InlineKeyboardButton(f"Next", callback_data=f"{query}|{index+1}"),
        ]])
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"Previous", callback_data=f"{query}|{index-1}"),
        InlineKeyboardButton(f"Next", callback_data=f"{query}|{index+1}"),
    ]])
