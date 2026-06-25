import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JSON = BASE_DIR / "data.json"


def get_level(sheet) -> str:
    level = sheet.get("internalLevelValue")
    if level is None:
        level = sheet.get("level", "")
    return str(level)


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


def get_type(sheet) -> str:
    t = sheet.get("type", "")
    if t == "std":
        return "ST"
    elif t == "dx":
        return "DX"
    return "UNK"


def format_song(song_name, sheet, nd) -> str:
    st_dx = get_type(sheet)
    difficulty = abbr_dif(sheet)
    level = get_level(sheet)
    return f"{nd} - {song_name} - {st_dx}/{difficulty}/{level}"


def find_nds(keyword: str, json_path: Path = DATA_JSON) -> list[str]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    songs_info = []
    for song in data.get("songs", []):
        song_name = song.get("songId", "")
        for sheet in song.get("sheets", []):
            internalLevelValue = sheet.get("internalLevelValue", 0)
            if internalLevelValue <= 12:
                continue
            nd = sheet.get("noteDesigner")
            if nd is None:
                continue
            if keyword.lower() in nd.lower():
                song_info = format_song(song_name, sheet, nd)
                songs_info.append(song_info)
        if len(songs_info) >= 20:
            break

    if len(songs_info) == 0:
        return ["No songs found"]
    return sorted(songs_info)
