from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
import requests
from requests.compat import urlencode
from app.core.config import Config
from app.core.token_store import save_tokens

router = APIRouter()

@router.get("/login")
def login():
    params = {
        "client_id": Config.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": Config.SPOTIFY_REDIRECT_URI,
        "scope": ' '.join(Config.SPOTIFY_SCOPES)
    }

    auth_url = ("https://accounts.spotify.com/authorize?" + urlencode(params))
    
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(code: str = None, error: str = None):

    if error:
        raise HTTPException(status_code=400, detail=error)

    if not code:
        raise HTTPException(status_code=422, detail="Missing code")

    response = requests.post(
        Config.TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Config.SPOTIFY_REDIRECT_URI,
            "client_id": Config.SPOTIFY_CLIENT_ID,
            "client_secret": Config.SPOTIFY_CLIENT_SECRET
        }
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    token_data = response.json()

    save_tokens(token_data)

    return {
        "status": "authenticated"
    }