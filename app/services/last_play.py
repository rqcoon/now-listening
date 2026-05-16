import json, tempfile, os
from pathlib import Path

LAST_PLAYED_PATH = Path("app/data/last_played.json")


def load_last_played():
    if not LAST_PLAYED_PATH.exists():
        return None

    try:
        return json.loads(LAST_PLAYED_PATH.read_text())
    except json.JSONDecodeError:
        return None

def save_last_played(data):
    LAST_PLAYED_PATH.parent.mkdir(parents=True, exist_ok=True)

    tmp_fd, tmp_path = tempfile.mkstemp(dir=LAST_PLAYED_PATH.parent)

    with os.fdopen(tmp_fd, "w") as f:
        f.write(json.dumps(data))

    os.replace(tmp_path, LAST_PLAYED_PATH)