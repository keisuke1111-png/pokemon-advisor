import json
import math
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from constants import (
    ACTION_GUARANTEE_ABILITIES,
    ACTION_GUARANTEE_ITEMS,
    BOOST_MOVES,
    META_COMBOS,
    META_THREATS,
    META_TOP_POKEMON,
    META_TOP_RATIONALE,
    NATURE_EFFECTS,
    NO_SELECTION,
    PRIORITY_MOVES,
    ROLE_TARGETS,
    SETUP_MOVES,
    SPEED_TARGET_BASES,
    TEAM_SLOTS,
    TYPE_CHART,
    TYPE_COLORS,
    TYPES,
)
from pokemon_data import POKEMON_DB

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
    for idx, name in enumerate(db.keys(), start=1):
        info = db[name]
        if not info.get("dex_id") and not info.get("id"):
            info["dex_id"] = idx
        if not info.get("name"):
            info["name"] = name
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


def calc_defensive_table(team: list[str], db: dict) -> pd.DataFrame:
    rows = []
    for t in TYPES:
        weak = 0
        resist = 0
        immune = 0
        quad = 0
        for p in team:
            m = type_multiplier(t, get_types(db[p]))
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


def calc_offensive_table(team: list[str], db: dict) -> pd.DataFrame:
    rows = []
    for t in TYPES:
        strong = 0
        weak = 0
        for p in team:
            atk_types = get_types(db[p])
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


def team_role_balance(team: list[str], db: dict) -> tuple[dict[str, int], list[str]]:
    counts = {k: 0 for k in ROLE_TARGETS}
    for name in team:
        info = db[name]
        roles = infer_battle_roles(info)
        for r in info["role_labels"]:
            if r in counts:
                roles.add(r)
        for r in roles:
            if r in counts:
                counts[r] += 1
    missing = [r for r, need in ROLE_TARGETS.items() if counts[r] < need]
    return counts, missing


def has_super_effective(team: list[str], defend_types: list[str], db: dict) -> bool:
    for p in team:
        for atk in get_types(db[p]):
            if type_multiplier(atk, defend_types) >= 2:
                return True
    return False


def has_resist(team: list[str], attack_type: str, db: dict) -> bool:
    return any(type_multiplier(attack_type, get_types(db[p])) <= 0.5 for p in team)


