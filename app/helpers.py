import hashlib


def generate_signature(data, secret_key):
    sign = ':'.join([str(data[key]) for key in sorted(data.keys())]) + secret_key
    return hashlib.sha256(sign.encode()).hexdigest()
