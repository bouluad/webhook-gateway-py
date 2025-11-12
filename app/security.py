import hmac
import hashlib
from app.config import GITHUB_SECRET

def verify_signature(payload, signature):
    if not signature:
        return False
    mac = hmac.new(GITHUB_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature)
