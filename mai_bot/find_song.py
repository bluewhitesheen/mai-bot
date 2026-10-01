import json
from pathlib import Path
from typing import AbstractSet, Optional

from mai_bot.util import get_level, is_intl, is_jp, is_utage, abbr_difficulty, abbr_version, abbr_variety

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JSON = BASE_DIR / "data.json"


def find_difficulties(
    song,
    difficulty_filter: Optional[AbstractSet[str]] = None,
) -> str:
    dif_st = []
    dif_dx = []
    version_std = ""
    version_dx = ""
    for sheet in song.get("sheets", []):
        version = sheet.get("version", "")
        sheet_type = sheet.get("type", "")
        difficulty = abbr_difficulty(sheet)
        if difficulty_filter is not None and difficulty not in difficulty_filter:
            continue
        level = get_level(sheet)

        if sheet_type == "std":
            if not version_std:
                version_std = version
            dif_st.append(f"{difficulty} {level}")
        elif sheet_type == "dx":
            if not version_dx:
                version_dx = version
            dif_dx.append(f"{difficulty} {level}")

    dif_results = []
    if dif_st:
        dif_st = dif_st[::-1]
        dif_results.append(f"ST({abbr_version(version_std)}): " + " / ".join(dif_st))
    if dif_dx:
        dif_dx = dif_dx[::-1]
        dif_results.append(f"DX({abbr_version(version_dx)}): " + " / ".join(dif_dx))

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


    for song in data.get("songs", []):
        song_id = song.get("songId", "")
        song_variety = song.get("category", "")
        if keyword_lower in song_id.lower() and not is_utage(song):
            difficulties = find_difficulties(song, difficulty_filter=difficulty_filter)
            if difficulty_filter is not None and difficulties == "none":
                continue
            if is_intl(song):
                matches.append((song_id, song_variety, difficulties, 0))
            elif is_jp(song):
                matches.append((song_id, song_variety, difficulties, 1))

    def sort_key(song_id: str) -> tuple[int, str]:
        sid = song_id.lower()
        return (0 if sid.startswith(keyword_lower) else 1, sid)

    # item list: [song_id, song_variety, difficulties, 0=intl/1=jp]
    matches.sort(key=lambda item: (sort_key(item[0]), item[3]))

    max_results = 5
    results = []

    for song_id, song_variety, difficulties, region_type in matches[:max_results]:
        if region_type == 0:
            results.append(f"{song_id} ({abbr_variety(song_variety)})\n{difficulties}")
        elif region_type == 1:
            results.append(f"[JAPAN_ONLY] {song_id} ({abbr_variety(song_variety)})\n{difficulties}")

    if len(matches) > max_results:
        results.append("符合條件之歌曲數量較多，僅顯示前五筆結果")

    if not results:
        return ["No matches found"]
    return results
