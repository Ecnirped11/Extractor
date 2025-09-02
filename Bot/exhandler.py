import os
from telegram import Update
import time
from .message_tracker.dispatchers.txt_refined import RefinedTextHandler
from telegram.constants import ParseMode
from telegram.error import TimedOut, NetworkError
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from .dup_extractor.duplicate import DuplicateExtractor

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    await update.message.reply_text(f'You are welcome @{username}.')

async def handle_txt_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    caption = update.message.caption
    text = update.message.text
    
    RESOLVE_COMMAND = "resolve"
    CLEAR_COMMAND = "clear"

    try:
        if text:
            refined_text = RefinedTextHandler(text, RESOLVE_COMMAND, CLEAR_COMMAND)
            content = refined_text.crop_out_content()
            if text.lower() == RESOLVE_COMMAND:
                await update.message.reply_text(content)
            elif text.lower() == CLEAR_COMMAND:
                await update.message.reply_text("✅ File cleared successfully.")
    except TimedOut:
           await update.message.reply_text("Error: unstable network..")

    if document:
        if document.mime_type == "text/plain":
            os.makedirs("downloads", exist_ok=True)
          
            file = await context.bot.get_file(document.file_id)  
            file_path = f"downloads/{document.file_name}"  
            await file.download_to_drive(file_path)  
    
            try:  
                duplicate = DuplicateExtractor(caption ,file_path)
                response = duplicate.extractor()
                
                await update.message.reply_text(response, parse_mode="HTML")
            except Exception as e: 
        
                await update.message.reply_text(  
                    f"❌ Error reading the file:\n<pre>{e}</pre>", parse_mode=ParseMode.HTML  
                )
                os.remove(file_path)
            
        else:
            await update.message.reply_text("❗ Please send a valid .txt file.")
        
