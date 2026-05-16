import json, tempfile, os
from pathlib import Path

LAST_PLAYED_PATH = Path("app/data/last_played.json")


def load_last_played(data):
    LAST_PLAYED_PATH.parent.mkdir(parents=True, exist_ok=True)

    LAST_PLAYED_PATH.write_text(json.dumps(data))

def save_last_played(data):
    LAST_PLAYED_PATH.parent.mkdir(parents=True, exist_ok=True)

    tmp_fd, tmp_path = tempfile.mkstemp(dir=LAST_PLAYED_PATH.parent)

    with os.fdopen(tmp_fd, "w") as f:
        f.write(json.dumps(data))

    os.replace(tmp_path, LAST_PLAYED_PATH)