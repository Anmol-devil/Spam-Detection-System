import re 


def clean(text):
    text = text.lower()

    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    text = re.sub(r"\$+", " money ", text)

    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

import email

def extract_body(raw):
    try:
        msg = email.message_from_string(raw)

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(errors='ignore')
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                return payload.decode(errors='ignore')

    except:
        pass

    return raw 