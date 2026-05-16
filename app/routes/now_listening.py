from fastapi import APIRouter, HTTPException
import requests
from app.services.spotify import get_access_token

router = APIRouter()

@router.get("/now-listening")
def now_listening():
    token = get_access_token()

    response = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code == 204:
        return {
            "is_playing": False
        }

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    data = response.json()

    item = data.get("item")

    return {
        "is_playing": data.get("is_playing"),
        "track": item["name"],
        "artist": ", ".join(a["name"] for a in item["artists"]),
        "album": item["album"]["name"],
        "spotify_url": item["external_urls"]["spotify"]
    }