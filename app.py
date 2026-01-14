import json
import os
from typing import List

import pandas as pd
import streamlit as st

DATA_PATH = "pokemon_data.json"
STAT_KEYS = ["hp", "atk", "def", "spa", "spd", "spe"]
STAT_LABELS = {"hp": "H", "atk": "A", "def": "B", "spa": "C", "spd": "D", "spe": "S"}


@st.cache_data(show_spinner=False)
def load_pokemon_data(path: str, version: float) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as file:
        raw = json.load(file)

    records: List[dict] = []
    for entry in raw:
        display_name = entry.get("japanese_name") or entry.get("name", "")
        type1 = entry.get("type1_ja") or entry.get("type1", "")
        type2 = entry.get("type2_ja") or entry.get("type2", "")
        ability1 = entry.get("ability1_ja") or entry.get("ability1", "")
        ability2 = entry.get("ability2_ja") or entry.get("ability2", "")
        hidden = entry.get("hidden_ability_ja") or entry.get("hidden_ability", "")
        moves = " / ".join(entry.get("moves", []))
        records.append(
            {
                "No.": entry.get("id"),
                "名前": display_name,
                "英名": entry.get("name", ""),
                "画像": entry.get("image_url", ""),
                "タイプ1": type1,
                "タイプ2": type2,
                "特性1": ability1,
                "特性2": ability2,
                "隠れ特性": hidden,
                "H": entry.get("hp", 0),
                "A": entry.get("atk", 0),
                "B": entry.get("def", 0),
                "C": entry.get("spa", 0),
                "D": entry.get("spd", 0),
                "S": entry.get("spe", 0),
                "合計": entry.get("total", 0),
                "技": moves,
            }
        )

    return pd.DataFrame(records)


def build_search_text(row: pd.Series) -> str:
    return " ".join(
        [
            str(row.get("名前", "")),
            str(row.get("英名", "")),
            str(row.get("特性1", "")),
            str(row.get("特性2", "")),
            str(row.get("隠れ特性", "")),
            str(row.get("技", "")),
        ]
    ).lower()


st.set_page_config(page_title="ポケモン大図鑑", layout="wide")
st.title("ポケモン大図鑑（全データ版）")
st.caption("タイプ・種族値・特性・技をAND検索して高速フィルタリング")

data_version = os.path.getmtime(DATA_PATH)
data = load_pokemon_data(DATA_PATH, data_version)
data["検索テキスト"] = data.apply(build_search_text, axis=1)

all_types = sorted(
    set(data["タイプ1"].dropna().tolist() + data["タイプ2"].dropna().tolist())
)
all_types = [t for t in all_types if t]

with st.sidebar:
    st.header("検索フィルター")
    search_term = st.text_input("名前 / 技 / 特性（スペース区切りで複数）")

    st.subheader("タイプ")
    selected_types = st.multiselect("タイプ（最大2つ）", all_types)

    st.subheader("種族値（以上 / 以下）")
    stat_ranges = {}
    for key in STAT_KEYS:
        label = STAT_LABELS[key]
        min_value = int(data[label].min())
        max_value = int(data[label].max())
        stat_ranges[key] = st.slider(
            f"{label}",
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value),
        )

    total_min = int(data["合計"].min())
    total_max = int(data["合計"].max())
    total_range = st.slider(
        "合計値(BST)",
        min_value=total_min,
        max_value=total_max,
        value=(total_min, total_max),
    )

    page_size = st.selectbox("表示件数", [100, 200, 500], index=0)

filtered = data.copy()

if len(selected_types) > 2:
    selected_types = selected_types[:2]

if len(selected_types) == 1:
    selected = selected_types[0]
    filtered = filtered[
        (filtered["タイプ1"] == selected) | (filtered["タイプ2"] == selected)
    ]
elif len(selected_types) == 2:
    selected_a, selected_b = selected_types
    filtered = filtered[
        ((filtered["タイプ1"] == selected_a) & (filtered["タイプ2"] == selected_b))
        | ((filtered["タイプ1"] == selected_b) & (filtered["タイプ2"] == selected_a))
    ]

for key in STAT_KEYS:
    label = STAT_LABELS[key]
    minimum, maximum = stat_ranges[key]
    filtered = filtered[(filtered[label] >= minimum) & (filtered[label] <= maximum)]

filtered = filtered[
    (filtered["合計"] >= total_range[0]) & (filtered["合計"] <= total_range[1])
]

terms = [t for t in search_term.strip().lower().split() if t]
if terms:
    search_text = filtered["検索テキスト"]
    mask = search_text.apply(lambda text: all(term in text for term in terms))
    filtered = filtered[mask]

total_results = len(filtered)
st.subheader(f"検索結果: {total_results} 匹")

if total_results == 0:
    st.info("条件に一致するポケモンが見つかりませんでした。")
else:
    if not search_term and not selected_types:
        filtered = filtered.sort_values("No.").head(page_size)

    total_pages = max((total_results - 1) // page_size + 1, 1)
    page = st.number_input("ページ", min_value=1, max_value=total_pages, value=1)
    start = (page - 1) * page_size
    end = start + page_size
    display = filtered.sort_values("No.").iloc[start:end]

    heatmap_columns = ["H", "A", "B", "C", "D", "S"]
    base_columns = [
        "No.",
        "名前",
        "タイプ1",
        "タイプ2",
        "特性1",
        "特性2",
        "隠れ特性",
        "合計",
    ]
    display_table = display[base_columns + heatmap_columns]
    try:
        styled = display_table.style.background_gradient(
            subset=heatmap_columns, cmap="YlOrRd"
        )
        st.dataframe(styled, use_container_width=True, hide_index=True)
    except ImportError:
        st.info("ヒートマップ表示には matplotlib が必要です。通常テーブルで表示します。")
        st.dataframe(display_table, use_container_width=True, hide_index=True)

    with st.expander("画像付き一覧を表示"):
        image_columns = ["画像", "No.", "名前", "タイプ1", "タイプ2", "合計"]
        st.dataframe(
            display[image_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "画像": st.column_config.ImageColumn("画像", width="small"),
            },
        )