def render_type_badges(types: list[str]) -> str:
    return "".join(
        [
            f'<span class="badge" style="background:{TYPE_COLORS.get(t, "#3B82F6")}">{t}</span>'
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
    dex_id = info.get("dex_id") or info.get("id")
    if dex_id:
        try:
            dex_id = int(str(dex_id).strip().lstrip("#"))
        except (TypeError, ValueError):
            dex_id = None
    if dex_id:
        return (
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"
            f"{dex_id}.png"
        )
    if info.get("image_url"):
        return info["image_url"]
    if info.get("sprite_url"):
        return info["sprite_url"]
    return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"


def get_type_css_class(info: dict) -> str:
    type_map = {
        "ノーマル": "card-normal",
        "ほのお": "card-fire",
        "みず": "card-water",
        "でんき": "card-electric",
        "くさ": "card-grass",
        "こおり": "card-ice",
        "かくとう": "card-fighting",
        "どく": "card-poison",
        "じめん": "card-ground",
        "ひこう": "card-flying",
        "エスパー": "card-psychic",
        "むし": "card-bug",
        "いわ": "card-rock",
        "ゴースト": "card-ghost",
        "ドラゴン": "card-dragon",
        "あく": "card-dark",
        "はがね": "card-steel",
        "フェアリー": "card-fairy",
    }
    primary = get_types(info)[0]
    return type_map.get(primary, "card-normal")


def detect_cores(team: list[str], db: dict) -> list[dict]:
    cores = []
    if not team:
        return cores
    type_to_members: dict[str, list[str]] = {t: [] for t in TYPES}
    for name in team:
        for t in get_types(db[name]):
            type_to_members[t].append(name)

    if type_to_members["ほのお"] and type_to_members["みず"] and type_to_members["くさ"]:
        cores.append(
            {
                "name": "炎・水・草コア",
                "members": [
                    type_to_members["ほのお"][0],
                    type_to_members["みず"][0],
                    type_to_members["くさ"][0],
                ],
            }
        )

    volt_users = [n for n in team if "ボルトチェンジ" in get_all_moves(db[n])]
    uturn_users = [n for n in team if "とんぼがえり" in get_all_moves(db[n])]
    if volt_users and uturn_users:
        cores.append(
            {
                "name": "ボルトン軸",
                "members": [volt_users[0], uturn_users[0]],
            }
        )
    return cores


def identify_sweepers(team: list[str], db: dict) -> list[str]:
    sweepers = []
    sweeper_abilities = {"かそく", "ビーストブースト", "じしんかじょう", "エナジーエンジン"}
    for name in team:
        info = db[name]
        stats = info["stats"]
        speed = stats["S"]
        power = max(stats["A"], stats["C"])
        abilities = set(info.get("abilities", []))
        has_boost = any(m in BOOST_MOVES for m in get_all_moves(info))
        if speed >= 110 and power >= 115:
            sweepers.append(name)
        elif has_boost and speed >= 90 and power >= 110:
            sweepers.append(name)
        elif abilities & sweeper_abilities and speed >= 90:
            sweepers.append(name)
    return sweepers


def sweep_support_status(team: list[str], db: dict) -> dict:
    sweepers = identify_sweepers(team, db)
    has_setup = any(is_setup_role(db[p]) for p in team)
    return {"sweepers": sweepers, "has_setup": has_setup}


def detect_critical_vulnerabilities(team: list[str], db: dict) -> list[dict]:
    critical = []
    for name, types in META_TOP_POKEMON.items():
        weak_count = 0
        total_damage = 0.0
        for p in team:
            mults = [type_multiplier(t, get_types(db[p])) for t in types]
            total_damage += max(mults)
            if any(m >= 2 for m in mults):
                weak_count += 1
        if weak_count >= 3:
            critical.append(
                {
                    "name": name,
                    "types": types,
                    "weak_count": weak_count,
                    "damage": round(total_damage, 2),
                }
            )
    return critical


def calculate_balance_score(team: list[str], db: dict) -> dict:
    score = 100
    strengths = []
    weaknesses = []

    if not team:
        return {"score": 0, "strengths": [], "weaknesses": ["未選択"], "cores": []}

    role_counts, missing_roles = team_role_balance(team, db)
    if not missing_roles:
        strengths.append("主要ロールが揃っている")
    else:
        score -= 8 * len(missing_roles)
        weaknesses.append(f"不足ロール: {', '.join(missing_roles)}")

    cores = detect_cores(team, db)
    if cores:
        strengths.append("有名コアを形成")
        score += min(8, 4 * len(cores))

    sweep_status = sweep_support_status(team, db)
    if sweep_status["sweepers"] and sweep_status["has_setup"]:
        strengths.append("抜きエースと起点作成が両立")
        score += 6
    elif sweep_status["sweepers"] and not sweep_status["has_setup"]:
        weaknesses.append("抜き性能は高いが起点作成が不足")
        score -= 8

    critical = detect_critical_vulnerabilities(team, db)
    if critical:
        score -= 10 * len(critical)
        weaknesses.extend([f"{c['name']}が一貫" for c in critical])

    def_table = calc_defensive_table(team, db)
    heavy_weak = def_table[def_table["弱点"] >= 3]["攻撃タイプ"].tolist()
    if heavy_weak:
        score -= 2 * len(heavy_weak)
        weaknesses.append(f"被ダメ偏り: {', '.join(heavy_weak[:4])}")

    score = max(0, min(100, score))
    return {"score": score, "strengths": strengths, "weaknesses": weaknesses, "cores": cores}


def estimate_survivability(team: list[str], db: dict) -> list[dict]:
    results = []
    for threat, rationale in META_TOP_RATIONALE.items():
        attackers = rationale["pressure_types"]
        for name in team:
            info = db[name]
            types = get_types(info)
            bulk = info["stats"]["H"] + info["stats"]["B"] + info["stats"]["D"]
            mult = max(type_multiplier(t, types) for t in attackers)
            if mult >= 2 and bulk < 300:
                verdict = "危険"
            elif mult >= 2:
                verdict = "要注意"
            elif mult <= 0.5:
                verdict = "安定"
            else:
                verdict = "互角"
            results.append(
                {
                    "threat": threat,
                    "name": name,
                    "mult": mult,
                    "bulk": bulk,
                    "verdict": verdict,
                }
            )
    return results


def evaluate_cycle_score(team: list[str], db: dict) -> dict:
    volt_users = [n for n in team if "ボルトチェンジ" in get_all_moves(db[n])]
    uturn_users = [n for n in team if "とんぼがえり" in get_all_moves(db[n])]
    pivots = len(set(volt_users + uturn_users))
    cushions = [n for n in team if "クッション" in db[n]["role_labels"] or "受け" in db[n]["role_labels"]]
    score = min(100, pivots * 18 + len(cushions) * 12)
    if pivots == 0:
        label = "低"
    elif pivots == 1:
        label = "中"
    else:
        label = "高"
    return {
        "score": score,
        "label": label,
        "pivots": pivots,
        "pivot_names": list(dict.fromkeys(volt_users + uturn_users)),
        "cushions": cushions,
    }


def suggest_tera_solutions(team: list[str], db: dict) -> list[dict]:
    solutions = []
    if not team:
        return solutions
    def_table = calc_defensive_table(team, db)
    weak_types = def_table[def_table["弱点"] >= 3]["攻撃タイプ"].tolist()
    if not weak_types:
        return solutions
    defensive_tera = {
        "ほのお": "みず",
        "みず": "くさ",
        "でんき": "じめん",
        "くさ": "ほのお",
        "こおり": "ほのお",
        "かくとう": "フェアリー",
        "どく": "はがね",
        "じめん": "くさ",
        "ひこう": "でんき",
        "エスパー": "あく",
        "むし": "ほのお",
        "いわ": "みず",
        "ゴースト": "あく",
        "ドラゴン": "フェアリー",
        "あく": "かくとう",
        "はがね": "ほのお",
        "フェアリー": "はがね",
        "ノーマル": "はがね",
    }
    for wt in weak_types:
        target_tera = defensive_tera.get(wt)
        if not target_tera:
            continue
        candidates = []
        for name in team:
            info = db[name]
            if wt in get_types(info):
                continue
            if type_multiplier(wt, get_types(info)) >= 2:
                candidates.append(name)
        if candidates:
            solutions.append(
                {
                    "weak_type": wt,
                    "tera": target_tera,
                    "candidates": candidates[:2],
                }
            )
    return solutions


def tactical_review(team: list[str], db: dict) -> dict:
    review = {"alerts": [], "reasons": [], "wins": []}
    if not team:
        return review

    critical = detect_critical_vulnerabilities(team, db)
    for item in critical:
        reason = f"{item['name']}の攻撃範囲に対し、弱点が{item['weak_count']}体重なる"
        review["alerts"].append(f"{item['name']}が重い")
        review["reasons"].append(reason)

    cycle = evaluate_cycle_score(team, db)
    if cycle["label"] == "低":
        review["alerts"].append("対面操作が困難")
        review["reasons"].append("とんぼ/ボルチェン持ちが不足し、不利対面の解消が難しい")

    sweep = sweep_support_status(team, db)
    if sweep["sweepers"] and not sweep["has_setup"]:
        review["alerts"].append("抜き性能の支援不足")
        review["reasons"].append("スイーパーはいるが起点作成役がいない")

    cores = detect_cores(team, db)
    if cores:
        core = cores[0]["members"]
        review["wins"].append(f"{core[0]}で対面調整し、{core[1]}で有利対面を継続")

    if sweep["sweepers"]:
        sweeper = sweep["sweepers"][0]
        review["wins"].append(f"起点作成→{sweeper}でテラス全抜きを狙う")

    return review


def _team_signature(team: list[str]) -> int:
    return sum(sum(ord(c) for c in name) for name in team) % 7


def generate_anti_meta_plans(team: list[str], db: dict) -> list[dict]:
    if not team:
        return []
    options = []
    signature = _team_signature(team)
    tera_solutions = suggest_tera_solutions(team, db)
    sweep = sweep_support_status(team, db)
    if tera_solutions:
        s = tera_solutions[signature % len(tera_solutions)]
        candidates = " / ".join(s["candidates"])
        options.append(
            {
                "title": "奇策テラ切り返し",
                "plan": f"敢えて不利対面で{candidates}に{s['tera']}テラスを切り、{s['weak_type']}一貫を遮断して流れを奪う。",
                "risk": "テラス温存が崩れた場合の再現性が低い。",
                "reward": "相手の計算を外し、一気に主導権を奪える。",
                "highlight": True,
            }
        )
    if sweep["sweepers"]:
        sweeper = sweep["sweepers"][0]
        options.append(
            {
                "title": "囮展開",
                "plan": f"受け駒を捨て気味に使い、{sweeper}の全抜きラインを最優先で作る。",
                "risk": "受け回しが崩れて一気に不利になる。",
                "reward": "相手が守りに入る前に試合を決められる。",
                "highlight": True,
            }
        )
    if not options:
        options.append(
            {
                "title": "速度逆転プラン",
                "plan": "先制技や切り返し技に寄せ、相手のSラインを無視した攻め筋を構築する。",
                "risk": "交代戦に弱くなりやすい。",
                "reward": "相手の想定を崩しやすい。",
                "highlight": True,
            }
        )
    return options


def resource_priority_advice(team: list[str], db: dict) -> list[str]:
    advice = []
    sweep = sweep_support_status(team, db)
    if sweep["sweepers"]:
        advice.append(f"勝ち筋のエースは{', '.join(sweep['sweepers'][:2])}。HP温存を最優先。")
    cores = detect_cores(team, db)
    if cores:
        core_members = " / ".join(cores[0]["members"])
        advice.append(f"{core_members}はサイクルの心臓。交代で削られ過ぎないよう注意。")
    cycle = evaluate_cycle_score(team, db)
    if cycle["pivots"] == 0:
        advice.append("不利対面の処理はテラス権で行う前提。温存ラインを確保。")
    else:
        pivots = ", ".join(cycle["pivot_names"][:2])
        advice.append(f"{pivots}は対面操作の鍵。持ち物・HPを後半まで残す。")
    return advice


def win_loss_simulation(team: list[str], db: dict) -> dict:
    if not team:
        return {"win": [], "loss": []}
    sweep = sweep_support_status(team, db)
    wins = []
    losses = []
    if sweep["sweepers"]:
        sweeper = sweep["sweepers"][0]
        wins.append(f"{sweeper}の起点が完成すれば全抜きが見える。")
        losses.append(f"{sweeper}が削られると勝ち筋が消える。")
    critical = detect_critical_vulnerabilities(team, db)
    if critical:
        losses.append(f"{critical[0]['name']}の一貫が止まらないと負け筋。")
    cycle = evaluate_cycle_score(team, db)
    if cycle["pivots"] >= 2:
        wins.append("対面操作で有利対面を繰り返せれば試合を優位に運べる。")
    else:
        losses.append("交代戦が続くと不利な対面を解消できない。")
    return {"win": wins, "loss": losses}


def build_dual_plans(team: list[str], db: dict) -> list[dict]:
    if not team:
        return []
    plans = []
    review = tactical_review(team, db)
    default_plan = {
        "title": "プランA：定石",
        "plan": review["wins"][0] if review["wins"] else "起点作成→エースで全抜きを目指す。",
        "risk": "相手の受けルートにハマると詰みやすい。",
        "reward": "再現性が高く安定した勝ち筋。",
        "highlight": False,
    }
    plans.append(default_plan)
    anti_meta = generate_anti_meta_plans(team, db)
    if anti_meta:
        anti = anti_meta[_team_signature(team) % len(anti_meta)]
        anti["title"] = "プランB：奇策"
        plans.append(anti)
    return plans


def varied_insight_lines(team: list[str], db: dict) -> list[str]:
    variants = [
        "相手の勝ち筋を断つより、自分の勝ち筋を太くする方が速い局面。",
        "1ターンの猶予を作れれば、勝ち筋が現実になる構図。",
        "表の対策より裏の押し付けで試合速度を上げるべき。",
        "受けではなく対面操作でテンポを取るのが正解。",
        "テラスの使い所が勝敗を決める構築。",
        "勝ち筋は細いが、通れば一瞬で決まるタイプ。",
    ]
    if not team:
        return []
    pick = _team_signature(team)
    return [variants[pick % len(variants)]]


def meta_threat_levels(team: list[str], db: dict) -> list[dict]:
    results = []
    for name, types in META_TOP_POKEMON.items():
        weak = 0
        resist = 0
        immune = 0
        for p in team:
            mults = [type_multiplier(t, get_types(db[p])) for t in types]
            if any(m == 0 for m in mults):
                immune += 1
            elif any(m >= 2 for m in mults):
                weak += 1
            elif all(m <= 0.5 for m in mults):
                resist += 1
        threat = max(0, weak - resist - (1 if immune else 0))
        results.append(
            {
                "name": name,
                "weak": weak,
                "resist": resist,
                "immune": immune,
                "score": threat,
                "level": "high" if threat >= 2 else "mid" if threat == 1 else "low",
            }
        )
    return results


def build_speed_cards(team: list[str], db: dict, nature: str | None) -> list[dict]:
    cards = []
    max_speed = max((calc_stat_max(db[p]["stats"]["S"], nature, "S") for p in team), default=0)
    for p in team:
        s_base = db[p]["stats"]["S"]
        s_actual = calc_stat_max(s_base, nature, "S")
        ratio = 0 if max_speed == 0 else s_actual / max_speed
        cards.append(
            {
                "name": p,
                "type": " / ".join(get_types(db[p])),
                "base": s_base,
                "actual": s_actual,
                "ratio": ratio,
                "is_fastest": s_actual == max_speed and max_speed > 0,
            }
        )
    return sorted(cards, key=lambda x: x["actual"], reverse=True)


def default_team_slot() -> dict:
    return {"pokemon": NO_SELECTION, "nickname": "", "item": "", "tera": "", "role": ""}


def normalize_team_member(member: dict | str) -> dict:
    if isinstance(member, str):
        data = default_team_slot()
        data["pokemon"] = member
        return data
    data = default_team_slot()
    data.update(member or {})
    data["pokemon"] = data.get("pokemon") or NO_SELECTION
    return data


def team_slots_from_members(members: list) -> list[dict]:
    slots = [normalize_team_member(m) for m in members[:TEAM_SLOTS]]
    while len(slots) < TEAM_SLOTS:
        slots.append(default_team_slot())
    return slots


def extract_team_names(team_slots: list[dict]) -> list[str]:
    return [slot["pokemon"] for slot in team_slots if slot["pokemon"] != NO_SELECTION]


def build_speed_table(team: list[str], db: dict, nature: str | None) -> pd.DataFrame:
    rows = []
    max_speed = max((calc_stat_max(db[p]["stats"]["S"], nature, "S") for p in team), default=0)
    for p in team:
        s_base = db[p]["stats"]["S"]
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


def speed_target_check(team: list[str], db: dict, nature: str | None) -> dict[str, dict]:
    fastest = max((calc_stat_max(db[p]["stats"]["S"], nature, "S") for p in team), default=0)
    results = {}
    for label, base in SPEED_TARGET_BASES.items():
        target = calc_stat_max(base, nature, "S")
        results[label] = {"target": target, "ok": fastest > target}
    return results


@st.cache_data(show_spinner=False)
def build_speed_ranking(db: dict, nature: str | None) -> pd.DataFrame:
    rows = []
    for name, info in db.items():
        s_base = info["stats"]["S"]
        s_actual = calc_stat_max(s_base, nature, "S")
        rows.append(
            {
                "ポケモン": name,
                "タイプ": " / ".join(get_types(info)),
                "役割": ", ".join(info.get("role_labels", [])),
                "S種族値": s_base,
                "S最大実数": s_actual,
            }
        )
    df = pd.DataFrame(rows)
    return df.sort_values("S最大実数", ascending=False)


def export_showdown(team: list[str], db: dict) -> str:
    lines = []
    for name in team:
        info = db[name]
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


def meta_warnings(team: list[str], db: dict) -> tuple[list[str], list[str]]:
    coverage_missing = []
    for name, types in META_TOP_POKEMON.items():
        if not has_super_effective(team, types, db):
            coverage_missing.append(name)

    combo_alerts = []
    for combo in META_COMBOS:
        lacks_coverage = all(
            not has_super_effective(team, META_TOP_POKEMON.get(m, []), db) for m in combo["members"]
        )
        lacks_resist = all(
            all(not has_resist(team, t, db) for t in META_TOP_POKEMON.get(m, [])) for m in combo["members"]
        )
        if lacks_coverage and lacks_resist:
            combo_alerts.append(combo["name"])
    return coverage_missing, combo_alerts


def meta_pressure(team: list[str], db: dict) -> list[str]:
    warnings = []
    if not team:
        return warnings
    threshold = (len(team) + 1) // 2
    for name, types in META_TOP_POKEMON.items():
        weak_count = 0
        for p in team:
            defender_types = get_types(db[p])
            if any(type_multiplier(t, defender_types) >= 2 for t in types):
                weak_count += 1
        if weak_count >= threshold:
            warnings.append(f"{name}が一貫しています")
    return warnings


def counter_candidates(team: list[str], target_types: list[str], db: dict) -> list[str]:
    scored = []
    for name, info in db.items():
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
        offense_score = 2 if has_super_effective([name], target_types, db) else 0
        role_score = 1 if "クッション" in info["role_labels"] else 0
        total = resist_score + offense_score + role_score
        if total > 0:
            scored.append((total, name))
    scored.sort(reverse=True)
    return [name for _, name in scored[:6]]


def suggest_complements(team: list[str], roles_needed: list[str], meta_focus: list[str], concept: str, db: dict) -> list[dict]:
    if not team:
        return []
    base_table = calc_defensive_table(team, db)
    weakness_types = set(base_table[base_table["弱点"] >= 2]["攻撃タイプ"].tolist())

    meta_keywords = set()
    for threat in meta_focus:
        meta_keywords.update(META_THREATS.get(threat, []))

    team_has_setup = any(is_setup_role(db[p]) for p in team)
    team_has_sweeper = any(is_setup_sweeper(db[p]) for p in team)

    scored = []
    for name, info in db.items():
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


def build_tactical_plans(team: list[str], db: dict) -> list[str]:
    plans = []
    setup_candidates = [p for p in team if is_setup_role(db[p])]
    sweepers = [p for p in team if is_setup_sweeper(db[p])]
    if setup_candidates and sweepers:
        lead = setup_candidates[0]
        finisher = sweepers[0]
        tera = recommended_tera(db[finisher])
        plans.append(f"積みリレープラン: {lead}で起点を作り、{finisher}でテラスタル({tera[0]})して全抜き。")

    cushions = [p for p in team if "クッション" in db[p]["role_labels"]]
    attackers = [p for p in team if "エース" in db[p]["role_labels"] or "ブレイカー" in db[p]["role_labels"]]
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


def synergy_score(a: str, b: str, db: dict) -> int:
    types_a = get_types(db[a])
    types_b = get_types(db[b])
    score = 0
    for t in TYPES:
        ma = type_multiplier(t, types_a)
        mb = type_multiplier(t, types_b)
        if ma >= 2 and mb <= 0.5:
            score += 1
        if mb >= 2 and ma <= 0.5:
            score += 1
    return score


def build_synergy_network(team: list[str], db: dict) -> go.Figure:
    if len(team) < 2:
        fig = go.Figure()
        fig.update_layout(template="plotly_white", height=380)
        return fig

    positions = {}
    for i, name in enumerate(team):
        angle = (2 * math.pi * i) / len(team)
        positions[name] = (1.2 * math.cos(angle), 1.2 * math.sin(angle))

    edge_x = []
    edge_y = []
    for i, a in enumerate(team):
        for b in team[i + 1 :]:
            score = synergy_score(a, b, db)
            if score > 0:
                x0, y0 = positions[a]
                x1, y1 = positions[b]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    for name in team:
        x, y = positions[name]
        node_x.append(x)
        node_y.append(y)
        node_text.append(name)
        primary_type = get_types(db[name])[0]
        node_colors.append(TYPE_COLORS.get(primary_type, "#3B82F6"))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(color="rgba(100, 116, 139, 0.5)", width=1),
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
            marker=dict(
                size=22,
                color=node_colors,
                line=dict(width=1, color="#E2E8F0"),
                opacity=0.95,
            ),
            textfont=dict(color="#1E293B"),
            hoverinfo="text",
        )
    )
    fig.update_layout(
        template="plotly_white",
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
    )
    return fig


