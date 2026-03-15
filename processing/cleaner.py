import re

def clean(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(r'\n',' ',text)

    text = re.sub(r'[^a-zA-Z0-9 ]','',text)

    text = re.sub(r'\s+',' ',text)

    return text