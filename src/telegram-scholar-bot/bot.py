from telegram import Update  # класс для обновления в чате
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
class Bot():
    def __init__(self, token: str):
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.start))

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
