import json
from pathlib import Path
from typing import AbstractSet, Optional

from mai_bot.util import get_level, is_intl, is_utage

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


# list all difficulties of this song

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


def find_songs_by_keyword(
    keyword: str,
    difficulty_filter: Optional[AbstractSet[str]] = None,
    json_path=DATA_JSON,
) -> list[str]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    matches = []
    keyword_lower = keyword.lower()

    def sort_key(song_id: str) -> tuple[int, str]:
        sid = song_id.lower()
        return (0 if sid.startswith(keyword_lower) else 1, sid)

    for song in data.get("songs", []):
        song_id = song.get("songId", "")
        difficulties = find_difficulties(song, difficulty_filter=difficulty_filter)
        if keyword_lower in song_id.lower() and is_intl(song) and not is_utage(song):
            if difficulty_filter is not None and difficulties == "none":
                continue
            matches.append((song_id, difficulties))

    matches.sort(key=lambda item: sort_key(item[0]))
    results = [f"{song_id}\n{difficulties}" for song_id, difficulties in matches[:5]]

    if not results:
        return ["No matches found"]
    return results
