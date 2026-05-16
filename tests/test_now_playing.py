from fastapi.testclient import TestClient
from app.main import app

import app.routes.now_listening as nl

client = TestClient(app)

def test_now_playing_mock(mocker):

    mocker.patch(
        "app.routes.now_listening.get_access_token",
        return_value="fake-token"
    )

    mocker.patch(
        "requests.get",
        return_value=type("obj", (), {
            "status_code": 200,
            "json": lambda: {
                "is_playing": True,
                "item": {
                    "name": "Song",
                    "artists": [{"name": "Artist"}],
                    "album": {"name": "Album"},
                    "duration_ms": 200000,
                    "external_urls": {"spotify": "url"}
                },
                "progress_ms": 10000
            }
        })
    )

    res = client.get("/now-listening")

    assert res.status_code == 200
    assert "track" in res.json()