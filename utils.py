import hashlib


def get_digest(body):
    return hashlib.md5(str(body).encode()).hexdigest()