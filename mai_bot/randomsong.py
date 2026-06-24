import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JSON = BASE_DIR / "data.json"


def format_song(song):
    name = song.get("songId", "")
    artist = song.get("artist", "")
    version = song.get("version", "")
    return f"{name} - {artist} - {version}"


def random_song(json_path: Path = DATA_JSON) -> str:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    songs = []
    for song in data.get("songs", []):
        for sheet in song.get("sheets", []):
            if sheet.get("regions", {}).get("jp", "") is True:
                break
        song_info = format_song(song)
        songs.append(song_info)

    return random.choice(songs)
