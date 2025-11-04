import emoji

def text_filter(value) -> str:
    return emoji.replace_emoji(value, replace="")