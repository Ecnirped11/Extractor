import os
from collections import Counter
from cloud.firebase import SenderMailDatabaseManager
import json

class FileManager:

    def __init__(self, refined_text, command):
        self.expand_dir = os.path.expanduser("~")
        self.file_path = os.path.join(self.expand_dir,  "extracted_message.txt")
        self.file_content = refined_text
        self.data_list = []
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

    def user_mail_collector(self, check_last_index) -> None:
        if check_last_index["mail"] is None:
            data_manager = SenderMailDatabaseManager(None, check_last_index["username"])
            self.user_mail = data_manager.extract_user_mail()
        else:
            self.user_mail = check_last_index["mail"]

    def edit_duplicate_message(self,  content_list: list) -> str:
        data = f"[{content_list[0]}]"
        data_output = json.loads(data)
        check_last_index = data_output[len(data_output) - 1]

        self.user_mail_collector(check_last_index)
        
        for item in data_output:
            self.data_list.append(item["message"])
        find_repeated_message = dict(Counter(self.data_list))
        for key, value in find_repeated_message.items(): 
            if value > 1: 
                for element in data_output: 
                    for element_key , element_value in element.items(): 
                        if element_value == key and element["username"] == check_last_index["username"]: 
                            self.total_number += int(element["number_length"]) 
                            self.extracted_content = f"{check_last_index['username']}[{self.total_number}]\n\n[{self.user_mail}]\n\n{key}" 
                            self.duplicate_message_found = True
            elif not self.duplicate_message_found: 
                self.extracted_content = f"{check_last_index['username']}[{check_last_index['number_length']}]\n\n[{self.user_mail}]\n\n{key}"

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
    
    