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

