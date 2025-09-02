import os

from dotenv import load_dotenv
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,filters)

from Extractor.Bot.exhandler import sending_number_file_handler, start_cmd, text_file_editor

load_dotenv()

Acceess_token = os.getenv('Token')

def main():
   try:
      app = ApplicationBuilder().token(Acceess_token).build()
      app.add_handler(CommandHandler("start", start_cmd))
      app.add_handler(MessageHandler(filters.Document.ALL, sending_number_file_handler))
      app.add_handler(MessageHandler(filters.TEXT, text_file_editor))
      print('bot starting....')
      app.run_polling()

   except Exception as error:
      print(error)
if __name__ == "__main__":
   main()