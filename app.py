# VSCodeターミナルで実行:
# pip install streamlit pandas plotly
# streamlit run app.py

import json
import math
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from pokemon_data import POKEMON_DB


st.set_page_config(page_title="ポケモン構築サポーター", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
:root {
  --bg: #0b0f1a;
  --panel: rgba(11, 18, 32, 0.72);
  --panel-border: rgba(0, 212, 255, 0.18);
  --accent: #00d4ff;
  --text: #e6f1ff;
  --muted: #94a3b8;
}

body { background: var(--bg); color: var(--text); }
.main { padding-top: 0.5rem; }
section[data-testid="stSidebar"] { background: #0a0e17; }

h1, h2, h3, h4, h5 { color: var(--text); }

.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  margin: 0.75rem 0;
}

.card {
  position: relative;
  padding: 0.9rem 1rem;
  border-radius: 16px;
  background: var(--panel);
  border: 1px solid var(--panel-border);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(6px);
  margin-bottom: 0.9rem;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 212, 255, 0.16);
  border-color: rgba(0, 212, 255, 0.5);
}

.card-title {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.card-meta {
  color: var(--muted);
  font-size: 0.9rem;
}

.card-image {
  width: 96px;
  height: 96px;
  border-radius: 12px;
  background: rgba(0, 212, 255, 0.06);
  border: 1px solid rgba(0, 212, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-image img {
  width: 92px;
  height: 92px;
  object-fit: contain;
}

.type-watermark {
  position: absolute;
  right: 12px;
  bottom: 6px;
  font-size: 3rem;
  opacity: 0.06;
}

.badge {
  display: inline-block;
  padding: 0.18rem 0.55rem;
  border-radius: 999px;
  color: #0b0f1a;
  font-size: 0.78rem;
  font-weight: 700;
  margin-right: 0.25rem;
  box-shadow: inset 0 -2px 0 rgba(0,0,0,0.12);
}

div[data-testid="stSelectbox"] > div, div[data-testid="stMultiSelect"] > div {
  font-size: 1.05rem;
}

div.stButton > button {
  font-size: 1.05rem;
  padding: 0.75rem 1.1rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 212, 255, 0.4);
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.18), rgba(0, 212, 255, 0.06));
  color: var(--text);
}
</style>
""",
    unsafe_allow_html=True,
)

TYPES = [
    "ノーマル",
    "ほのお",
    "みず",
    "でんき",
    "くさ",
    "こおり",
    "かくとう",
    "どく",
    "じめん",
    "ひこう",
    "エスパー",
    "むし",
    "いわ",
    "ゴースト",
    "ドラゴン",
    "あく",
    "はがね",
    "フェアリー",
]

TYPE_CHART = {
    "ノーマル": {"いわ": 0.5, "ゴースト": 0, "はがね": 0.5},
    "ほのお": {"ほのお": 0.5, "みず": 0.5, "くさ": 2, "こおり": 2, "むし": 2, "いわ": 0.5, "ドラゴン": 0.5, "はがね": 2},
    "みず": {"ほのお": 2, "みず": 0.5, "くさ": 0.5, "じめん": 2, "いわ": 2, "ドラゴン": 0.5},
    "でんき": {"みず": 2, "でんき": 0.5, "くさ": 0.5, "じめん": 0, "ひこう": 2, "ドラゴン": 0.5},
    "くさ": {"ほのお": 0.5, "みず": 2, "くさ": 0.5, "どく": 0.5, "じめん": 2, "ひこう": 0.5, "むし": 0.5, "いわ": 2, "ドラゴン": 0.5, "はがね": 0.5},
    "こおり": {"ほのお": 0.5, "みず": 0.5, "くさ": 2, "こおり": 0.5, "じめん": 2, "ひこう": 2, "ドラゴン": 2, "はがね": 0.5},
    "かくとう": {"ノーマル": 2, "こおり": 2, "どく": 0.5, "ひこう": 0.5, "エスパー": 0.5, "むし": 0.5, "いわ": 2, "ゴースト": 0, "あく": 2, "はがね": 2, "フェアリー": 0.5},
    "どく": {"くさ": 2, "どく": 0.5, "じめん": 0.5, "いわ": 0.5, "ゴースト": 0.5, "はがね": 0, "フェアリー": 2},
    "じめん": {"ほのお": 2, "でんき": 2, "くさ": 0.5, "どく": 2, "ひこう": 0, "むし": 0.5, "いわ": 2, "はがね": 2},
    "ひこう": {"でんき": 0.5, "くさ": 2, "かくとう": 2, "むし": 2, "いわ": 0.5, "はがね": 0.5},
    "エスパー": {"かくとう": 2, "どく": 2, "エスパー": 0.5, "あく": 0, "はがね": 0.5},
    "むし": {"ほのお": 0.5, "くさ": 2, "かくとう": 0.5, "どく": 0.5, "ひこう": 0.5, "エスパー": 2, "ゴースト": 0.5, "あく": 2, "はがね": 0.5, "フェアリー": 0.5},
    "いわ": {"ほのお": 2, "こおり": 2, "かくとう": 0.5, "じめん": 0.5, "ひこう": 2, "むし": 2, "はがね": 0.5},
    "ゴースト": {"ノーマル": 0, "エスパー": 2, "ゴースト": 2, "あく": 0.5},
    "ドラゴン": {"ドラゴン": 2, "はがね": 0.5, "フェアリー": 0},
    "あく": {"かくとう": 0.5, "エスパー": 2, "ゴースト": 2, "あく": 0.5, "フェアリー": 0.5},
    "はがね": {"ほのお": 0.5, "みず": 0.5, "でんき": 0.5, "こおり": 2, "いわ": 2, "はがね": 0.5, "フェアリー": 2},
    "フェアリー": {"ほのお": 0.5, "かくとう": 2, "どく": 0.5, "ドラゴン": 2, "あく": 2, "はがね": 0.5},
}

TYPE_COLORS = {
    "ノーマル": "#d1d5db",
    "ほのお": "#ff6b4a",
    "みず": "#3aa5ff",
    "でんき": "#ffd13b",
    "くさ": "#4ee08f",
    "こおり": "#6ae6ff",
    "かくとう": "#ff4d6d",
    "どく": "#c084fc",
    "じめん": "#ffb86b",
    "ひこう": "#7aa2ff",
    "エスパー": "#ff7ab6",
    "むし": "#a5e635",
    "いわ": "#e0c087",
    "ゴースト": "#7c6cff",
    "ドラゴン": "#3d7bff",
    "あく": "#8b8f9b",
    "はがね": "#7fd1d9",
    "フェアリー": "#ff9de2",
}

TYPE_EMOJI = {
    "ノーマル": "⚪",
    "ほのお": "🔥",
    "みず": "💧",
    "でんき": "⚡",
    "くさ": "🌿",
    "こおり": "❄️",
    "かくとう": "🥊",
    "どく": "☠️",
    "じめん": "🌎",
    "ひこう": "🪽",
    "エスパー": "🔮",
    "むし": "🐛",
    "いわ": "🪨",
    "ゴースト": "👻",
    "ドラゴン": "🐉",
    "あく": "🌑",
    "はがね": "⚙️",
    "フェアリー": "✨",
}

META_THREATS = {
    "高速ドラゴン全般": ["対ドラゴン", "フェアリー", "はがね"],
    "受けループ": ["対受け", "崩し"],
    "積みアタッカー": ["積み対策", "切り返し"],
    "雨パーティ": ["対水", "電気", "くさ"],
    "鋼受け": ["対鋼", "ほのお", "かくとう"],
}

CONCEPTS = {
    "対面構築": "単体性能を重視し、出し負けが少ない補完を優先。",
    "サイクル構築": "相性補完を最重視し、クッション役で回す。",
    "展開構築": "起点作成役と積みエースをセットで採用。",
}

ROLE_TARGETS = {
    "エース": 1,
    "クッション": 1,
    "スイーパー": 1,
}

META_TOP_POKEMON = {
    "ハバタクカミ": ["ゴースト", "フェアリー"],
    "カイリュー": ["ドラゴン", "ひこう"],
    "パオジアン": ["あく", "こおり"],
    "サーフゴー": ["ゴースト", "はがね"],
    "ウーラオス(れんげき)": ["かくとう", "みず"],
    "テツノツツミ": ["こおり", "みず"],
    "イーユイ": ["ほのお", "あく"],
}

META_COMBOS = [
    {"name": "ハバタクカミ＋イーユイ", "members": ["ハバタクカミ", "イーユイ"]},
    {"name": "カイリュー＋サーフゴー", "members": ["カイリュー", "サーフゴー"]},
]

SETUP_MOVES = {"ステルスロック", "あくび", "キノコのほうし", "おにび", "トリックルーム"}
BOOST_MOVES = {"つるぎのまい", "りゅうのまい", "ちょうのまい", "わるだくみ", "はらだいこ"}

PRIORITY_MOVES = {"しんそく", "かげうち", "アクアジェット", "ふいうち", "でんこうせっか", "マッハパンチ"}
ACTION_GUARANTEE_ITEMS = {"きあいのタスキ"}
ACTION_GUARANTEE_ABILITIES = {
    "マルチスケイル",
    "ばけのかわ",
    "がんじょう",
    "multiscale",
    "disguise",
    "sturdy",
}

SPEED_TARGET_BASES = {
    "最速135族": 135,
    "最速142族": 142,
    "最速123族": 123,
    "最速110族": 110,
}

NATURE_EFFECTS = {
    "ようき": {"up": "S", "down": "C"},
    "おくびょう": {"up": "S", "down": "A"},
    "いじっぱり": {"up": "A", "down": "C"},
    "ひかえめ": {"up": "C", "down": "A"},
    "ずぶとい": {"up": "B", "down": "A"},
    "わんぱく": {"up": "B", "down": "C"},
    "おだやか": {"up": "D", "down": "A"},
    "しんちょう": {"up": "D", "down": "C"},
    "ゆうかん": {"up": "A", "down": "S"},
}

MASTER_JSON_PATH = Path(__file__).with_name("pokemon_master.json")
SAVED_TEAMS_PATH = Path(__file__).with_name("saved_teams.json")
BATTLE_LOGS_PATH = Path(__file__).with_name("battle_logs.json")


@st.cache_data(show_spinner=False)
def load_pokemon_db() -> dict:
    if MASTER_JSON_PATH.exists():
        with MASTER_JSON_PATH.open("r", encoding="utf-8") as f:
            db = json.load(f)
    else:
        db = POKEMON_DB
    for info in db.values():
        info.setdefault("new_mechanic_compatibility", False)
    return db


def load_json_list(path: Path) -> list:
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_json_list(path: Path, data: list) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@st.cache_data(show_spinner=False)
def filter_pokemon_names(db: dict, query: str) -> list[str]:
    if not query:
        return list(db.keys())
    query = query.strip()
    return [name for name in db.keys() if query in name]


def get_types(info: dict) -> list[str]:
    types = [info["type1"]]
    if info.get("type2"):
        types.append(info["type2"])
    return types


def get_all_moves(info: dict) -> list[str]:
    moves = info.get("moves", {})
    return moves.get("physical", []) + moves.get("special", []) + moves.get("status", [])


def primary_ability(info: dict) -> str:
    return info.get("abilities", ["未設定"])[0]


def has_new_mechanic(info: dict) -> bool:
    return bool(info.get("new_mechanic_compatibility", False))


def nature_modifier(stat_key: str, nature: str | None) -> float:
    if not nature or nature == "無補正":
        return 1.0
    effect = NATURE_EFFECTS.get(nature)
    if not effect:
        return 1.0
    if stat_key == effect["up"]:
        return 1.1
    if stat_key == effect["down"]:
        return 0.9
    return 1.0


def calc_stat_max(base_stat: int, nature: str | None, stat_key: str) -> int:
    raw = base_stat * 2 + 31 + 63 + 5
    return int(raw * nature_modifier(stat_key, nature))


def type_multiplier(attack_type: str, defend_types: list[str]) -> float:
    mult = 1.0
    for d in defend_types:
        mult *= TYPE_CHART.get(attack_type, {}).get(d, 1.0)
    return mult


def calc_defensive_table(team: list[str]) -> pd.DataFrame:
    rows = []
    for t in TYPES:
        weak = 0
        resist = 0
        immune = 0
        quad = 0
        for p in team:
            m = type_multiplier(t, get_types(POKEMON_DB[p]))
            if m == 0:
                immune += 1
            elif m >= 2:
                weak += 1
                if m >= 4:
                    quad += 1
            elif m <= 0.5:
                resist += 1
        is_pierce = weak >= 2 and (resist + immune) == 0
        rows.append(
            {
                "攻撃タイプ": t,
                "弱点": weak,
                "4倍弱点": quad,
                "耐性": resist,
                "無効": immune,
                "一貫": "あり" if is_pierce else "",
            }
        )
    return pd.DataFrame(rows)


def calc_offensive_table(team: list[str]) -> pd.DataFrame:
    rows = []
    for t in TYPES:
        strong = 0
        weak = 0
        for p in team:
            atk_types = get_types(POKEMON_DB[p])
            for atk in atk_types:
                m = type_multiplier(atk, [t])
                if m >= 2:
                    strong += 1
                elif m <= 0.5:
                    weak += 1
        rows.append({"相手タイプ": t, "有利打点数": strong, "不利打点数": weak})
    return pd.DataFrame(rows)


def has_priority_move(info: dict) -> bool:
    return any(m in PRIORITY_MOVES for m in get_all_moves(info))


def has_action_guarantee(info: dict) -> bool:
    items = info.get("recommended_items", [])
    abilities = info.get("abilities", [])
    if any(item in ACTION_GUARANTEE_ITEMS for item in items):
        return True
    return any(any(key in ab for key in ACTION_GUARANTEE_ABILITIES) for ab in abilities)


def is_setup_role(info: dict) -> bool:
    return any(m in SETUP_MOVES for m in get_all_moves(info)) or "ステロ" in info.get("meta_tags", [])


def is_setup_sweeper(info: dict) -> bool:
    return any(m in BOOST_MOVES for m in get_all_moves(info))


def infer_battle_roles(info: dict) -> set[str]:
    stats = info["stats"]
    roles = set()
    if max(stats["A"], stats["C"]) >= 120 or "エース" in info["role_labels"] or "ブレイカー" in info["role_labels"]:
        roles.add("エース")
    if stats["H"] >= 100 and (stats["B"] >= 100 or stats["D"] >= 100) or "クッション" in info["role_labels"] or "受け" in info["role_labels"]:
        roles.add("クッション")
    if stats["S"] >= 100 or "スイーパー" in info["role_labels"]:
        roles.add("スイーパー")
    return roles


def team_role_balance(team: list[str]) -> tuple[dict[str, int], list[str]]:
    counts = {k: 0 for k in ROLE_TARGETS}
    for name in team:
        info = POKEMON_DB[name]
        roles = infer_battle_roles(info)
        for r in info["role_labels"]:
            if r in counts:
                roles.add(r)
        for r in roles:
            if r in counts:
                counts[r] += 1
    missing = [r for r, need in ROLE_TARGETS.items() if counts[r] < need]
    return counts, missing


def has_super_effective(team: list[str], defend_types: list[str]) -> bool:
    for p in team:
        for atk in get_types(POKEMON_DB[p]):
            if type_multiplier(atk, defend_types) >= 2:
                return True
    return False


def has_resist(team: list[str], attack_type: str) -> bool:
    return any(type_multiplier(attack_type, get_types(POKEMON_DB[p])) <= 0.5 for p in team)


def render_type_badges(types: list[str]) -> str:
    return "".join(
        [
            f'<span class="badge" style="background:{TYPE_COLORS.get(t, "#00d4ff")}">{t}</span>'
            for t in types
        ]
    )


def recommended_tera(info: dict) -> list[str]:
    if info.get("tera_types"):
        return info["tera_types"]
    weakness_types = []
    for t in TYPES:
        if type_multiplier(t, get_types(info)) >= 2:
            weakness_types.append(t)
    if weakness_types:
        return weakness_types[:2]
    return get_types(info)


def get_image_url(info: dict) -> str:
    if info.get("image_url"):
        return info["image_url"]
    if info.get("sprite_url"):
        return info["sprite_url"]
    dex_id = info.get("dex_id") or info.get("id")
    if dex_id:
        return (
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"
            f"{dex_id}.png"
        )
    return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"


def build_speed_table(team: list[str], nature: str | None) -> pd.DataFrame:
    rows = []
    max_speed = max((calc_stat_max(POKEMON_DB[p]["stats"]["S"], nature, "S") for p in team), default=0)
    for p in team:
        s_base = POKEMON_DB[p]["stats"]["S"]
        s_actual = calc_stat_max(s_base, nature, "S")
        rows.append(
            {
                "ポケモン": p,
                "S種族値": s_base,
                "S最大実数": s_actual,
                "最速枠": "◎" if s_actual == max_speed else "",
            }
        )
    return pd.DataFrame(rows)


def speed_target_check(team: list[str], nature: str | None) -> dict[str, dict]:
    fastest = max((calc_stat_max(POKEMON_DB[p]["stats"]["S"], nature, "S") for p in team), default=0)
    results = {}
    for label, base in SPEED_TARGET_BASES.items():
        target = calc_stat_max(base, nature, "S")
        results[label] = {"target": target, "ok": fastest > target}
    return results


def export_showdown(team: list[str]) -> str:
    lines = []
    for name in team:
        info = POKEMON_DB[name]
        item = info["recommended_items"][0] if info["recommended_items"] else "もちもの未設定"
        lines.append(f"{name} @ {item}")
        lines.append(f"Ability: {primary_ability(info)}")
        tera = recommended_tera(info)
        if tera:
            lines.append(f"Tera Type: {tera[0]}")
        lines.append("EVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe")
        lines.append(f"{info['recommended_nature']} Nature")
        for move in get_all_moves(info)[:4]:
            lines.append(f"- {move}")
        lines.append("")
    return "\n".join(lines).strip()


def meta_warnings(team: list[str]) -> tuple[list[str], list[str]]:
    coverage_missing = []
    for name, types in META_TOP_POKEMON.items():
        if not has_super_effective(team, types):
            coverage_missing.append(name)

    combo_alerts = []
    for combo in META_COMBOS:
        lacks_coverage = all(
            not has_super_effective(team, META_TOP_POKEMON.get(m, [])) for m in combo["members"]
        )
        lacks_resist = all(
            all(not has_resist(team, t) for t in META_TOP_POKEMON.get(m, [])) for m in combo["members"]
        )
        if lacks_coverage and lacks_resist:
            combo_alerts.append(combo["name"])
    return coverage_missing, combo_alerts


def meta_pressure(team: list[str]) -> list[str]:
    warnings = []
    if not team:
        return warnings
    threshold = (len(team) + 1) // 2
    for name, types in META_TOP_POKEMON.items():
        weak_count = 0
        for p in team:
            defender_types = get_types(POKEMON_DB[p])
            if any(type_multiplier(t, defender_types) >= 2 for t in types):
                weak_count += 1
        if weak_count >= threshold:
            warnings.append(f"{name}が一貫しています")
    return warnings


def counter_candidates(team: list[str], target_types: list[str]) -> list[str]:
    scored = []
    for name, info in POKEMON_DB.items():
        if name in team:
            continue
        types = get_types(info)
        resist_score = 0
        for t in target_types:
            m = type_multiplier(t, types)
            if m == 0:
                resist_score += 3
            elif m <= 0.5:
                resist_score += 2
        offense_score = 2 if has_super_effective([name], target_types) else 0
        role_score = 1 if "クッション" in info["role_labels"] else 0
        total = resist_score + offense_score + role_score
        if total > 0:
            scored.append((total, name))
    scored.sort(reverse=True)
    return [name for _, name in scored[:6]]


def suggest_complements(team: list[str], roles_needed: list[str], meta_focus: list[str], concept: str) -> list[dict]:
    if not team:
        return []
    base_table = calc_defensive_table(team)
    weakness_types = set(base_table[base_table["弱点"] >= 2]["攻撃タイプ"].tolist())

    meta_keywords = set()
    for threat in meta_focus:
        meta_keywords.update(META_THREATS.get(threat, []))

    team_has_setup = any(is_setup_role(POKEMON_DB[p]) for p in team)
    team_has_sweeper = any(is_setup_sweeper(POKEMON_DB[p]) for p in team)

    scored = []
    for name, info in POKEMON_DB.items():
        if name in team:
            continue
        reasons = []
        cover_score = 0
        for wt in weakness_types:
            m = type_multiplier(wt, get_types(info))
            if m <= 0.5:
                cover_score += 2
            elif m == 0:
                cover_score += 3
        if cover_score > 0:
            reasons.append("弱点補完")

        role_score = 0
        for r in roles_needed:
            if r in info["role_labels"]:
                role_score += 2
        if role_score > 0:
            reasons.append("必要ロール")

        meta_score = 0
        for tag in info.get("meta_tags", []):
            if tag in meta_keywords:
                meta_score += 2
        if meta_score > 0:
            reasons.append("環境対策")

        concept_score = 0
        stats = info["stats"]
        if concept == "対面構築":
            stat_total = sum(stats.values())
            liability = sum(1 for t in TYPES if type_multiplier(t, get_types(info)) >= 2)
            concept_score += (stat_total // 60) + (stats["S"] // 20) - liability
            if has_priority_move(info):
                concept_score += 3
                reasons.append("先制技")
            if has_action_guarantee(info):
                concept_score += 3
                reasons.append("行動保証")
        elif concept == "サイクル構築":
            if "クッション" in info["role_labels"] or "受け" in info["role_labels"]:
                concept_score += 4
                reasons.append("受け性能")
            bulk = stats["H"] + stats["B"] + stats["D"]
            if bulk >= 320:
                concept_score += 3
                reasons.append("数値受け")
            concept_score += cover_score
        elif concept == "展開構築":
            if is_setup_role(info) and not team_has_setup:
                concept_score += 6
                reasons.append("起点作成")
            if is_setup_sweeper(info) and not team_has_sweeper:
                concept_score += 6
                reasons.append("積みエース")

        total = cover_score + role_score + meta_score + concept_score
        if total > 0:
            scored.append({"name": name, "score": total, "reasons": reasons})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:8]


def build_tactical_plans(team: list[str]) -> list[str]:
    plans = []
    setup_candidates = [p for p in team if is_setup_role(POKEMON_DB[p])]
    sweepers = [p for p in team if is_setup_sweeper(POKEMON_DB[p])]
    if setup_candidates and sweepers:
        lead = setup_candidates[0]
        finisher = sweepers[0]
        tera = recommended_tera(POKEMON_DB[finisher])
        plans.append(f"積みリレープラン: {lead}で起点を作り、{finisher}でテラスタル({tera[0]})して全抜き。")

    cushions = [p for p in team if "クッション" in POKEMON_DB[p]["role_labels"]]
    attackers = [p for p in team if "エース" in POKEMON_DB[p]["role_labels"] or "ブレイカー" in POKEMON_DB[p]["role_labels"]]
    if cushions and attackers:
        plans.append(f"対面操作サイクルプラン: {cushions[0]}をクッションにして有利対面を作り、サイクルで{attackers[0]}の火力を通す。")
    return plans


def offense_hint(info: dict) -> str:
    nature = info.get("recommended_nature", "無補正")
    atk = calc_stat_max(info["stats"]["A"], nature, "A")
    spa = calc_stat_max(info["stats"]["C"], nature, "C")
    main = max(atk, spa)
    if main >= 200:
        return "火力目安: H振りカイリューを2発圏内に入れやすい。"
    if main >= 170:
        return "火力目安: 耐久調整相手にも削りが通る目安。"
    return "火力目安: 受け寄りの相手にはサポートが欲しい。"


def synergy_score(a: str, b: str) -> int:
    types_a = get_types(POKEMON_DB[a])
    types_b = get_types(POKEMON_DB[b])
    score = 0
    for t in TYPES:
        ma = type_multiplier(t, types_a)
        mb = type_multiplier(t, types_b)
        if ma >= 2 and mb <= 0.5:
            score += 1
        if mb >= 2 and ma <= 0.5:
            score += 1
    return score


def build_synergy_network(team: list[str]) -> go.Figure:
    if len(team) < 2:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", height=380)
        return fig

    positions = {}
    for i, name in enumerate(team):
        angle = (2 * math.pi * i) / len(team)
        positions[name] = (1.2 * math.cos(angle), 1.2 * math.sin(angle))

    edge_x = []
    edge_y = []
    for i, a in enumerate(team):
        for b in team[i + 1 :]:
            score = synergy_score(a, b)
            if score > 0:
                x0, y0 = positions[a]
                x1, y1 = positions[b]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

    node_x = []
    node_y = []
    node_text = []
    for name in team:
        x, y = positions[name]
        node_x.append(x)
        node_y.append(y)
        node_text.append(name)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(color="#1f2937", width=2),
            hoverinfo="none",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="bottom center",
            marker=dict(size=20, color="#00d4ff", line=dict(width=1, color="#0b0f1a")),
            hoverinfo="text",
        )
    )
    fig.update_layout(
        template="plotly_dark",
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def table_to_plotly(df: pd.DataFrame, title: str) -> go.Figure:
    header_color = "#0b1220"
    cells_color = "#111827"
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=list(df.columns), fill_color=header_color, font=dict(color="#e5e7eb")),
                cells=dict(values=[df[col].tolist() for col in df.columns], fill_color=cells_color, font=dict(color="#e5e7eb")),
            )
        ]
    )
    fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(l=10, r=10, t=20, b=10),
        title=title,
    )
    return fig


def battle_log_summary(logs: list[dict]) -> list[tuple[str, int]]:
    counts = {}
    for log in logs:
        if log.get("result") == "負け":
            opponent = log.get("opponent_core", "")
            if opponent:
                counts[opponent] = counts.get(opponent, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


def build_personal_warning(logs: list[dict], team: list[str]) -> str | None:
    ranking = battle_log_summary(logs)
    if not ranking:
        return None
    top_name, count = ranking[0]
    if top_name not in META_TOP_POKEMON:
        return None
    counters = counter_candidates(team, META_TOP_POKEMON[top_name])
    if not counters:
        return f"戦績上、{top_name}が非常に重いため、受け出し可能な枠の追加を強く推奨します。"
    return f"戦績上、{top_name}が非常に重いため、{counters[0]}の採用を強く推奨します。"


st.title("ポケモン構築サポーター")
st.write("軸ポケモンを決め、補完枠や弱点をスマホで直感的にチェックできます。")

POKEMON_DB = load_pokemon_db()

if "saved_teams" not in st.session_state:
    st.session_state.saved_teams = load_json_list(SAVED_TEAMS_PATH)
if "battle_logs" not in st.session_state:
    st.session_state.battle_logs = load_json_list(BATTLE_LOGS_PATH)

with st.sidebar:
    st.header("構築の軸を選択")
    st.write("大量データ向けに検索バーを用意しました。")
    query_1 = st.text_input("検索 (軸ポケモン1)", "")
    names_1 = filter_pokemon_names(POKEMON_DB, query_1)
    core_1 = st.selectbox("軸ポケモン1", ["未選択"] + names_1, index=0)
    query_2 = st.text_input("検索 (軸ポケモン2)", "")
    names_2 = filter_pokemon_names(POKEMON_DB, query_2)
    core_2 = st.selectbox("軸ポケモン2 (任意)", ["未選択"] + names_2, index=0)
    st.header("構築コンセプト")
    concept = st.selectbox("コンセプト", list(CONCEPTS.keys()))
    st.header("役割の希望")
    roles_needed = st.multiselect(
        "必要な役割",
        ["エース", "クッション", "スイーパー", "起点作成", "サポート", "ブレイカー", "受け", "ストッパー", "サイクル", "トリックルーム"],
    )
    st.header("環境対策")
    meta_focus = st.multiselect("意識したい環境", list(META_THREATS.keys()))
    st.header("Sライン補正")
    speed_nature = st.selectbox("性格補正 (S)", ["無補正", "ようき", "おくびょう", "ゆうかん"])

    query_extra = st.text_input("検索 (追加メンバー)", "")
    extra_candidates = filter_pokemon_names(POKEMON_DB, query_extra)
    additional_members = st.multiselect(
        "追加メンバー (0〜4体)",
        [name for name in extra_candidates if name not in {core_1, core_2}],
    )

    st.header("構築の保存/呼び出し")
    team_name = st.text_input("保存名", "")
    team_memo = st.text_area("メモ", "", height=80)
    save_clicked = st.button("構築を保存")
    if save_clicked:
        team_data = {
            "name": team_name or f"未命名-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "members": [p for p in [core_1, core_2] if p != "未選択"] + additional_members,
            "concept": concept,
            "memo": team_memo,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
        }
        st.session_state.saved_teams.append(team_data)
        save_json_list(SAVED_TEAMS_PATH, st.session_state.saved_teams)
        st.success("構築を保存しました。")

    if st.session_state.saved_teams:
        names = [t["name"] for t in st.session_state.saved_teams]
        selected_team = st.selectbox("保存済み構築", ["未選択"] + names)
        load_clicked = st.button("構築を読み込む")
        if load_clicked and selected_team != "未選択":
            team_data = next(t for t in st.session_state.saved_teams if t["name"] == selected_team)
            st.session_state.loaded_team = team_data

team = [p for p in [core_1, core_2] if p != "未選択"] + additional_members
if "loaded_team" in st.session_state:
    team = st.session_state.loaded_team.get("members", [])
    concept = st.session_state.loaded_team.get("concept", concept)
    team_memo = st.session_state.loaded_team.get("memo", "")

if len(team) > 6:
    team = team[:6]


tabs = st.tabs(["構築", "相性表", "メタ対策", "Sライン", "戦績ログ"])

with tabs[0]:
    st.subheader("構築")
    st.write(CONCEPTS[concept])
    if not team:
        st.info("まずは軸ポケモンを1体選んでください。")
    else:
        st.write(f"現在のメンバー数: {len(team)} / 6")
        cols = st.columns(2)
        for idx, name in enumerate(team):
            info = POKEMON_DB[name]
            badges = render_type_badges(get_types(info))
            extra_badge = " <span class='badge' style='background:#00d4ff;'>NEW</span>" if has_new_mechanic(info) else ""
            watermark = TYPE_EMOJI.get(get_types(info)[0], "")
            image_url = get_image_url(info)
            card_html = (
                f'<div class="card">'
                f'<div class="type-watermark">{watermark}</div>'
                f'<div style="display:flex; gap:0.8rem; align-items:center;">'
                f'  <div class="card-image"><img src="{image_url}" alt="{name}"/></div>'
                f'  <div>'
                f'    <div class="card-title">{name} {extra_badge}</div>'
                f'    <div>{badges}</div>'
                f'    <div class="card-meta">役割: {", ".join(info["role_labels"])}</div>'
                f'    <div class="card-meta">特性: {", ".join(info["abilities"])}</div>'
                f'    <div class="card-meta">性格: {info["recommended_nature"]}</div>'
                f'  </div>'
                f'</div>'
                f'<div class="divider"></div>'
                f'<div class="card-meta">持ち物: {", ".join(info["recommended_items"])}</div>'
                f'<div class="card-meta">技: {", ".join(get_all_moves(info))}</div>'
                f'<div class="card-meta">テラ: {", ".join(recommended_tera(info))}</div>'
                f'<div class="card-meta">{offense_hint(info)}</div>'
                f'</div>'
            )
            with cols[idx % 2]:
                st.markdown(card_html, unsafe_allow_html=True)

        st.subheader("戦術プラン")
        plans = build_tactical_plans(team)
        if plans:
            for p in plans:
                st.write(f"- {p}")
        else:
            st.write("現時点では明確な勝ち筋が不足しています。起点作成やエースを追加してください。")

        st.subheader("補完候補")
        suggestions = suggest_complements(team, roles_needed, meta_focus, concept)
        if not suggestions:
            st.write("条件に合う候補が見つかりませんでした。")
        else:
            option_map = {f"{s['name']} (理由: {', '.join(s['reasons'])})": s for s in suggestions}
            selected = st.radio("候補を選択", list(option_map.keys()))
            info = POKEMON_DB[option_map[selected]["name"]]
            st.write(f"推奨テラスタイプ: {', '.join(recommended_tera(info))}")
            st.write(f"採用理由: {', '.join(option_map[selected]['reasons'])}")

        st.subheader("ロールバランスチェック")
        role_counts, missing_roles = team_role_balance(team)
        st.write(
            f"エース: {role_counts['エース']} / クッション: {role_counts['クッション']} / スイーパー: {role_counts['スイーパー']}"
        )
        if missing_roles:
            st.warning(f"不足している役割: {', '.join(missing_roles)}")
        else:
            st.success("主要ロールは揃っています。")

with tabs[1]:
    st.subheader("相性表")
    if not team:
        st.info("メンバーを選択すると相性表が表示されます。")
    else:
        def_table = calc_defensive_table(team)
        off_table = calc_offensive_table(team)
        st.plotly_chart(table_to_plotly(def_table, "防御相性"), use_container_width=True)
        st.plotly_chart(table_to_plotly(off_table, "攻撃相性"), use_container_width=True)
        st.subheader("相性ネットワーク")
        st.plotly_chart(build_synergy_network(team), use_container_width=True)

with tabs[2]:
    st.subheader("メタ対策")
    if not team:
        st.info("メンバーを選択するとメタ対策が表示されます。")
    else:
        st.write("環境上位への対策状況を自動チェックします。")
        warnings = meta_pressure(team)
        if warnings:
            for w in warnings:
                st.error(w)
        else:
            st.success("一貫するメタ対象は検出されませんでした。")

        missing_coverage, combo_alerts = meta_warnings(team)
        if missing_coverage:
            st.warning(f"上位ポケモンへの打点不足: {', '.join(missing_coverage)}")
        else:
            st.success("上位ポケモンへの打点は概ね確保されています。")
        if combo_alerts:
            st.error(f"対策必須の並び: {', '.join(combo_alerts)}")

        personal_warning = build_personal_warning(st.session_state.battle_logs, team)
        if personal_warning:
            st.warning(personal_warning)

        st.subheader("対策候補")
        for name, types in META_TOP_POKEMON.items():
            counters = counter_candidates(team, types)
            if counters:
                st.write(f"{name} 対策候補: {', '.join(counters)}")

with tabs[3]:
    st.subheader("Sライン")
    if not team:
        st.info("メンバーを選択するとSラインが表示されます。")
    else:
        speed_table = build_speed_table(team, speed_nature)
        st.plotly_chart(table_to_plotly(speed_table, "Sライン"), use_container_width=True)
        speed_checks = speed_target_check(team, speed_nature)
        for target, data in speed_checks.items():
            st.write(f"- {target} (目安 {data['target']}): {'抜ける' if data['ok'] else '抜けない'}")

        st.subheader("構築の書き出し")
        export_text = export_showdown(team)
        st.text_area("Showdown形式 (コピー用)", export_text, height=240)
        st.download_button("テキストをダウンロード", export_text, file_name="pokemon_team.txt")

        st.subheader("構築メモ")
        st.write("弱点が重なるタイプは要注意。コンセプトに合わせて役割を補完すると構築が安定します。")

with tabs[4]:
    st.subheader("戦績ログ")
    st.write("対戦直後に素早く記録できるよう、入力数を最小限にしています。")
    result = st.radio("勝敗", ["勝ち", "負け"], horizontal=True)
    opponent_core = st.selectbox("相手の軸ポケモン", ["未選択"] + list(POKEMON_DB.keys()))
    picked = st.multiselect("選出した自軍 (3体)", team)
    memo = st.text_area("メモ", "", height=90)
    log_clicked = st.button("戦績を記録")
    if log_clicked:
        log = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "result": result,
            "opponent_core": "" if opponent_core == "未選択" else opponent_core,
            "picked": picked[:3],
            "memo": memo,
            "team": team,
        }
        st.session_state.battle_logs.append(log)
        save_json_list(BATTLE_LOGS_PATH, st.session_state.battle_logs)
        st.success("戦績を記録しました。")

    if st.session_state.battle_logs:
        st.subheader("要注意ポケモンランキング")
        ranking = battle_log_summary(st.session_state.battle_logs)
        if ranking:
            for name, count in ranking[:10]:
                st.write(f"- {name}: {count}回")
        else:
            st.write("まだ負け試合の記録がありません。")

        st.subheader("戦績データの出力")
        df_logs = pd.DataFrame(st.session_state.battle_logs)
        csv_data = df_logs.to_csv(index=False)
        st.download_button("CSVをダウンロード", csv_data, file_name="battle_logs.csv")
