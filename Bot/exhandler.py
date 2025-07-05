import os
from collections import Counter
from telegram import Update
import time
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
import re


def normalize_number(number: str) -> str:
    return re.sub(r'\D', '', number.strip())


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    await update.message.reply_text(f'You are welcome @{username}.')


async def handle_txt_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    
    if document.mime_type == "text/plain":
        os.makedirs("downloads", exist_ok=True)

        file = await context.bot.get_file(document.file_id)
        file_path = f"downloads/{document.file_name}"

        await file.download_to_drive(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                phone_number_list = lines = [normalize_number(line) for line in f if line.strip()]
            

            data = []
            testing_number = []
            seen_numbers = set()
            duplicate_number = set()
            count = dict(Counter(phone_number_list))
            duplicates_found = False
          
            for phone_numbers in phone_number_list:
                if phone_numbers in seen_numbers:
                    duplicate_number.add(phone_numbers)
                    duplicates_found = True
     
                else:
                    seen_numbers.add(phone_numbers)
                    
            dup_list = list(duplicate_number)
            
            if duplicates_found:
                dup_line = chr(10).join( f'The phone_numbers {number} found in line {phone_number_list.index(str(number))}'for number in phone_number_list if number in dup_list) 
                duplicate = chr(10).join(f'{number} appeared {count[str(number)]} times' for number in duplicate_number) 
                message = (
                    f"<b>Phone-number Length:</b>\n<pre>{len(phone_number_list)}</pre>"
                    f"<b>Duplicate number found:</b>\n<pre>{duplicate}</pre>\n"
                    f"<b>Line number:</b> <pre>{dup_line}</pre>\n"
                )
                await update.message.reply_text(message, parse_mode=ParseMode.HTML)
    
            else:
                await update.message.reply_text("✅ No duplicate numbers found.")

        except Exception as e:
            print(e)
            await update.message.reply_text(
                f"❌ Error reading the file:\n<pre>{e}</pre>", parse_mode=ParseMode.HTML
            )
    else:
        await update.message.reply_text("❗ Please send a valid .txt file.")
        