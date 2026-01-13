import json
import time
from typing import Any, Dict, List

import requests

BASE_URL = "https://pokeapi.co/api/v2"
OUTPUT_PATH = "pokemon_data.json"
REQUEST_SLEEP_SEC = 0.35


def fetch_json(url: str) -> Dict[str, Any]:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def select_major_moves(moves: List[Dict[str, Any]], limit: int = 8) -> List[str]:
    seen = set()
    picked: List[str] = []
    for entry in moves:
        move_name = entry["move"]["name"].replace("-", " ")
        if move_name in seen:
            continue
        seen.add(move_name)
        picked.append(move_name)
        if len(picked) >= limit:
            break
    return picked


def fetch_japanese_name(species_url: str) -> str:
    species = fetch_json(species_url)
    names = species.get("names", [])
    for entry in names:
        if entry["language"]["name"] == "ja-Hrkt":
            return entry["name"]
    for entry in names:
        if entry["language"]["name"] == "ja":
            return entry["name"]
    return ""


def extract_image_url(detail: Dict[str, Any]) -> str:
    sprites = detail.get("sprites", {})
    other = sprites.get("other", {})
    official = other.get("official-artwork", {})
    return official.get("front_default") or sprites.get("front_default") or ""


def convert_pokemon(detail: Dict[str, Any]) -> Dict[str, Any]:
    types = [t["type"]["name"] for t in detail["types"]]
    ability_entries = detail["abilities"]
    abilities = [a["ability"]["name"] for a in ability_entries if not a["is_hidden"]]
    hidden = next(
        (a["ability"]["name"] for a in ability_entries if a["is_hidden"]),
        "",
    )
    japanese_name = fetch_japanese_name(detail["species"]["url"])
    image_url = extract_image_url(detail)
    stats_map = {s["stat"]["name"]: s["base_stat"] for s in detail["stats"]}
    total = sum(stats_map.values())

    return {
        "id": detail["id"],
        "name": detail["name"],
        "japanese_name": japanese_name,
        "image_url": image_url,
        "type1": types[0] if types else "",
        "type2": types[1] if len(types) > 1 else "",
        "ability1": abilities[0] if len(abilities) > 0 else "",
        "ability2": abilities[1] if len(abilities) > 1 else "",
        "hidden_ability": hidden,
        "hp": stats_map.get("hp", 0),
        "atk": stats_map.get("attack", 0),
        "def": stats_map.get("defense", 0),
        "spa": stats_map.get("special-attack", 0),
        "spd": stats_map.get("special-defense", 0),
        "spe": stats_map.get("speed", 0),
        "total": total,
        "moves": select_major_moves(detail["moves"]),
    }


def main() -> None:
    print("Fetching pokemon list...")
    data = fetch_json(f"{BASE_URL}/pokemon?limit=2000")
    results = data.get("results", [])
    print(f"Found {len(results)} entries")

    all_pokemon: List[Dict[str, Any]] = []

    for idx, item in enumerate(results, start=1):
        detail = fetch_json(item["url"])
        all_pokemon.append(convert_pokemon(detail))
        if idx % 50 == 0:
            print(f"Fetched {idx} / {len(results)}")
        time.sleep(REQUEST_SLEEP_SEC)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_pokemon, f, ensure_ascii=False, indent=2)

    print(f"Saved: {OUTPUT_PATH} ({len(all_pokemon)} records)")


if __name__ == "__main__":
    main()
