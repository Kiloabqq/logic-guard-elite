from urllib.parse import urlparse

def validate_url(url):
    if not url:
        return None
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
    return url.rstrip('/')

def validate_token(token):
    if not token:
        return None
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    parts = token.split('.')
    if len(parts) != 3:
        return None
    return token
