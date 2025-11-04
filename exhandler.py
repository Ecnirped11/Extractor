import os
from telegram import Update, ReplyKeyboardMarkup
import time
from message_tracker.dispatchers.txt_refined import RefinedTextHandler
from telegram.constants import ParseMode
from telegram.error import TimedOut, BadRequest
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)
from utils import filter
from message_tracker.file_manager.sysfile_editor import FileManager
from dup_extractor.duplicate import DuplicateExtractor
from cloud.firebase import SenderMailDatabaseManager

class CheetahExtractor:

    def __init__(self, Acceess_token) -> None:   
        self.keyboard = [
            ["resolve", "clear file"],
            ["Check Total Mail Stored", "check user"]
        ]
        self.file_manager = FileManager(None, None)
        self.data_manager = SenderMailDatabaseManager(None, None)
        self.mark_up = ReplyKeyboardMarkup(
            self.keyboard, one_time_keyboard=False, resize_keyboard=True
        )
        self.application = ApplicationBuilder().token(Acceess_token).build()
        
        self.application.add_handler(CommandHandler("start", self.start_cmd))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.sending_number_file_handler))
        self.application.add_handler(MessageHandler(filters.TEXT, self.text_file_editor))
    

    def request_reply_mesesage(self, update: Update, message) -> str:
        return update.message.reply_text(message, parse_mode=ParseMode.HTML)
    
    async def start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        username = update.effective_user.username
        await update.message.reply_text(f'You are welcome @{username}.', reply_markup=self.mark_up)

    async def clear_user_data(self, update: Update, context) -> str:
        confirmation_auth = filter.text_filter(update.message.text)
        match confirmation_auth:
            case "Y":
                context.user_data["confirm"] = False
                self.file_manager.clear_file()
                return "✅ File cleared successfully."
            case "N":
                context.user_data["confirm"] = False
                return "✅ Request terminated"
            case _:
                return "⚠️invalid input"
    
    async def check_user_data(self, update: Update, context) -> str:
        user_name = filter.text_filter(update.message.text)
        maiil_database_manager = SenderMailDatabaseManager(None, user_name)
        context.user_data["is_exist"] = False
        return maiil_database_manager.is_exist()

    async def text_file_editor(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text

        if context.user_data.get("is_exist"):
            is_exist = await self.check_user_data(update, context)
            await self.request_reply_mesesage(update, is_exist)

        if context.user_data.get("confirm"):
            clear_data_res = await self.clear_user_data(update, context)
            await self.request_reply_mesesage(update, clear_data_res)

        try:
            if text:
                refined_text = RefinedTextHandler(text)
                match = refined_text.text_match()
                btn_action = refined_text.btn_handler()
                if match:
                    content = refined_text.crop_out_content()
                    await self.request_reply_mesesage(update, content)
                
            match text:
                case "resolve":
                    await self.request_reply_mesesage(update, btn_action)
                case "clear file":
                    context.user_data["confirm"] = True
                    await self.request_reply_mesesage(update, "Confirm your request Y[proceed] / N[cancel]")
                case "Check Total Mail Stored":
                    mail_length = self.data_manager.check_stored_mail_length()
                    await self.request_reply_mesesage(
                        update,
                        f"<b>Total user mail stored in database: <i>{mail_length}</i></b>"
                    )
                case "check user":
                    context.user_data["is_exist"] = True
                    await self.request_reply_mesesage(update, "Enter user the name")
                case _:
                    return ""
        except TimedOut:
            await update.message.reply_text("Error: unstable network..")
        except BadRequest:
            await self.request_reply_mesesage(update, "<b>An error occur due to Bad request</b>")


    async def sending_number_file_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        document = update.message.document
        caption = update.message.caption

        if document:
            if document.mime_type == "text/plain":
                os.makedirs("downloads", exist_ok=True)
            
                file = await context.bot.get_file(document.file_id)  
                file_path = f"downloads/{document.file_name}"  
                await file.download_to_drive(file_path)  
        
                try:  
                    duplicate = DuplicateExtractor(caption ,file_path)
                    response = duplicate.extractor()
                    
                    await self.request_reply_mesesage(update, response)
                except Exception as e: 
            
                    await self.request_reply_mesesage(  
                        update,
                        f"❌ Error reading the file:\n<pre>{e}</pre>" 
                    )
                    os.remove(file_path)
                
            else:
                await self.request_reply_mesesage(update, "❗ Please send a valid .txt file.")
            
    def run_application(self) -> None:
        # print("\nBot is starting..")
        self.application.run_polling()