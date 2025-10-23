import os
import logging
from dotenv import load_dotenv
from exhandler import CheetahExtractor

load_dotenv()

ACCESS_TOKEN = os.getenv('Token')

# Set up logging to see errors on Render
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    if not ACCESS_TOKEN:
        logging.error("Bot token not found! Make sure it's in .env as 'Token'")
        return

    try:
        extractor_bot = CheetahExtractor(ACCESS_TOKEN)
        # Keep the bot running; assuming run_application() uses run_polling() internally
        extractor_bot.run_application()
    except Exception as error:
        logging.exception("Bot failed to start:")

if __name__ == "__main__":
    main()