def render_stat_bar(value: int, label: str) -> str:
    max_value = 255
    ratio = max(0, min(value, max_value)) / max_value
    percent = int(ratio * 100)
    if ratio >= 0.8:
        color = "linear-gradient(90deg, #FFB800, #FFF2B0)"
    elif ratio >= 0.5:
        color = "linear-gradient(90deg, #22D3EE, #38BDF8)"
    else:
        color = "linear-gradient(90deg, #F97316, #FACC15)"
    return (
        f"<div class='stat-bar-label'>{label} {value}</div>"
        f"<div class='stat-bar'><div class='stat-bar-fill' style='width:{percent}%; background:{color};'></div></div>"
    )


def table_to_plotly(df: pd.DataFrame, title: str) -> go.Figure:
    header_color = "#F1F5F9"
    cells_color = "#FFFFFF"
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df.columns),
                    fill_color=header_color,
                    font=dict(color="#1E293B", size=12),
                    line=dict(color="#E2E8F0"),
                ),
                cells=dict(
                    values=[df[col].tolist() for col in df.columns],
                    fill_color=cells_color,
                    font=dict(color="#334155", size=12),
                    line=dict(color="#E2E8F0"),
                ),
            )
        ]
    )
    fig.update_layout(
        template="plotly_white",
        height=360,
        margin=dict(l=10, r=10, t=20, b=10),
        title=title,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
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


def build_personal_warning(logs: list[dict], team: list[str], db: dict) -> str | None:
    ranking = battle_log_summary(logs)
    if not ranking:
        return None
    top_name, count = ranking[0]
    if top_name not in META_TOP_POKEMON:
        return None
    counters = counter_candidates(team, META_TOP_POKEMON[top_name], db)
    if not counters:
        return f"戦績上、{top_name}が非常に重いため、受け出し可能な枠の追加を強く推奨します。"
    return f"戦績上、{top_name}が非常に重いため、{counters[0]}の採用を強く推奨します。"
