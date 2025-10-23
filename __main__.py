import os
import threading
from flask import Flask
from dotenv import load_dotenv
from exhandler import CheetahExtractor

load_dotenv()

ACCESS_TOKEN = os.getenv("Token")

# Create a small web server (Render requires this)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    extractor_bot = CheetahExtractor(ACCESS_TOKEN)
    extractor_bot.run_application()

if __name__ == "__main__":
    # Run bot in background
    threading.Thread(target=run_bot).start()

    # Bind to Render port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
