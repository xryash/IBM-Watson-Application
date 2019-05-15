import hashlib


def get_digest(body):
    return hashlib.md5(str(body).encode()).hexdigest()


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default
