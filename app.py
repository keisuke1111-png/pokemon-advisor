import streamlit as st
import pandas as pd

POKEMON_LIST = [
    {
        "id": 149,
        "name": "カイリュー",
        "types": ["ドラゴン", "ひこう"],
        "abilities": ["マルチスケイル", "せいしんりょく"],
        "moves": ["しんそく", "りゅうのまい", "げきりん", "じしん"],
        "stats": {"hp": 91, "atk": 134, "def": 95, "spa": 100, "spd": 100, "spe": 80},
    },
    {
        "id": 987,
        "name": "ハバタクカミ",
        "types": ["ゴースト", "フェアリー"],
        "abilities": ["こだいかっせい"],
        "moves": ["ムーンフォース", "シャドーボール", "マジカルフレイム", "みがわり"],
        "stats": {"hp": 55, "atk": 55, "def": 55, "spa": 135, "spd": 135, "spe": 135},
    },
    {
        "id": 892,
        "name": "ウーラオス(れんげきのかた)",
        "types": ["かくとう", "みず"],
        "abilities": ["ふかしのこぶし"],
        "moves": ["すいりゅうれんだ", "インファイト", "アクアジェット", "つるぎのまい"],
        "stats": {"hp": 100, "atk": 130, "def": 100, "spa": 63, "spd": 60, "spe": 97},
    },
    {
        "id": 1002,
        "name": "パオジアン",
        "types": ["あく", "こおり"],
        "abilities": ["わざわいのつるぎ"],
        "moves": ["つららおとし", "かみくだく", "せいなるつるぎ", "ふいうち"],
        "stats": {"hp": 80, "atk": 120, "def": 80, "spa": 90, "spd": 65, "spe": 135},
    },
    {
        "id": 1000,
        "name": "サーフゴー",
        "types": ["ゴースト", "はがね"],
        "abilities": ["おうごんのからだ"],
        "moves": ["ゴールドラッシュ", "シャドーボール", "わるだくみ", "きあいだま"],
        "stats": {"hp": 87, "atk": 60, "def": 95, "spa": 133, "spd": 91, "spe": 84},
    },
    {
        "id": 645,
        "name": "ランドロス(れいじゅうフォルム)",
        "types": ["じめん", "ひこう"],
        "abilities": ["いかく"],
        "moves": ["じしん", "とんぼがえり", "ストーンエッジ", "つるぎのまい"],
        "stats": {"hp": 89, "atk": 145, "def": 90, "spa": 105, "spd": 80, "spe": 91},
    },
    {
        "id": 1003,
        "name": "ディンルー",
        "types": ["あく", "じめん"],
        "abilities": ["わざわいのうつわ"],
        "moves": ["じしん", "まきびし", "ステルスロック", "じわれ"],
        "stats": {"hp": 155, "atk": 110, "def": 125, "spa": 45, "spd": 80, "spe": 50},
    },
    {
        "id": 991,
        "name": "テツノツツミ",
        "types": ["こおり", "みず"],
        "abilities": ["クォークチャージ"],
        "moves": ["フリーズドライ", "ハイドロポンプ", "こおりのつぶて", "みがわり"],
        "stats": {"hp": 56, "atk": 80, "def": 114, "spa": 124, "spd": 60, "spe": 136},
    },
    {
        "id": 445,
        "name": "ガブリアス",
        "types": ["ドラゴン", "じめん"],
        "abilities": ["すながくれ", "さめはだ"],
        "moves": ["じしん", "げきりん", "アイアンヘッド", "ほのおのキバ"],
        "stats": {"hp": 108, "atk": 130, "def": 95, "spa": 80, "spd": 85, "spe": 102},
    },
    {
        "id": 1004,
        "name": "イーユイ",
        "types": ["あく", "ほのお"],
        "abilities": ["わざわいのたま"],
        "moves": ["かえんほうしゃ", "あくのはどう", "おにび", "わるだくみ"],
        "stats": {"hp": 55, "atk": 80, "def": 80, "spa": 135, "spd": 120, "spe": 100},
    },
]

ALL_TYPES = [
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

STAT_KEYS = ["hp", "atk", "def", "spa", "spd", "spe"]
STAT_LABELS = {"hp": "H", "atk": "A", "def": "B", "spa": "C", "spd": "D", "spe": "S"}

st.set_page_config(page_title="ポケモン大図鑑", layout="wide")

st.title("ポケモン大図鑑（高性能検索エンジン）")
st.caption("種族値・タイプ・特性・技でリアルタイムに絞り込み")

with st.sidebar:
    st.header("検索フィルター")
    search_term = st.text_input("名前 / 技 / 特性")
    selected_types = st.multiselect("タイプ", ALL_TYPES)
    st.subheader("種族値（最小値）")
    min_stats = {}
    for key in STAT_KEYS:
        min_stats[key] = st.slider(
            f"{STAT_LABELS[key]}", min_value=40, max_value=200, value=40
        )

filtered = []
needle = search_term.strip().lower()

for pokemon in POKEMON_LIST:
    matches_text = (
        not needle
        or any(
            needle in entry.lower()
            for entry in [pokemon["name"], *pokemon["abilities"], *pokemon["moves"]]
        )
    )
    matches_types = not selected_types or all(
        t in pokemon["types"] for t in selected_types
    )
    matches_stats = all(
        pokemon["stats"][key] >= min_stats[key] for key in STAT_KEYS
    )
    if matches_text and matches_types and matches_stats:
        total = sum(pokemon["stats"][key] for key in STAT_KEYS)
        filtered.append({
            "No.": pokemon["id"],
            "名前": pokemon["name"],
            "タイプ": " / ".join(pokemon["types"]),
            "特性": " / ".join(pokemon["abilities"]),
            "技": " / ".join(pokemon["moves"]),
            "H": pokemon["stats"]["hp"],
            "A": pokemon["stats"]["atk"],
            "B": pokemon["stats"]["def"],
            "C": pokemon["stats"]["spa"],
            "D": pokemon["stats"]["spd"],
            "S": pokemon["stats"]["spe"],
            "BST": total,
        })

st.subheader(f"検索結果: {len(filtered)} 匹")

if filtered:
    df = pd.DataFrame(filtered)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("条件に一致するポケモンが見つかりませんでした。")
