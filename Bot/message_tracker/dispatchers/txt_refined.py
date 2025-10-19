import re
from Extractor.Bot.message_tracker.file_manager.sysfile_editor import FileManager
from telegram.error import BadRequest
from ...cloud.firebase import SenderMailDatabaseManager
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
        
        if not data["email"] is None and not extracted_content["email"] in previous_data:
            user_mail_dispatcher = SenderMailDatabaseManager(
                extracted_content["email"], extracted_content["username"]
            )
            user_mail_dispatcher.push_data_information()
        

    def crop_out_content(self) -> str:
        match = self.pattern.search(self.text)
        
        if match:
            extracted_content = {
                "length": match.group("sid").strip(),
                "username" : match.group("user").strip(),
                "message" : match.group("message").strip(),
                "email": (match.group("email") or "").strip() or None,
            }
            data = match.groupdict()
            self.dispatch_user_mail(extracted_content, data)
            sys_file = FileManager(extracted_content, None)
            sys_file.create_file()
        
        match self.text:
            case "resolve":
                try:
                    sys_file = FileManager(None, self.text)
                    sys_file.create_file()
                    return sys_file.output_extracted_content()
                
                except BadRequest as e:
                    return f"Error occurred: {e}"
            case "clear file":
                sys_file = FileManager(None, None, None)
                sys_file.clear_file()

    
            

            