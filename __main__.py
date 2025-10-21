import os

from dotenv import load_dotenv
from exhandler import CheetahExtractor

load_dotenv()

Acceess_token = os.getenv('Token')

def main():
   try:
      extractor_bot = CheetahExtractor(Acceess_token)
      extractor_bot.run_application()
   except Exception as error:
      pass
if __name__ == "__main__":
   main()