import os
from collections import Counter
from cloud.firebase import SenderMailDatabaseManager
import json

class FileManager:

    def __init__(self, refined_text, command):
        self.expand_dir = os.path.expanduser("~")
        self.file_path = os.path.join(self.expand_dir,  "extracted_message.txt")
        self.file_content = refined_text
        self.message_list = []
        self.total_number = 0
        self.user_mail  = None
        self.duplicate_message_found = False
        self.command = command

        self.resolve_command = "resolve"
        self.extracted_content = ""

    def enpack_text(self) -> dict:
        try:
            text_enpacked = self.file_content
            if isinstance(text_enpacked, dict):
                message_content = {
                    "username": text_enpacked["username"],
                    "message": text_enpacked["message"],
                    "number_length": text_enpacked["length"],
                    "mail" : text_enpacked["email"]
                }
                return message_content
        except TypeError:
            pass

    def is_registered(self) -> bool:
        msg_collector = self.enpack_text()
        data_administrator = SenderMailDatabaseManager(None, msg_collector["username"])
        return data_administrator.is_registered()
        
    def user_mail_collector(self, last_entry) -> None:
        """Fetches user mail from database or uses existing mail if present."""
        if last_entry["mail"] is None:
            data_manager = SenderMailDatabaseManager(None, last_entry["username"])
            self.user_mail = data_manager.extract_user_mail()
        else:
            self.user_mail = last_entry["mail"]

    def edit_duplicate_message(self,  file_lines: list) -> str:
        data = f"[{file_lines[0]}]"
        parsed_data = json.loads(data)
        last_entry = parsed_data[len(parsed_data) - 1]
        self.user_mail_collector(last_entry)

        self.message_list = [msg["message"] for msg in parsed_data]
        check_duplicate_msg = dict(Counter(self.message_list))

        duplicates_messages = [key for key, value in check_duplicate_msg.items() if value > 1]
        self.duplicate_message_found = bool(last_entry["message"] in duplicates_messages)
        user_msg = last_entry["message"]

        if self.duplicate_message_found:
            last_index_of_duplicates_messages = duplicates_messages[len(duplicates_messages) - 1]
            for data in parsed_data:
                if last_index_of_duplicates_messages == data["message"]:
                    self.total_number += int(data["number_length"]) 
                    self.extracted_content = f"{last_entry['username']}[{self.total_number}]\n\n[{self.user_mail}]\n\n{user_msg}" 
        else:
            self.extracted_content = f"{last_entry['username']}[{last_entry['number_length']}]\n\n[{self.user_mail}]\n\n{user_msg}"
        
    def create_file(self) -> None:
        extracted_message = self.enpack_text()
        try:
            if self.command != self.resolve_command:
                with open(self.file_path, "a", encoding="utf-8") as file:
                    message = json.dumps(extracted_message) if os.stat(self.file_path).st_size == 0 else "," + json.dumps(extracted_message)
                    file.write(message)

            elif self.command == self.resolve_command:
                with open(self.file_path,  "r", encoding="utf-8") as initial_contents:
                    list_values = initial_contents.readlines()
                    self.edit_duplicate_message(list_values)
                    
        except Exception as error:
            pass

    def clear_file(self) -> None:
        with open(self.file_path, "w") as file:
            pass

    def output_extracted_content(self) -> str:
        return self.extracted_content
    
    