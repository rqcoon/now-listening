from fastapi import APIRouter, HTTPException
import requests, time
from app.services.spotify import get_access_token
from app.services.last_play import save_last_played, load_last_played

router = APIRouter()

def build_payload(item=None, is_playing=False, progress_ms=0):
    if not item:
        return {
            "is_playing": False,
            "track": None,
            "artist": None,
            "album": None,
            "spotify_url": None,
            "progress_ms": None,
            "duration_ms": None,
            "progress_percent": 0,
            "timestamp": int(time.time()),
        }

    duration_ms = item.get("duration_ms") or 0

    return {
        "is_playing": is_playing,
        "track": item.get("name"),
        "artist": ", ".join(a.get("name", "") for a in item.get("artists", [])) or None,
        "album": item.get("album", {}).get("name"),
        "spotify_url": item.get("external_urls", {}).get("spotify"),
        "progress_ms": progress_ms,
        "duration_ms": duration_ms,
        "progress_percent": round((progress_ms / duration_ms) * 100, 2) if duration_ms else 0,
        "timestamp": int(time.time()),
    }

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

        if last:
            return build_payload(
                item=last,
                is_playing=False,
                progress_ms=last.get("progress_ms", 0)
            )
        return build_payload()
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    
    data = response.json()
    item = data.get("item")
    progress_ms = data.get("progress_ms", 0)

    if not item:
        last = load_last_played()

        if last:
            return build_payload(
                item=last,
                is_playing=False,
                progress_ms=last.get("progress_ms", 0)
            )

        return build_payload()
    
    payload = build_payload(
        item=item,
        is_playing=data.get("is_playing", False),
        progress_ms=progress_ms
    )

    if payload["is_playing"]:
        save_last_played({
            "name": item.get("name"),
            "artists": item.get("artists"),
            "album": item.get("album"),
            "external_urls": item.get("external_urls"),
            "duration_ms": item.get("duration_ms"),
            "progress_ms": progress_ms
        })

    return payload