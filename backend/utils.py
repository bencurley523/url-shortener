import string

CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits

def base62_encode(num) -> str:
    """Encodes a number using Base62 encoding."""
    if num == 0:
        return CHARS[0]
    encoding = ''
    while num > 0:
        num, remainder = divmod(num, 62)
        encoding = CHARS[remainder] + encoding
    return encoding