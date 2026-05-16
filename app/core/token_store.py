import json, os, time
from pathlib import Path

TOKEN_PATH = Path("app/data/token.json")

def save_tokens(token_data: dict):
    expires_in = token_data.get("expires_in", 3600)

    payload = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token"),
        "expires_at": int(time.time()) + expires_in
    }

    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(json.dumps(payload))

    os.chmod(TOKEN_PATH, 0o600) #owner rw only

def load_tokens():

    if not TOKEN_PATH.exists():
        return None

    return json.loads(TOKEN_PATH.read_text())