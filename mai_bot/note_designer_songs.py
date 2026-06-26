import json
from pathlib import Path
from typing import AbstractSet, Optional

from mai_bot.util import get_level

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


def find_difficulties(
    song,
    difficulty_filter: Optional[AbstractSet[str]] = None,
) -> str:
    dif_st = []
    dif_dx = []
    for sheet in song.get("sheets", []):
        sheet_type = sheet.get("type", "")
        difficulty = abbr_dif(sheet)
        if difficulty_filter is not None and difficulty not in difficulty_filter:
            continue
        level = get_level(sheet)

        if sheet_type == "std":
            dif_st.append(f"{difficulty} {level}")
        elif sheet_type == "dx":
            dif_dx.append(f"{difficulty} {level}")

    dif_results = []
    if dif_st:
        dif_st = dif_st[::-1]
        dif_results.append("ST : " + " / ".join(dif_st))
    if dif_dx:
        dif_dx = dif_dx[::-1]
        dif_results.append("DX : " + " / ".join(dif_dx))

    return "\n".join(dif_results) if dif_results else "none"


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
