from collections import Counter
import os
import re

def normalize_number(number: str) -> str:
    return re.sub(r'\D', '', number.strip())
    
class DuplicateExtractor:
    
    def __init__(self, caption, file_path) -> None:
        self.caption = caption
        self.file_path = file_path
        self.seen_numbers = set()  
        self.duplicate_number = set()  
        self.data = []  
        self.testing_number = []  
        self.duplicates_found = False
        
        
    def texting_number_hand(self) -> None:
        if self.caption:  
            f = [self.caption]  
            fixed_number = [number.replace('\n' , ",") for number in f]  
            e = list(map(int , fixed_number[0].split(",")))
            test_num = [fo]
    
    def numbers_file_handler(self) -> list[int]:
        with open(self.file_path, "r", encoding="utf-8") as f:  
            phone_number_list = [normalize_number(line) for line in f if line.strip()]
            return phone_number_list
    
    def duplicate_filter(self) -> None:
        number_list = self.numbers_file_handler()
        for phone_numbers in number_list:  
            if phone_numbers in self.seen_numbers:  
                self.duplicate_number.add(phone_numbers)  
                self.duplicates_found = True  
            else:    
                self.seen_numbers.add(phone_numbers)
    
    def extractor(self) -> str:
        
        number_list = self.numbers_file_handler()
        count = dict(Counter(number_list)) 
        self.duplicate_filter()
        
        if self.duplicates_found:  
            dup_list = list(self.duplicate_number)
            dup_line = [ind for i, value in enumerate(dup_list) for ind, val in enumerate(number_list) if dup_list[i] == val] 
            print(dup_list)
            duplicate = chr(10).join(f'{number} appeared {  
            count[str(number)]} times' for number in self.duplicate_number)  
            
                    
            message = (  
               f"<b>Phone-number Length:</b>\n<pre>{len(number_list)}</pre>"  
               f"<b>Duplicate number found:</b>\n<pre>{duplicate}</pre>\n"  
               f"<b>Line number:</b> <pre>{dup_line}</pre>\n"  
            )  
            return message
            os.remove(self.file_path)
        else:  
            return "✅ No duplicate numbers found."
            os.remove(self.file_path)
