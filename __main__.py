import os

from dotenv import load_dotenv
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          filters)

from extractor.Bot.exhandler import handle_txt_file, start_cmd

load_dotenv()

Access_token = os.getenv("Token")


def main():
    app = ApplicationBuilder().token(Access_token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_txt_file))
    app.run_polling()


if __name__ == "__main__":
    main()
