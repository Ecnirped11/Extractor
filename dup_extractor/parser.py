from collections import Counter
import re
import os

class NumberParser:

    def __init__(self, number_list, file_path) -> None:
        self.number_list = number_list
        self.validator_pattern =r'^(?:\+1\s?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}$|^1\d{10}$'
        self.area_code_pattern = r'^(?:\+?1)?[\s.-]*\(?(\d{3})\)?'
        self.file_path = file_path
    #helper give valid bool if number in list is USA number
    def validate_number_list(self) -> bool:
        for number in self.number_list:
            if re.match(self.validator_pattern, number):
                return True
            else:
                return False
    
    def area_code_extractor(self) -> list:
        extract_area_code = [
            match.group(1)
            for number in self.number_list if (match:= re.search(self.area_code_pattern, number))
        ]
        return extract_area_code
        
    def duplicate_area_code(self) -> list:
        area_codes = self.area_code_extractor()
        count = dict(Counter(area_codes))
        catched_area_code = [area_code 
            for area_code, number in count.items() if number == 1
        ]
        return catched_area_code
    
    def extract_testing_number(self) -> str:
        is_us_num = self.validate_number_list()
        catched_area_code = self.duplicate_area_code()
        if is_us_num:
            ultra_numbers = [
                number
                for number in self.number_list for area_code in catched_area_code 
                if number.startswith(area_code, 1) or number.startswith(area_code)
            ] 
            slice_numbers = ultra_numbers[:5]
            ultra_fetch_response = "\n".join(
                number for number in slice_numbers
            )
            return ultra_fetch_response           
        else:
            return "⚠️🌎 The numbers are not a valid U.S. number."
        # os.remove(self.file_path)