import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JSON = BASE_DIR / "data.json"


def find_nd(keyword: str, json_path: Path = DATA_JSON) -> list[str]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    note_designers = []
    for song in data.get("songs", []):
        for sheet in song.get("sheets", []):
            nd = sheet.get("noteDesigner")
            if nd is None:
                continue
            if keyword.lower() in nd.lower() and nd not in note_designers:
                note_designers.append(nd)
        if len(note_designers) >= 50:
            break

    sorted_note_designers = sorted(note_designers)

    if len(note_designers) == 0:
        return ["No note designers found"]
    return sorted_note_designers
