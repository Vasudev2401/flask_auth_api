import secrets

def generate_verificaction_token():
    return secrets.token_urlsafe(32)