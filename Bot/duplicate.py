from collections import Counter
import os
import re
    
class DuplicateExtractor:
    
    def __init__(self, caption: str, file_path: str) -> None:
        self.caption = caption
        self.file_path = file_path
        self.seen_numbers = set()  
        self.duplicate_number = set()  
        self.data = []  
        self.testing_number = []  
        self.duplicates_found = False
        
    def normalize_number(self, number: str) -> str:
        return re.sub(r'\D', '', number.strip())
    
    def numbers_file_handler(self) -> list[int]:
        with open(self.file_path, "r", encoding="utf-8") as f:  
            phone_number_list = [self.normalize_number(line) for line in f if line.strip()]
            return phone_number_list
            
    def texting_number_hand(self, number_list: list[int]) -> str:
        if self.caption:  
            fixed_number = self.caption.replace(' ', ',')
            try:
                e = list(map(int, fixed_number.split(',')))
            except ValueError:
                return "Error: Caption contains non-numeric values."
    
            test_num = '\n'.join(
                f"{val} found at {[i + 1 for i, num in enumerate(number_list) if int(num) == val]}"
                for val in e
            )
            if test_num:
                return test_num
            else:
                return "Not found!"
            
    def duplicate_filter(self, number_list: list[int]) -> None:
        for phone_numbers in number_list:  
            if phone_numbers in self.seen_numbers:  
                self.duplicate_number.add(phone_numbers)  
                self.duplicates_found = True  
            else:    
                self.seen_numbers.add(phone_numbers)
    
    def extractor(self) -> str:
        number_list = self.numbers_file_handler()
        testing_num = self.texting_number_hand(number_list)
        count = dict(Counter(number_list)) 
        
        self.duplicate_filter(number_list)
        if self.duplicates_found or testing_num:  
            dup_list = list(self.duplicate_number)
            dup_line = '\n'.join(
                f"{val} found at {[i + 1 for i, v in enumerate(number_list) if v == val]}"
                for val in dup_list
            )
        
            duplicate = chr(10).join(
                f'{number} appeared {count[str(number)]} times' for number in self.duplicate_number
            )  
                    
            message = (
                f"<b>📞 PHONE NUMBER LENGTH: {len(number_list)}</b>\n\n"
                f"<b>⚠️ DUPLICATE NUMBER FOUND:</b>\n\n<pre>{duplicate}</pre>\n\n"
                f"<b>📄 LINE NUMBER:</b>\n\n<pre>{dup_line}</pre>\n\n"
                f"<b>🔍 FILTER NUMBER:</b>\n\n<code>{chr(10).join(str(num) for num in dup_list)}</code>\n\n"
                f"<b>💡 TESTING NUMBER:</b>\n\n<code>{testing_num}</code>"
            )
            return message
            os.remove(self.file_path)
        else:  
            return "✅ No duplicate numbers found."
            os.remove(self.file_path)
