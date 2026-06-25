import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JSON = BASE_DIR / "data.json"


def abbr_dif(sheet) -> str:
    d = ""
    match sheet.get("difficulty", ""):
        case "basic":
            d = "BAS"
        case "advanced":
            d = "ADV"
        case "expert":
            d = "EXP"
        case "master":
            d = "MAS"
        case "remaster":
            d = "Re:MAS"
        case _:
            d = "UNKNOWN"
    return d


def MasterChoujoukyuu(json_path: Path = DATA_JSON) -> list[str]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cjk_sheets = []
    for song in data.get("songs", []):
        songName = song.get("songId", "")
        for sheet in song.get("sheets", []):
            internalLevel = sheet.get("internalLevelValue", 0)
            if 14.5 <= internalLevel <= 14.9 and not sheet.get("type", "") == "utage":
                diff = abbr_dif(sheet)
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
