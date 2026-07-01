def get_level(sheet) -> str:
    level = sheet.get("internalLevelValue")
    if level is None:
        level = sheet.get("level", "")
    return str(level)


def is_intl(song) -> bool:
    for sheet in song.get("sheets", []):
        if sheet.get("regions", {}).get("intl") == True:
            return True
    return False


def is_utage(song) -> bool:
    for sheet in song.get("sheets", []):
        if not sheet.get("type", "") == "utage":
            return False
    return True


def is_long(songName) -> bool:
    if songName == "Xaleid◆scopiX" or songName == "Ref:rain (for 7th Heaven)":
        return True
    return False

def abbr_difficulty(sheet) -> str:
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

def abbr_version(s) -> str:
    return s.replace("でらっくす", "DX").replace(" PLUS", "+")


def abbr_variety(s) -> str:
    mapping = {
        "POPS＆アニメ": "POPS＆ANIME",
        "niconico＆ボーカロイド": "niconico＆VOCALOID",
        "ゲーム＆バラエティ": "GAME＆VARIETY",
        "オンゲキ＆CHUNITHM": "オンゲキ＆CHUNITHM",
    }
    if s not in mapping: 
        return s
    return mapping.get(s, s)
