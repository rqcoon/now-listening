import time, requests

from app.core.token_store import load_tokens, save_tokens
from app.core.config import Config

def get_access_token():
    tokens = load_tokens()

    if not tokens:
        raise Exception("No spotify tokens found")
    
    if tokens["expires_at"] > time.time():
        return tokens["access_token"]
    
    response = requests.post(
        Config.TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
            "client_id": Config.SPOTIFY_CLIENT_ID,
            "client_secret": Config.SPOTIFY_CLIENT_SECRET
        }
    )

    if response.status_code != 200:
        raise Exception("Failed to refresh token")

    refreshed = response.json()

    refreshed["refresh_token"] = tokens["refresh_token"]

    save_tokens(refreshed)

    return refreshed["access_token"]