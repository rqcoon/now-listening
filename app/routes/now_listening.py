from fastapi import APIRouter, HTTPException
import requests, time
from app.services.spotify import get_access_token
from app.services.last_play import save_last_played, load_last_played

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
        last = load_last_played()
        
        if not last:
            return {
                "is_playing": False,
                "was_playing": None
            }
        
        return {
            "is_playing": False,
            "was_playing": last
        }

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    data = response.json()

    item = data.get("item")

    if not item:
        last = load_last_played()
        return {
            "is_playing": False,
            "was_playing": last
        }
    
    progress_ms = data.get("progress_ms", 0)
    duration_ms = data.get("duration_ms", 0)

    payload =  {
        "is_playing": data.get("is_playing"),
        "track": item["name"],
        "artist": ", ".join(a["name"] for a in item["artists"]),
        "album": item["album"]["name"],
        "spotify_url": item["external_urls"]["spotify"],
        "progress_ms": progress_ms,
        "duration_ms": duration_ms,
        "progress_percent": round((progress_ms / duration_ms) * 100, 2) if duration_ms else 0,

        "timestamp": int(time.time())
    }

    save_last_played({
        "track": payload["track"],
        "artist": payload["artist"],
        "album": payload["album"],
        "spotify_url": payload["spotify_url"],
        "timestamp": payload["timestamp"]
    })

    return payload