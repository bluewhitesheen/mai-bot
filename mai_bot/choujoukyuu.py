import json
import random
from pathlib import Path
from mai_bot.util import is_long, is_utage, abbr_difficulty

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JSON = BASE_DIR / "data.json"


def MasterChoujoukyuu(json_path: Path = DATA_JSON) -> list[str]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cjk_sheets = []
    for song in data.get("songs", []):
        if is_utage(song): continue

        songName = song.get("songId", "")
        if is_long(songName): continue

        for sheet in song.get("sheets", []):
            internalLevel = sheet.get("internalLevelValue", 0)
            if 14.5 <= internalLevel <= 14.9:
                diff = abbr_difficulty(sheet)
                level = str(internalLevel)
                entry = f"{songName} / {diff} ({level})"
                cjk_sheets.append(entry)

    fourSongs = []
    i = 0
    if not cjk_sheets:
        return []
    while i < 4:
        chosen = random.choice(cjk_sheets)
        fourSongs.append(chosen)
        i += 1

    return fourSongs
