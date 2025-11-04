import re
from message_tracker.file_manager.sysfile_editor import FileManager
from telegram import error
from utils import filter
import emoji
from cloud.firebase import SenderMailDatabaseManager

class RefinedTextHandler:

    def __init__(self, text: str) -> str:
        self.text = text
        self.pattern = re.compile(
            r"USER:\s*(?P<user>.*?)\n\s*(?:EMAIL:\s*(?P<email>.*?)\n\s*)?SID:\s*(?P<sid>.*)\n\s*PHONE:\s*(?P<phone>.*)\n\s*Message:\s*(?P<message>.*?)(?:\n\s*Image:|$)",
            re.DOTALL
        )
        self.sender_mails = SenderMailDatabaseManager(None, None)

    def dispatch_user_mail(self, extracted_content: dict, data: dict) -> dict:
        previous_data = self.sender_mails.check_existing_data()
        
        if extracted_content["email"] not in previous_data and extracted_content["email"] is not None:
            user_mail_dispatcher = SenderMailDatabaseManager(
                extracted_content["email"], extracted_content["username"]
            )
            user_mail_dispatcher.push_data_information()
        else:
            pass

    def text_match(self) -> bool:
        return  self.pattern.search(self.text)
    
    def crop_out_content(self) -> str:
        match = self.text_match()
        if match:
            extracted_content = {
                "length": match.group("sid").strip(),
                "username" : filter.text_filter(match.group("user").strip()),
                "message" : match.group("message").strip(),
                "email": (match.group("email") or "").strip() or None,
            }
            sys_file = FileManager(extracted_content, None)
            registered_user = sys_file.is_registered()
            sid_value = sys_file.valid_sid_value()

            if sid_value:
                if registered_user or not isinstance(extracted_content["email"], type(None)):
                    data = match.groupdict()
                    self.dispatch_user_mail(extracted_content, data)
                    sys_file.create_file()
                    return "<b>saved ✔️</b>"
                else:
                    username = extracted_content["username"]
                    return f"⚠️ Could\t'nt proceed the request @{username} is not registered"
            else:
                sid = extracted_content["length"]
                return f"⚠️ Invalid SID value [ {sid} ]"

            
    def btn_handler(self) -> str:
        match self.text:
            case "resolve":
                try:
                    sys_file = FileManager(None, self.text)
                    sys_file.create_file()
                    return sys_file.output_extracted_content()
                
                except error.BadRequest:
                    return f"An error occur: No data in the file to resolve"
            case _:
                pass