import re
from Extractor.Bot.message_tracker.file_manager.sysfile_editor import FileManager

class RefinedTextHandler:
    def __init__(self, text: str, command: str, clear_command: str) -> str:
        self.text = text.lower()
        self.resolve_command = command
        self.clear_command = clear_command


    def crop_out_content(self) -> str:
        pattern = re.compile(
            r"user:\s*(?P<user>.*)\n\s*sid:\s*(?P<sid>.*)\n\s*phone:\s*(?P<phone>.*)\n\s*message:\s*(?P<message>.*?)(?:\n\s*image:|$)",
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
            sys_file = FileManager(None, self.text, self.resolve_command)
            sys_file.create_file()
            return sys_file.output_extracted_content()

        elif self.text == self.clear_command:
            sys_file = FileManager(None, None, None)
            sys_file.clear_file()

            