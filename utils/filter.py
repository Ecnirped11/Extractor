import emoji

def filter_emoji(value) -> str:
    return emoji.replace_emoji(value, replace="").strip()