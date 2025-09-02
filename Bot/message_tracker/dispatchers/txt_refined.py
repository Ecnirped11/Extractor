import re
from Extractor.Bot.message_tracker.file_manager.sysfile_editor import FileManager
from telegram.error import BadRequest

class RefinedTextHandler:
    def __init__(self, text: str, command: str, clear_command: str) -> str:
        self.text = text
        self.resolve_command = command
        self.clear_command = clear_command

    def crop_out_content(self) -> str:
        pattern = re.compile(
            r"USER:\s*(?P<user>.*)\n\s*SID:\s*(?P<sid>.*)\n\s*PHONE:\s*(?P<phone>.*)\n\s*Message:\s*(?P<message>.*?)(?:\n\s*Image:|$)",
            re.DOTALL
        )
        match = pattern.search(self.text)
        
        if match:
            extracted_content = {
                "length": match.group("sid").strip(),
                "username" : match.group("user").strip(),
                "message" : match.group("message").strip()
            }
            sys_file = FileManager(extracted_content, None, self.resolve_command)
            sys_file.create_file()
            
        elif self.text == self.resolve_command:
            try:
                sys_file = FileManager(None, self.text, self.resolve_command)
                sys_file.create_file()
                return sys_file.output_extracted_content()
            
            except BadRequest as e:
                return f"Error occurred: {e}"

        elif self.text == self.clear_command:
            sys_file = FileManager(None, None, None)
            sys_file.clear_file()

            