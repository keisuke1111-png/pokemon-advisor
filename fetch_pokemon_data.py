import json
import time
from pathlib import Path

import requests


MASTER_JSON_PATH = Path(__file__).with_name("pokemon_master.json")
POKEAPI_BASE = "https://pokeapi.co/api/v2"

TYPE_MOVE_SETS = {
    "ほのお": {
        "physical": ["フレアドライブ"],
        "special": ["かえんほうしゃ"],
        "status": ["おにび"],
    },
    "みず": {
        "physical": ["アクアブレイク"],
        "special": ["ハイドロポンプ"],
        "status": ["あくび"],
    },
    "でんき": {
        "physical": ["ワイルドボルト"],
        "special": ["10まんボルト"],
        "status": ["でんじは"],
    },
    "くさ": {
        "physical": ["ウッドハンマー"],
        "special": ["ギガドレイン"],
        "status": ["やどりぎのタネ"],
    },
    "こおり": {
        "physical": ["つららおとし"],
        "special": ["れいとうビーム"],
        "status": ["こごえるかぜ"],
    },
    "かくとう": {
        "physical": ["インファイト"],
        "special": ["きあいだま"],
        "status": ["ビルドアップ"],
    },
    "どく": {
        "physical": ["どくづき"],
        "special": ["ヘドロばくだん"],
        "status": ["どくどく"],
    },
    "じめん": {
        "physical": ["じしん"],
        "special": ["だいちのちから"],
        "status": ["ステルスロック"],
    },
    "ひこう": {
        "physical": ["ブレイブバード"],
        "special": ["ぼうふう"],
        "status": ["はねやすめ"],
    },
    "エスパー": {
        "physical": ["サイコカッター"],
        "special": ["サイコキネシス"],
        "status": ["リフレクター"],
    },
    "むし": {
        "physical": ["とんぼがえり"],
        "special": ["むしのさざめき"],
        "status": ["ねばねばネット"],
    },
    "いわ": {
        "physical": ["ストーンエッジ"],
        "special": ["パワージェム"],
        "status": ["ステルスロック"],
    },
    "ゴースト": {
        "physical": ["シャドークロー"],
        "special": ["シャドーボール"],
        "status": ["おにび"],
    },
    "ドラゴン": {
        "physical": ["げきりん"],
        "special": ["りゅうせいぐん"],
        "status": ["りゅうのまい"],
    },
    "あく": {
        "physical": ["はたきおとす"],
        "special": ["あくのはどう"],
        "status": ["ちょうはつ"],
    },
    "はがね": {
        "physical": ["アイアンヘッド"],
        "special": ["ラスターカノン"],
        "status": ["てっぺき"],
    },
    "フェアリー": {
        "physical": ["じゃれつく"],
        "special": ["ムーンフォース"],
        "status": ["ひかりのかべ"],
    },
    "ノーマル": {
        "physical": ["すてみタックル"],
        "special": ["ハイパーボイス"],
        "status": ["あくび"],
    },
}

ROLE_ITEMS = {
    "アタッカー": ["いのちのたま", "こだわりハチマキ", "こだわりメガネ"],
    "クッション": ["たべのこし", "ゴツゴツメット"],
    "スイーパー": ["きあいのタスキ", "ブーストエナジー"],
}

NATURE_MAP = {
    "A": "いじっぱり",
    "C": "ひかえめ",
    "S": "ようき",
    "B": "わんぱく",
    "D": "おだやか",
}

STAT_KEYS = {"hp": "H", "attack": "A", "defense": "B", "special-attack": "C", "special-defense": "D", "speed": "S"}


def get_json(url: str) -> dict:
    res = requests.get(url, timeout=20)
    res.raise_for_status()
    return res.json()


def fetch_japanese_name(species_url: str) -> str:
    species = get_json(species_url)
    for entry in species.get("names", []):
        if entry["language"]["name"] == "ja-Hrkt":
            return entry["name"]
    return species.get("name", "Unknown")


