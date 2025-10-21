import re

def normalize_number(par: str) -> str:
    return re.sub(r'\D', '', par.strip())