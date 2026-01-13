import json
import time
from typing import Any, Dict, List, Tuple

import requests

BASE_URL = "https://pokeapi.co/api/v2"
OUTPUT_PATH = "pokemon_data.json"
REQUEST_SLEEP_SEC = 0.35


def fetch_json(url: str) -> Dict[str, Any]:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


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


def fetch_japanese_label(url: str) -> str:
    data = fetch_json(url)
    names = data.get("names", [])
    for entry in names:
        if entry["language"]["name"] == "ja-Hrkt":
            return entry["name"]
    for entry in names:
        if entry["language"]["name"] == "ja":
            return entry["name"]
    return ""


def extract_types(detail: Dict[str, Any]) -> Tuple[str, str, str, str]:
    types = detail["types"]
    type1 = types[0]["type"]["name"] if types else ""
    type2 = types[1]["type"]["name"] if len(types) > 1 else ""
    type1_ja = fetch_japanese_label(types[0]["type"]["url"]) if types else ""
    type2_ja = fetch_japanese_label(types[1]["type"]["url"]) if len(types) > 1 else ""
    return type1, type2, type1_ja, type2_ja


def extract_abilities(detail: Dict[str, Any]) -> Tuple[str, str, str, str, str, str]:
    ability_entries = detail["abilities"]
    abilities = [a for a in ability_entries if not a["is_hidden"]]
    hidden_entry = next((a for a in ability_entries if a["is_hidden"]), None)
    ability1 = abilities[0]["ability"]["name"] if len(abilities) > 0 else ""
    ability2 = abilities[1]["ability"]["name"] if len(abilities) > 1 else ""
    hidden = hidden_entry["ability"]["name"] if hidden_entry else ""
    ability1_ja = (
        fetch_japanese_label(abilities[0]["ability"]["url"]) if len(abilities) > 0 else ""
    )
    ability2_ja = (
        fetch_japanese_label(abilities[1]["ability"]["url"]) if len(abilities) > 1 else ""
    )
    hidden_ja = fetch_japanese_label(hidden_entry["ability"]["url"]) if hidden_entry else ""
    return ability1, ability2, hidden, ability1_ja, ability2_ja, hidden_ja


def extract_image_url(detail: Dict[str, Any]) -> str:
    sprites = detail.get("sprites", {})
    other = sprites.get("other", {})
    official = other.get("official-artwork", {})
    return official.get("front_default") or sprites.get("front_default") or ""


def convert_pokemon(detail: Dict[str, Any]) -> Dict[str, Any]:
    type1, type2, type1_ja, type2_ja = extract_types(detail)
    ability1, ability2, hidden, ability1_ja, ability2_ja, hidden_ja = extract_abilities(
        detail
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
        "type1": type1,
        "type2": type2,
        "type1_ja": type1_ja,
        "type2_ja": type2_ja,
        "ability1": ability1,
        "ability2": ability2,
        "hidden_ability": hidden,
        "ability1_ja": ability1_ja,
        "ability2_ja": ability2_ja,
        "hidden_ability_ja": hidden_ja,
        "hp": stats_map.get("hp", 0),
        "atk": stats_map.get("attack", 0),
        "def": stats_map.get("defense", 0),
        "spa": stats_map.get("special-attack", 0),
        "spd": stats_map.get("special-defense", 0),
        "spe": stats_map.get("speed", 0),
        "total": total,
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
