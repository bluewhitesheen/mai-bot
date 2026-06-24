import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JSON = BASE_DIR / "data.json"


# ?¾ä??°internal level å°±å? level

def get_level(sheet):
    level = sheet.get("internalLevelValue")
    if level is None:
        level = sheet.get("level", "")
    return str(level)


def abbr_dif(sheet):
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

def find_difficulties(song):
    dif_st = []
    dif_dx = []
    for sheet in song.get("sheets", []):
        sheet_type = sheet.get("type", "")
        difficulty = abbr_dif(sheet)
        level = get_level(sheet)

        if sheet_type == "std":
            dif_st.append(f"{difficulty}: {level}")
        elif sheet_type == "dx":
            dif_dx.append(f"{difficulty}: {level}")

    dif_results = []
    if dif_st:
        dif_results.append("ST : " + " / ".join(dif_st))
    if dif_dx:
        dif_results.append("DX : " + " / ".join(dif_dx))

    return "\n".join(dif_results) if dif_results else "none"


# ?ä»»ä?sheetä¸­ç? regions ??intl is true

def IsIntl(song) -> bool:
    for sheet in song.get("sheets", []):
        if sheet.get("regions", {}).get("intl") == True:
            return True
    return False


# ?‰typeä¸æ˜¯utage ?½ä?ç®—å®´è­?

def IsUtage(song) -> bool:
    for sheet in song.get("sheets", []):
        if not sheet.get("type", "") == "utage":
            return False
    return True



def find_songs_by_keyword(keyword: str, json_path=DATA_JSON) -> list:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for song in data.get("songs", []):
        song_id = song.get("songId", "")
        difficulties = find_difficulties(song)
        if keyword.lower() in song_id.lower() and IsIntl(song) and not IsUtage(song):
            results.append(f"{song_id}\n{difficulties}")
        if len(results) >= 20:
            break

    if not results:
        return ["No matches found"]
    return results