def normalize_types(type_entries: list[dict]) -> list[str]:
    type_map = {
        "normal": "ノーマル",
        "fire": "ほのお",
        "water": "みず",
        "electric": "でんき",
        "grass": "くさ",
        "ice": "こおり",
        "fighting": "かくとう",
        "poison": "どく",
        "ground": "じめん",
        "flying": "ひこう",
        "psychic": "エスパー",
        "bug": "むし",
        "rock": "いわ",
        "ghost": "ゴースト",
        "dragon": "ドラゴン",
        "dark": "あく",
        "steel": "はがね",
        "fairy": "フェアリー",
    }
    ordered = sorted(type_entries, key=lambda x: x["slot"])
    return [type_map.get(t["type"]["name"], t["type"]["name"]) for t in ordered]


def build_moves(types: list[str]) -> dict:
    moves = {"physical": [], "special": [], "status": []}
    for t in types:
        preset = TYPE_MOVE_SETS.get(t, {})
        for cat in moves:
            moves[cat].extend(preset.get(cat, []))
    # 重複排除しつつ4枠前後に整える
    for cat in moves:
        uniq = []
        for m in moves[cat]:
            if m not in uniq:
                uniq.append(m)
        moves[cat] = uniq[:4]
    return moves


def guess_roles(stats: dict) -> list[str]:
    roles = []
    if stats["S"] >= 100 and max(stats["A"], stats["C"]) >= 100:
        roles.append("スイーパー")
    if max(stats["A"], stats["C"]) >= 110:
        roles.append("アタッカー")
    if stats["H"] >= 100 and (stats["B"] >= 100 or stats["D"] >= 100):
        roles.append("クッション")
    if not roles:
        roles.append("アタッカー")
    return roles


def decide_nature(stats: dict, roles: list[str]) -> str:
    if "スイーパー" in roles:
        return "ようき"
    top_stat = max(("A", "C", "S", "B", "D"), key=lambda k: stats[k])
    return NATURE_MAP.get(top_stat, "ようき")


def recommend_items(roles: list[str]) -> list[str]:
    items = []
    for role in roles:
        items.extend(ROLE_ITEMS.get(role, []))
    uniq = []
    for item in items:
        if item not in uniq:
            uniq.append(item)
    return uniq[:3] if uniq else ["たべのこし"]


def convert_pokemon_entry(entry: dict) -> dict:
    jp_name = fetch_japanese_name(entry["species"]["url"])
    types = normalize_types(entry["types"])
    stats = {STAT_KEYS[s["stat"]["name"]]: s["base_stat"] for s in entry["stats"]}
    abilities = []
    for a in entry["abilities"]:
        name = a["ability"]["name"]
        label = f"{name}(隠れ)" if a.get("is_hidden") else name
        abilities.append(label)

    roles = guess_roles(stats)
    nature = decide_nature(stats, roles)
    moves = build_moves(types)
    items = recommend_items(roles)

    return {
        "name": jp_name,
        "type1": types[0],
        "type2": types[1] if len(types) > 1 else None,
        "abilities": abilities or ["未設定"],
        "stats": stats,
        "recommended_nature": nature,
        "recommended_items": items,
        "moves": moves,
        "tera_types": types[:2],
        "role_labels": roles,
        "meta_tags": [],
        "is_core": False,
        "future_tags": [],
    }


def fetch_all_pokemon() -> dict:
    data = get_json(f"{POKEAPI_BASE}/pokemon?limit=2000")
    results = data.get("results", [])
    pokemon_db = {}
    for idx, item in enumerate(results, start=1):
        poke = get_json(item["url"])
        pokemon_db_item = convert_pokemon_entry(poke)
        pokemon_db[pokemon_db_item["name"]] = pokemon_db_item
        if idx % 50 == 0:
            time.sleep(0.2)
    return pokemon_db


def main() -> None:
    pokemon_db = fetch_all_pokemon()
    with MASTER_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(pokemon_db, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(pokemon_db)} entries to {MASTER_JSON_PATH}")


if __name__ == "__main__":
    main()
