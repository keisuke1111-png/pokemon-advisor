# VSCodeターミナルで実行:
# pip install streamlit pandas
# streamlit run app.py

import streamlit as st
import pandas as pd


st.set_page_config(page_title="ポケモン構築サポーター", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
body { background: #f6f7fb; }
.main { padding-top: 0.5rem; }
div[data-testid="stSelectbox"] > div, div[data-testid="stMultiSelect"] > div {
  font-size: 1.05rem;
}
div.stButton > button {
  font-size: 1.05rem;
  padding: 0.65rem 1rem;
}
.badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  background: #111827;
  color: white;
  font-size: 0.8rem;
  margin-right: 0.25rem;
}
.card {
  padding: 0.85rem 1rem;
  border-radius: 14px;
  background: white;
  box-shadow: 0 6px 18px rgba(17, 24, 39, 0.08);
  margin-bottom: 0.75rem;
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
    "ノーマル": "#9FA19F",
    "ほのお": "#E76A3B",
    "みず": "#4D90D5",
    "でんき": "#F6C747",
    "くさ": "#62B957",
    "こおり": "#74CEC0",
    "かくとう": "#D3425F",
    "どく": "#B763CF",
    "じめん": "#D89454",
    "ひこう": "#748FC9",
    "エスパー": "#F65F6A",
    "むし": "#92BC2C",
    "いわ": "#C9BB8A",
    "ゴースト": "#5F6DBC",
    "ドラゴン": "#0C69C8",
    "あく": "#595761",
    "はがね": "#5695A3",
    "フェアリー": "#EE90E6",
}

POKEMON_DB = {
    "カイリュー": {
        "types": ["ドラゴン", "ひこう"],
        "stats": {"HP": 91, "A": 134, "B": 95, "C": 100, "D": 100, "S": 80},
        "roles": ["スイーパー"],
        "ability": "マルチスケイル",
        "moves": ["しんそく", "りゅうのまい", "じしん", "はねやすめ"],
        "meta_tags": ["受け崩し", "終盤全抜き"],
        "tera": ["ノーマル", "ひこう", "はがね"],
        "future": ["メガシンカ候補"],
    },
    "ミミッキュ": {
        "types": ["ゴースト", "フェアリー"],
        "stats": {"HP": 55, "A": 90, "B": 80, "C": 50, "D": 105, "S": 96},
        "roles": ["ストッパー", "スイーパー"],
        "ability": "ばけのかわ",
        "moves": ["つるぎのまい", "シャドークロー", "じゃれつく", "かげうち"],
        "meta_tags": ["対ドラゴン", "切り返し"],
        "tera": ["ゴースト", "フェアリー"],
        "future": [],
    },
    "サーフゴー": {
        "types": ["ゴースト", "はがね"],
        "stats": {"HP": 87, "A": 60, "B": 95, "C": 133, "D": 91, "S": 84},
        "roles": ["アタッカー", "クッション"],
        "ability": "おうごんのからだ",
        "moves": ["ゴールドラッシュ", "シャドーボール", "わるだくみ", "トリック"],
        "meta_tags": ["対受け", "サイクル"],
        "tera": ["ゴースト", "はがね"],
        "future": [],
    },
    "ガブリアス": {
        "types": ["ドラゴン", "じめん"],
        "stats": {"HP": 108, "A": 130, "B": 95, "C": 80, "D": 85, "S": 102},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "さめはだ",
        "moves": ["げきりん", "じしん", "ストーンエッジ", "つるぎのまい"],
        "meta_tags": ["電気無効", "崩し"],
        "tera": ["じめん", "ほのお"],
        "future": ["メガシンカ候補"],
    },
    "ロトム(ウォッシュ)": {
        "types": ["でんき", "みず"],
        "stats": {"HP": 50, "A": 65, "B": 107, "C": 105, "D": 107, "S": 86},
        "roles": ["クッション", "サイクル"],
        "ability": "ふゆう",
        "moves": ["ボルトチェンジ", "ハイドロポンプ", "おにび", "トリック"],
        "meta_tags": ["物理受け", "対地面"],
        "tera": ["みず", "でんき"],
        "future": [],
    },
    "ウーラオス(れんげき)": {
        "types": ["かくとう", "みず"],
        "stats": {"HP": 100, "A": 130, "B": 100, "C": 63, "D": 60, "S": 97},
        "roles": ["アタッカー", "ブレイカー"],
        "ability": "ふかしのこぶし",
        "moves": ["すいりゅうれんだ", "インファイト", "アクアジェット", "とんぼがえり"],
        "meta_tags": ["壁破壊", "対受け"],
        "tera": ["みず", "かくとう"],
        "future": [],
    },
    "テツノドクガ": {
        "types": ["ほのお", "どく"],
        "stats": {"HP": 80, "A": 70, "B": 60, "C": 140, "D": 110, "S": 110},
        "roles": ["スイーパー", "アタッカー"],
        "ability": "クォークチャージ",
        "moves": ["ほのおのまい", "ヘドロばくだん", "エナジーボール", "ちょうのまい"],
        "meta_tags": ["対フェアリー", "崩し"],
        "tera": ["ほのお", "くさ"],
        "future": [],
    },
    "ハバタクカミ": {
        "types": ["ゴースト", "フェアリー"],
        "stats": {"HP": 55, "A": 55, "B": 55, "C": 135, "D": 135, "S": 135},
        "roles": ["スイーパー", "アタッカー"],
        "ability": "こだいかっせい",
        "moves": ["ムーンフォース", "シャドーボール", "みがわり", "たたりめ"],
        "meta_tags": ["高速アタッカー", "対ドラゴン"],
        "tera": ["フェアリー", "ゴースト"],
        "future": [],
    },
    "ディンルー": {
        "types": ["あく", "じめん"],
        "stats": {"HP": 155, "A": 110, "B": 125, "C": 55, "D": 80, "S": 45},
        "roles": ["クッション", "受け"],
        "ability": "わざわいのうつわ",
        "moves": ["じしん", "あくのはどう", "ステルスロック", "ふきとばし"],
        "meta_tags": ["受け", "ステロ"],
        "tera": ["あく", "じめん"],
        "future": [],
    },
    "ヘイラッシャ": {
        "types": ["みず"],
        "stats": {"HP": 150, "A": 100, "B": 115, "C": 65, "D": 65, "S": 35},
        "roles": ["クッション", "受け"],
        "ability": "てんねん",
        "moves": ["ウェーブタックル", "ねむる", "いねむり", "じわれ"],
        "meta_tags": ["物理受け", "積み対策"],
        "tera": ["みず"],
        "future": [],
    },
    "キョジオーン": {
        "types": ["いわ"],
        "stats": {"HP": 100, "A": 100, "B": 130, "C": 45, "D": 90, "S": 35},
        "roles": ["クッション", "受け"],
        "ability": "きよめのしお",
        "moves": ["しおづけ", "じこさいせい", "まもる", "ステルスロック"],
        "meta_tags": ["受け", "崩し"],
        "tera": ["いわ", "はがね"],
        "future": [],
    },
    "サザンドラ": {
        "types": ["あく", "ドラゴン"],
        "stats": {"HP": 92, "A": 105, "B": 90, "C": 125, "D": 90, "S": 98},
        "roles": ["アタッカー"],
        "ability": "ふゆう",
        "moves": ["あくのはどう", "りゅうせいぐん", "ラスターカノン", "とんぼがえり"],
        "meta_tags": ["崩し", "対エスパー"],
        "tera": ["はがね", "ドラゴン"],
        "future": [],
    },
    "カバルドン": {
        "types": ["じめん"],
        "stats": {"HP": 108, "A": 112, "B": 118, "C": 68, "D": 72, "S": 47},
        "roles": ["クッション", "受け"],
        "ability": "すなおこし",
        "moves": ["じしん", "あくび", "ステルスロック", "なまける"],
        "meta_tags": ["ステロ", "物理受け"],
        "tera": ["じめん", "みず"],
        "future": [],
    },
    "ブリムオン": {
        "types": ["エスパー", "フェアリー"],
        "stats": {"HP": 57, "A": 90, "B": 95, "C": 136, "D": 103, "S": 29},
        "roles": ["トリックルーム", "アタッカー"],
        "ability": "マジックミラー",
        "moves": ["マジカルシャイン", "サイコキネシス", "トリックルーム", "いやしのねがい"],
        "meta_tags": ["対ドラゴン", "起点回避"],
        "tera": ["フェアリー", "エスパー"],
        "future": [],
    },
    "トドロクツキ": {
        "types": ["あく", "ドラゴン"],
        "stats": {"HP": 105, "A": 139, "B": 71, "C": 55, "D": 101, "S": 119},
        "roles": ["スイーパー"],
        "ability": "こだいかっせい",
        "moves": ["りゅうのまい", "はたきおとす", "アクロバット", "じしん"],
        "meta_tags": ["高速崩し", "終盤全抜き"],
        "tera": ["ひこう", "あく"],
        "future": [],
    },
    "パオジアン": {
        "types": ["あく", "こおり"],
        "stats": {"HP": 80, "A": 120, "B": 80, "C": 90, "D": 65, "S": 135},
        "roles": ["スイーパー", "アタッカー"],
        "ability": "わざわいのつるぎ",
        "moves": ["つららおとし", "かみくだく", "せいなるつるぎ", "つるぎのまい"],
        "meta_tags": ["高速アタッカー", "対ドラゴン"],
        "tera": ["あく", "こおり"],
        "future": [],
    },
    "ウルガモス": {
        "types": ["ほのお", "むし"],
        "stats": {"HP": 85, "A": 60, "B": 65, "C": 135, "D": 105, "S": 100},
        "roles": ["スイーパー"],
        "ability": "ほのおのからだ",
        "moves": ["ちょうのまい", "ほのおのまい", "むしのさざめき", "ギガドレイン"],
        "meta_tags": ["特殊アタッカー", "対草"],
        "tera": ["くさ", "ほのお"],
        "future": [],
    },
    "モロバレル": {
        "types": ["くさ", "どく"],
        "stats": {"HP": 114, "A": 85, "B": 70, "C": 85, "D": 80, "S": 30},
        "roles": ["クッション", "サポート"],
        "ability": "さいせいりょく",
        "moves": ["キノコのほうし", "ギガドレイン", "クリアスモッグ", "いかりのこな"],
        "meta_tags": ["状態異常", "対水"],
        "tera": ["くさ", "みず"],
        "future": [],
    },
    "アーマーガア": {
        "types": ["ひこう", "はがね"],
        "stats": {"HP": 98, "A": 87, "B": 105, "C": 53, "D": 85, "S": 67},
        "roles": ["クッション", "受け"],
        "ability": "ミラーアーマー",
        "moves": ["ボディプレス", "てっぺき", "はねやすめ", "とんぼがえり"],
        "meta_tags": ["物理受け", "対地面"],
        "tera": ["はがね", "ひこう"],
        "future": [],
    },
    "カイオーガ": {
        "types": ["みず"],
        "stats": {"HP": 100, "A": 100, "B": 90, "C": 150, "D": 140, "S": 90},
        "roles": ["アタッカー"],
        "ability": "あめふらし",
        "moves": ["しおふき", "こんげんのはどう", "かみなり", "れいとうビーム"],
        "meta_tags": ["特殊アタッカー", "対鋼"],
        "tera": ["みず", "でんき"],
        "future": [],
    },
    "ザシアン": {
        "types": ["フェアリー", "はがね"],
        "stats": {"HP": 92, "A": 170, "B": 115, "C": 80, "D": 115, "S": 148},
        "roles": ["スイーパー", "アタッカー"],
        "ability": "ふとうのけん",
        "moves": ["きょじゅうざん", "インファイト", "じゃれつく", "つるぎのまい"],
        "meta_tags": ["高速アタッカー", "対ドラゴン"],
        "tera": ["フェアリー", "はがね"],
        "future": [],
    },
    "テツノカイナ": {
        "types": ["かくとう", "でんき"],
        "stats": {"HP": 154, "A": 140, "B": 108, "C": 50, "D": 68, "S": 50},
        "roles": ["アタッカー", "クッション"],
        "ability": "クォークチャージ",
        "moves": ["ドレインパンチ", "ワイルドボルト", "つるぎのまい", "はらだいこ"],
        "meta_tags": ["対水", "物理アタッカー"],
        "tera": ["でんき", "かくとう"],
        "future": [],
    },
    "テツノツツミ": {
        "types": ["こおり", "みず"],
        "stats": {"HP": 56, "A": 80, "B": 65, "C": 124, "D": 60, "S": 136},
        "roles": ["スイーパー"],
        "ability": "クォークチャージ",
        "moves": ["ハイドロポンプ", "れいとうビーム", "フリーズドライ", "クイックターン"],
        "meta_tags": ["高速アタッカー", "対飛行"],
        "tera": ["こおり", "みず"],
        "future": [],
    },
    "ドラパルト": {
        "types": ["ドラゴン", "ゴースト"],
        "stats": {"HP": 88, "A": 120, "B": 75, "C": 100, "D": 75, "S": 142},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "すりぬけ",
        "moves": ["ドラゴンアロー", "ゴーストダイブ", "とんぼがえり", "りゅうのまい"],
        "meta_tags": ["高速アタッカー", "切り返し"],
        "tera": ["ゴースト", "ドラゴン"],
        "future": [],
    },
    "サンダー": {
        "types": ["でんき", "ひこう"],
        "stats": {"HP": 90, "A": 90, "B": 85, "C": 125, "D": 90, "S": 100},
        "roles": ["アタッカー", "クッション"],
        "ability": "せいでんき",
        "moves": ["10まんボルト", "ぼうふう", "ねっぷう", "はねやすめ"],
        "meta_tags": ["対草", "対鋼"],
        "tera": ["でんき", "ひこう"],
        "future": [],
    },
    "ハッサム": {
        "types": ["むし", "はがね"],
        "stats": {"HP": 70, "A": 130, "B": 100, "C": 55, "D": 80, "S": 65},
        "roles": ["アタッカー", "クッション"],
        "ability": "テクニシャン",
        "moves": ["バレットパンチ", "とんぼがえり", "つるぎのまい", "はねやすめ"],
        "meta_tags": ["対フェアリー", "物理アタッカー"],
        "tera": ["はがね", "ひこう"],
        "future": [],
    },
    "ドドゲザン": {
        "types": ["あく", "はがね"],
        "stats": {"HP": 100, "A": 135, "B": 120, "C": 60, "D": 85, "S": 50},
        "roles": ["アタッカー", "クッション"],
        "ability": "そうだいしょう",
        "moves": ["ドゲザン", "アイアンヘッド", "ふいうち", "けたぐり"],
        "meta_tags": ["対ゴースト", "切り返し"],
        "tera": ["あく", "はがね"],
        "future": [],
    },
    "ブースター": {
        "types": ["ほのお"],
        "stats": {"HP": 65, "A": 130, "B": 60, "C": 95, "D": 110, "S": 65},
        "roles": ["ブレイカー"],
        "ability": "こんじょう",
        "moves": ["フレアドライブ", "ばかぢから", "でんこうせっか", "ねがいごと"],
        "meta_tags": ["受け崩し", "対鋼"],
        "tera": ["ほのお", "ノーマル"],
        "future": [],
    },
    "トリトドン": {
        "types": ["みず", "じめん"],
        "stats": {"HP": 111, "A": 83, "B": 68, "C": 92, "D": 82, "S": 39},
        "roles": ["クッション", "受け"],
        "ability": "よびみず",
        "moves": ["ねっとう", "だいちのちから", "じこさいせい", "あくび"],
        "meta_tags": ["対電気", "対水"],
        "tera": ["みず", "じめん"],
        "future": [],
    },
    "サーフゴー(スカーフ)": {
        "types": ["ゴースト", "はがね"],
        "stats": {"HP": 87, "A": 60, "B": 95, "C": 133, "D": 91, "S": 84},
        "roles": ["スイーパー", "切り返し"],
        "ability": "おうごんのからだ",
        "moves": ["ゴールドラッシュ", "シャドーボール", "トリック", "きあいだま"],
        "meta_tags": ["高速化", "切り返し"],
        "tera": ["ゴースト", "はがね"],
        "future": [],
    },
    "ラッシャ(ヘイラッシャ)": {
        "types": ["みず"],
        "stats": {"HP": 150, "A": 100, "B": 115, "C": 65, "D": 65, "S": 35},
        "roles": ["クッション"],
        "ability": "てんねん",
        "moves": ["ウェーブタックル", "あくび", "ねむる", "じわれ"],
        "meta_tags": ["物理受け"],
        "tera": ["みず"],
        "future": [],
    },
    "イーユイ": {
        "types": ["ほのお", "あく"],
        "stats": {"HP": 55, "A": 80, "B": 80, "C": 135, "D": 120, "S": 100},
        "roles": ["アタッカー", "ブレイカー"],
        "ability": "わざわいのたま",
        "moves": ["かえんほうしゃ", "オーバーヒート", "あくのはどう", "テラバースト"],
        "meta_tags": ["崩し", "対はがね"],
        "tera": ["ほのお", "あく"],
        "future": [],
    },
    "イダイナキバ": {
        "types": ["じめん", "かくとう"],
        "stats": {"HP": 115, "A": 131, "B": 131, "C": 53, "D": 53, "S": 87},
        "roles": ["クッション", "アタッカー"],
        "ability": "こだいかっせい",
        "moves": ["じしん", "インファイト", "ステルスロック", "こうそくスピン"],
        "meta_tags": ["ステロ", "対でんき"],
        "tera": ["じめん", "かくとう"],
        "future": [],
    },
    "テツノワダチ": {
        "types": ["じめん", "はがね"],
        "stats": {"HP": 90, "A": 112, "B": 120, "C": 72, "D": 70, "S": 106},
        "roles": ["アタッカー", "クッション"],
        "ability": "クォークチャージ",
        "moves": ["じしん", "アイアンヘッド", "こうそくスピン", "ステルスロック"],
        "meta_tags": ["ステロ", "対フェアリー"],
        "tera": ["じめん", "はがね"],
        "future": [],
    },
    "テツノブジン": {
        "types": ["フェアリー", "かくとう"],
        "stats": {"HP": 74, "A": 130, "B": 90, "C": 120, "D": 60, "S": 116},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "クォークチャージ",
        "moves": ["ムーンフォース", "インファイト", "つるぎのまい", "シャドークロー"],
        "meta_tags": ["高速アタッカー", "対ドラゴン"],
        "tera": ["フェアリー", "かくとう"],
        "future": [],
    },
    "セグレイブ": {
        "types": ["ドラゴン", "こおり"],
        "stats": {"HP": 115, "A": 145, "B": 92, "C": 75, "D": 86, "S": 87},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "ねつこうかん",
        "moves": ["つららばり", "げきりん", "りゅうのまい", "じしん"],
        "meta_tags": ["崩し", "対ドラゴン"],
        "tera": ["こおり", "ドラゴン"],
        "future": [],
    },
    "マスカーニャ": {
        "types": ["くさ", "あく"],
        "stats": {"HP": 76, "A": 110, "B": 70, "C": 81, "D": 70, "S": 123},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "へんげんじざい",
        "moves": ["トリックフラワー", "はたきおとす", "とんぼがえり", "かげうち"],
        "meta_tags": ["高速アタッカー", "対水"],
        "tera": ["くさ", "あく"],
        "future": [],
    },
    "ウルガモス(テラス草)": {
        "types": ["ほのお", "むし"],
        "stats": {"HP": 85, "A": 60, "B": 65, "C": 135, "D": 105, "S": 100},
        "roles": ["スイーパー"],
        "ability": "ほのおのからだ",
        "moves": ["ちょうのまい", "ほのおのまい", "ギガドレイン", "みがわり"],
        "meta_tags": ["対水", "積みエース"],
        "tera": ["くさ", "ほのお"],
        "future": [],
    },
    "オーガポン(かまど)": {
        "types": ["くさ", "ほのお"],
        "stats": {"HP": 80, "A": 120, "B": 84, "C": 60, "D": 96, "S": 110},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "かたやぶり",
        "moves": ["ツタこんぼう", "ウッドホーン", "つるぎのまい", "ニードルガード"],
        "meta_tags": ["対水", "崩し"],
        "tera": ["ほのお", "くさ"],
        "future": [],
    },
    "ガチグマ(アカツキ)": {
        "types": ["じめん", "ノーマル"],
        "stats": {"HP": 113, "A": 70, "B": 120, "C": 135, "D": 65, "S": 52},
        "roles": ["ブレイカー", "クッション"],
        "ability": "しんがん",
        "moves": ["ブラッドムーン", "だいちのちから", "あくび", "なまける"],
        "meta_tags": ["崩し", "対でんき"],
        "tera": ["ノーマル", "じめん"],
        "future": [],
    },
    "ドドゲザン(先発)": {
        "types": ["あく", "はがね"],
        "stats": {"HP": 100, "A": 135, "B": 120, "C": 60, "D": 85, "S": 50},
        "roles": ["クッション", "サポート"],
        "ability": "そうだいしょう",
        "moves": ["ステルスロック", "ふいうち", "ドゲザン", "ちょうはつ"],
        "meta_tags": ["ステロ", "対ゴースト"],
        "tera": ["あく", "はがね"],
        "future": [],
    },
    "イーユイ(メガ想定)": {
        "types": ["ほのお", "あく"],
        "stats": {"HP": 55, "A": 90, "B": 90, "C": 155, "D": 130, "S": 110},
        "roles": ["アタッカー"],
        "ability": "メガ想定",
        "moves": ["かえんほうしゃ", "あくのはどう", "わるだくみ", "オーバーヒート"],
        "meta_tags": ["未来想定"],
        "tera": ["ほのお", "あく"],
        "future": ["メガシンカ候補"],
    },
    "エースバーン": {
        "types": ["ほのお"],
        "stats": {"HP": 80, "A": 116, "B": 75, "C": 65, "D": 75, "S": 119},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "リベロ",
        "moves": ["かえんボール", "とんぼがえり", "ふいうち", "とびひざげり"],
        "meta_tags": ["高速アタッカー", "対くさ"],
        "tera": ["ほのお", "かくとう"],
        "future": [],
    },
    "リザードン": {
        "types": ["ほのお", "ひこう"],
        "stats": {"HP": 78, "A": 84, "B": 78, "C": 109, "D": 85, "S": 100},
        "roles": ["アタッカー"],
        "ability": "もうか",
        "moves": ["ねっぷう", "エアスラッシュ", "ソーラービーム", "りゅうのはどう"],
        "meta_tags": ["対草", "対虫"],
        "tera": ["ほのお", "ひこう"],
        "future": ["メガシンカ候補"],
    },
    "バンギラス": {
        "types": ["いわ", "あく"],
        "stats": {"HP": 100, "A": 134, "B": 110, "C": 95, "D": 100, "S": 61},
        "roles": ["クッション", "ブレイカー"],
        "ability": "すなおこし",
        "moves": ["ストーンエッジ", "かみくだく", "ステルスロック", "りゅうのまい"],
        "meta_tags": ["ステロ", "対ゴースト"],
        "tera": ["あく", "いわ"],
        "future": ["メガシンカ候補"],
    },
    "キラフロル": {
        "types": ["いわ", "どく"],
        "stats": {"HP": 83, "A": 55, "B": 90, "C": 130, "D": 81, "S": 86},
        "roles": ["サポート", "アタッカー"],
        "ability": "どくげしょう",
        "moves": ["パワージェム", "ヘドロばくだん", "ステルスロック", "だいちのちから"],
        "meta_tags": ["ステロ", "対フェアリー"],
        "tera": ["どく", "いわ"],
        "future": [],
    },
    "グライオン": {
        "types": ["じめん", "ひこう"],
        "stats": {"HP": 75, "A": 95, "B": 125, "C": 45, "D": 75, "S": 95},
        "roles": ["クッション", "サポート"],
        "ability": "ポイズンヒール",
        "moves": ["じしん", "どくどく", "まもる", "はねやすめ"],
        "meta_tags": ["対でんき", "受け"],
        "tera": ["じめん", "ひこう"],
        "future": [],
    },
    "ラオス(いちげき)": {
        "types": ["かくとう", "あく"],
        "stats": {"HP": 100, "A": 130, "B": 100, "C": 63, "D": 60, "S": 97},
        "roles": ["アタッカー", "ブレイカー"],
        "ability": "ふかしのこぶし",
        "moves": ["あんこくきょうだ", "インファイト", "ふいうち", "とんぼがえり"],
        "meta_tags": ["対受け", "崩し"],
        "tera": ["あく", "かくとう"],
        "future": [],
    },
    "サケブシッポ": {
        "types": ["フェアリー", "エスパー"],
        "stats": {"HP": 115, "A": 65, "B": 99, "C": 65, "D": 115, "S": 111},
        "roles": ["サポート"],
        "ability": "こだいかっせい",
        "moves": ["リフレクター", "ひかりのかべ", "いやしのねがい", "マジカルシャイン"],
        "meta_tags": ["壁", "起点作成"],
        "tera": ["フェアリー", "エスパー"],
        "future": [],
    },
    "レジエレキ": {
        "types": ["でんき"],
        "stats": {"HP": 80, "A": 100, "B": 50, "C": 100, "D": 50, "S": 200},
        "roles": ["スイーパー", "アタッカー"],
        "ability": "トランジスタ",
        "moves": ["サンダープリズン", "ボルトチェンジ", "でんじは", "テラバースト"],
        "meta_tags": ["高速アタッカー", "対水"],
        "tera": ["でんき", "こおり"],
        "future": [],
    },
    "ランドロス(霊獣)": {
        "types": ["じめん", "ひこう"],
        "stats": {"HP": 89, "A": 125, "B": 90, "C": 115, "D": 80, "S": 101},
        "roles": ["クッション", "アタッカー"],
        "ability": "いかく",
        "moves": ["じしん", "とんぼがえり", "がんせきふうじ", "ステルスロック"],
        "meta_tags": ["ステロ", "対でんき"],
        "tera": ["じめん", "ひこう"],
        "future": [],
    },
    "ヒードラン": {
        "types": ["ほのお", "はがね"],
        "stats": {"HP": 91, "A": 90, "B": 106, "C": 130, "D": 106, "S": 77},
        "roles": ["クッション", "アタッカー"],
        "ability": "もらいび",
        "moves": ["マグマストーム", "ラスターカノン", "だいちのちから", "ステルスロック"],
        "meta_tags": ["対フェアリー", "ステロ"],
        "tera": ["ほのお", "はがね"],
        "future": [],
    },
    "ゴリランダー": {
        "types": ["くさ"],
        "stats": {"HP": 100, "A": 125, "B": 90, "C": 60, "D": 70, "S": 85},
        "roles": ["アタッカー"],
        "ability": "グラスメイカー",
        "moves": ["グラススライダー", "ウッドハンマー", "はたきおとす", "とんぼがえり"],
        "meta_tags": ["対水", "崩し"],
        "tera": ["くさ", "あく"],
        "future": [],
    },
    "カイオーガ(スカーフ)": {
        "types": ["みず"],
        "stats": {"HP": 100, "A": 100, "B": 90, "C": 150, "D": 140, "S": 90},
        "roles": ["スイーパー", "アタッカー"],
        "ability": "あめふらし",
        "moves": ["しおふき", "なみのり", "かみなり", "れいとうビーム"],
        "meta_tags": ["高速化", "対はがね"],
        "tera": ["みず", "でんき"],
        "future": [],
    },
    "テラパゴス": {
        "types": ["ノーマル"],
        "stats": {"HP": 90, "A": 65, "B": 85, "C": 135, "D": 105, "S": 60},
        "roles": ["アタッカー", "クッション"],
        "ability": "テラスチェンジ",
        "moves": ["テラクラスター", "だいちのちから", "リフレクター", "ねむる"],
        "meta_tags": ["特殊アタッカー", "対ドラゴン"],
        "tera": ["ノーマル"],
        "future": ["テラス環境想定"],
    },
    "ウネルミナモ": {
        "types": ["みず", "ドラゴン"],
        "stats": {"HP": 99, "A": 83, "B": 91, "C": 125, "D": 83, "S": 109},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "こだいかっせい",
        "moves": ["ハイドロポンプ", "りゅうせいぐん", "ねっぷう", "ちょうはつ"],
        "meta_tags": ["対ほのお", "崩し"],
        "tera": ["みず", "ドラゴン"],
        "future": [],
    },
    "テツノイサハ": {
        "types": ["くさ", "エスパー"],
        "stats": {"HP": 90, "A": 130, "B": 88, "C": 70, "D": 108, "S": 104},
        "roles": ["アタッカー", "スイーパー"],
        "ability": "クォークチャージ",
        "moves": ["リーフブレード", "サイコカッター", "つるぎのまい", "でんこうせっか"],
        "meta_tags": ["対水", "高速アタッカー"],
        "tera": ["くさ", "エスパー"],
        "future": [],
    },
    "クエスパトラ": {
        "types": ["エスパー"],
        "stats": {"HP": 95, "A": 60, "B": 60, "C": 101, "D": 60, "S": 105},
        "roles": ["スイーパー"],
        "ability": "かそく",
        "moves": ["ルミナコリジョン", "みがわり", "てっぺき", "バトンタッチ"],
        "meta_tags": ["積みエース", "崩し"],
        "tera": ["エスパー"],
        "future": [],
    },
    "ドオー": {
        "types": ["どく", "じめん"],
        "stats": {"HP": 130, "A": 75, "B": 60, "C": 45, "D": 100, "S": 20},
        "roles": ["クッション", "受け"],
        "ability": "てんねん",
        "moves": ["じしん", "どくどく", "じこさいせい", "あくび"],
        "meta_tags": ["積み対策", "対でんき"],
        "tera": ["どく", "みず"],
        "future": [],
    },
    "サーフゴー(サイクル)": {
        "types": ["ゴースト", "はがね"],
        "stats": {"HP": 87, "A": 60, "B": 95, "C": 133, "D": 91, "S": 84},
        "roles": ["クッション", "サイクル"],
        "ability": "おうごんのからだ",
        "moves": ["ゴールドラッシュ", "シャドーボール", "ボルトチェンジ", "トリック"],
        "meta_tags": ["サイクル", "対受け"],
        "tera": ["はがね", "ゴースト"],
        "future": [],
    },
    "トリックルームエース(代表)": {
        "types": ["はがね", "フェアリー"],
        "stats": {"HP": 60, "A": 95, "B": 115, "C": 130, "D": 95, "S": 50},
        "roles": ["トリックルーム", "アタッカー"],
        "ability": "ふゆう",
        "moves": ["トリックルーム", "ラスターカノン", "サイコキネシス", "じしん"],
        "meta_tags": ["トリル", "崩し"],
        "tera": ["はがね", "フェアリー"],
        "future": [],
    },
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

# 最新環境の上位を想定したメタチェック用データ
META_TOP_POKEMON = {
    "ハバタクカミ": ["ゴースト", "フェアリー"],
    "イーユイ": ["ほのお", "あく"],
    "カイリュー": ["ドラゴン", "ひこう"],
    "サーフゴー": ["ゴースト", "はがね"],
    "パオジアン": ["あく", "こおり"],
    "ウーラオス(れんげき)": ["かくとう", "みず"],
    "ガチグマ(アカツキ)": ["じめん", "ノーマル"],
    "テツノブジン": ["フェアリー", "かくとう"],
    "セグレイブ": ["ドラゴン", "こおり"],
    "テツノツツミ": ["こおり", "みず"],
}

META_COMBOS = [
    {"name": "ハバタクカミ＋イーユイ", "members": ["ハバタクカミ", "イーユイ"]},
    {"name": "カイリュー＋サーフゴー", "members": ["カイリュー", "サーフゴー"]},
]

# 展開構築判定のための簡易タグ（起点作成/積みエース）
SETUP_MOVES = {"ステルスロック", "あくび", "キノコのほうし", "おにび", "トリックルーム"}
BOOST_MOVES = {"つるぎのまい", "りゅうのまい", "ちょうのまい", "わるだくみ", "はらだいこ"}

SPEED_TARGETS = {
    "最速ドラパルト(142)": 142,
    "最速ハバタクカミ(135)": 135,
    "最速パオジアン(135)": 135,
    "最速マスカーニャ(123)": 123,
    "最速カイリュー(80)": 80,
}


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
            m = type_multiplier(t, POKEMON_DB[p]["types"])
            if m == 0:
                immune += 1
            elif m >= 2:
                weak += 1
                if m >= 4:
                    quad += 1
            elif m <= 0.5:
                resist += 1
        # 弱点が通りやすいタイプは「一貫」として警告
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
            atk_types = POKEMON_DB[p]["types"]
            for atk in atk_types:
                m = type_multiplier(atk, [t])
                if m >= 2:
                    strong += 1
                elif m <= 0.5:
                    weak += 1
        rows.append({"相手タイプ": t, "有利打点数": strong, "不利打点数": weak})
    return pd.DataFrame(rows)


def is_setup_role(info: dict) -> bool:
    # 起点作成役: ステロや状態異常で展開を作る簡易判定
    return any(m in SETUP_MOVES for m in info["moves"]) or "ステロ" in info["meta_tags"]


def is_setup_sweeper(info: dict) -> bool:
    # 積みエース: 積み技を持っていれば候補
    return any(m in BOOST_MOVES for m in info["moves"])


def infer_battle_roles(info: dict) -> set[str]:
    # ステータスと既存rolesから、エース/クッション/スイーパーをざっくり推定
    stats = info["stats"]
    roles = set()
    if max(stats["A"], stats["C"]) >= 120 or "アタッカー" in info["roles"] or "ブレイカー" in info["roles"]:
        roles.add("エース")
    if stats["HP"] >= 100 and (stats["B"] >= 100 or stats["D"] >= 100) or "クッション" in info["roles"] or "受け" in info["roles"]:
        roles.add("クッション")
    if stats["S"] >= 100 or "スイーパー" in info["roles"]:
        roles.add("スイーパー")
    return roles


def team_role_balance(team: list[str]) -> tuple[dict[str, int], list[str]]:
    # パーティ全体のロール分布を集計し、不足分を返す
    counts = {k: 0 for k in ROLE_TARGETS}
    for name in team:
        roles = infer_battle_roles(POKEMON_DB[name])
        for r in roles:
            if r in counts:
                counts[r] += 1
    missing = [r for r, need in ROLE_TARGETS.items() if counts[r] < need]
    return counts, missing


def has_super_effective(team: list[str], defend_types: list[str]) -> bool:
    # 各ポケモンのタイプを「打点」とみなして、弱点を突けるか確認
    for p in team:
        for atk in POKEMON_DB[p]["types"]:
            if type_multiplier(atk, defend_types) >= 2:
                return True
    return False


def has_resist(team: list[str], attack_type: str) -> bool:
    return any(type_multiplier(attack_type, POKEMON_DB[p]["types"]) <= 0.5 for p in team)


def render_type_badges(types: list[str]) -> str:
    return "".join(
        [f'<span class="badge" style="background:{TYPE_COLORS.get(t, "#111827")}">{t}</span>' for t in types]
    )


def recommended_tera(info: dict, team: list[str]) -> list[str]:
    # 既存データがあればそれを優先
    if info.get("tera"):
        return info["tera"]
    # ない場合は、弱点の多いタイプを補う方向で簡易提案
    weakness_types = []
    for t in TYPES:
        if type_multiplier(t, info["types"]) >= 2:
            weakness_types.append(t)
    if weakness_types:
        return weakness_types[:2]
    return info["types"]


def build_speed_table(team: list[str]) -> pd.DataFrame:
    rows = []
    max_speed = max((POKEMON_DB[p]["stats"]["S"] for p in team), default=0)
    for p in team:
        s = POKEMON_DB[p]["stats"]["S"]
        rows.append({"ポケモン": p, "S実数(種族値基準)": s, "最速枠": "◎" if s == max_speed else ""})
    return pd.DataFrame(rows)


def speed_target_check(team: list[str]) -> dict[str, bool]:
    fastest = max((POKEMON_DB[p]["stats"]["S"] for p in team), default=0)
    return {name: fastest > value for name, value in SPEED_TARGETS.items()}


def export_showdown(team: list[str]) -> str:
    lines = []
    for name in team:
        info = POKEMON_DB[name]
        lines.append(f"{name} @ もちもの未設定")
        lines.append(f"Ability: {info['ability']}")
        tera = recommended_tera(info, team)
        if tera:
            lines.append(f"Tera Type: {tera[0]}")
        lines.append("EVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe")
        lines.append("Jolly Nature")
        for move in info["moves"][:4]:
            lines.append(f"- {move}")
        lines.append("")
    return "\n".join(lines).strip()


def meta_warnings(team: list[str]) -> tuple[list[str], list[str]]:
    # メタ上位への打点チェックと並びの警告を出す
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


def suggest_complements(team: list[str], roles_needed: list[str], meta_focus: list[str], concept: str) -> list[str]:
    if not team:
        return []
    base_table = calc_defensive_table(team)
    weakness_types = set(base_table[base_table["弱点"] >= 2]["攻撃タイプ"].tolist())

    meta_keywords = set()
    for threat in meta_focus:
        meta_keywords.update(META_THREATS.get(threat, []))

    scored = []
    for name, info in POKEMON_DB.items():
        if name in team:
            continue
        cover_score = 0
        for wt in weakness_types:
            m = type_multiplier(wt, info["types"])
            if m <= 0.5:
                cover_score += 2
            elif m == 0:
                cover_score += 3
        role_score = 0
        for r in roles_needed:
            if r in info["roles"]:
                role_score += 2
        meta_score = 0
        for tag in info["meta_tags"]:
            if tag in meta_keywords:
                meta_score += 2

        # 構築コンセプトごとの優先度を上乗せ
        concept_score = 0
        stats = info["stats"]
        if concept == "対面構築":
            # 単体性能と素早さを重視
            stat_total = sum(stats.values())
            liability = sum(1 for t in TYPES if type_multiplier(t, info["types"]) >= 2)
            concept_score += (stat_total // 60) + (stats["S"] // 20) - liability
        elif concept == "サイクル構築":
            # クッション役と相性補完を強化
            if "クッション" in info["roles"] or "受け" in info["roles"]:
                concept_score += 4
            concept_score += cover_score
        elif concept == "展開構築":
            # 起点作成と積みエースは別枠で提示するので通常スコアは控えめ
            if is_setup_role(info) or is_setup_sweeper(info):
                concept_score += 3

        total = cover_score + role_score + meta_score + concept_score
        if total > 0:
            scored.append((total, name))

    scored.sort(reverse=True)
    return [name for _, name in scored[:6]]


st.title("ポケモン構築サポーター")
st.write("軸ポケモンを決め、補完枠や弱点をスマホで直感的にチェックできます。")

with st.sidebar:
    st.header("構築の軸を選択")
    core_1 = st.selectbox("軸ポケモン1", ["未選択"] + list(POKEMON_DB.keys()))
    core_2 = st.selectbox("軸ポケモン2 (任意)", ["未選択"] + list(POKEMON_DB.keys()))
    st.header("構築コンセプト")
    concept = st.selectbox("コンセプト", list(CONCEPTS.keys()))
    st.header("役割の希望")
    roles_needed = st.multiselect(
        "必要な役割",
        ["アタッカー", "クッション", "スイーパー", "サポート", "ブレイカー", "受け", "ストッパー", "サイクル", "トリックルーム"],
    )
    st.header("環境対策")
    meta_focus = st.multiselect("意識したい環境", list(META_THREATS.keys()))

additional_members = st.multiselect(
    "追加メンバー (0〜4体)",
    [name for name in POKEMON_DB.keys() if name not in {core_1, core_2}],
)

team = [p for p in [core_1, core_2] if p != "未選択"] + additional_members

tabs = st.tabs(["構築入力", "タイプ相性表", "AIアドバイス"])

with tabs[0]:
    st.subheader("構築入力")
    st.write(CONCEPTS[concept])
    if not team:
        st.info("まずは軸ポケモンを1体選んでください。")
    else:
        st.write(f"現在のメンバー数: {len(team)} / 6")
        for name in team:
            info = POKEMON_DB[name]
            badges = render_type_badges(info["types"])
            st.markdown(
                f'<div class="card"><strong>{name}</strong> {badges}<br>'
                f'役割: {", ".join(info["roles"])} | 特性: {info["ability"]}<br>'
                f'推奨技: {", ".join(info["moves"])}<br>'
                f'推奨テラスタイプ: {", ".join(recommended_tera(info, team))}'
                f"</div>",
                unsafe_allow_html=True,
            )

with tabs[1]:
    st.subheader("タイプ相性表")
    if not team:
        st.info("メンバーを選択すると相性表が表示されます。")
    else:
        st.write("防御相性: 4倍弱点や一貫は赤色で警告。")
        def_table = calc_defensive_table(team)

        def color_def(val, col):
            if col == "4倍弱点" and isinstance(val, int) and val > 0:
                return "background-color: #ff7f7f"
            if col == "一貫" and val == "あり":
                return "background-color: #ff7f7f"
            if col == "弱点" and isinstance(val, int) and val >= 3:
                return "background-color: #ffb3b3"
            if col == "攻撃タイプ":
                return f"background-color: {TYPE_COLORS.get(val, '#ffffff')}; color: #111827;"
            if col in ("耐性", "無効") and isinstance(val, int) and val >= 2:
                return "background-color: #d7f5d7"
            return ""

        def_table_style = def_table.style.apply(
            lambda row: [color_def(v, c) for v, c in zip(row, def_table.columns)], axis=1
        )
        st.dataframe(def_table_style, use_container_width=True, height=460)

        st.write("攻撃相性: 有利打点が少ないタイプは注意。")
        off_table = calc_offensive_table(team)

        def color_off(val):
            if isinstance(val, int):
                if val >= 3:
                    return "background-color: #d7f5d7"
                if val == 0:
                    return "background-color: #ffd6a5"
            return ""

        st.dataframe(off_table.style.applymap(color_off), use_container_width=True, height=460)

with tabs[2]:
    st.subheader("AIアドバイス")
    if not team:
        st.info("メンバーを選択するとアドバイスが表示されます。")
    else:
        st.write("補完枠の提案")
        if concept == "展開構築":
            setup_candidates = []
            sweeper_candidates = []
            for name, info in POKEMON_DB.items():
                if name in team:
                    continue
                if is_setup_role(info):
                    setup_candidates.append(name)
                if is_setup_sweeper(info):
                    sweeper_candidates.append(name)
            st.write("起点作成役候補")
            for name in setup_candidates[:6]:
                info = POKEMON_DB[name]
                st.write(f"- {name} ({', '.join(info['moves'])})")
            st.write("積みエース候補")
            for name in sweeper_candidates[:6]:
                info = POKEMON_DB[name]
                st.write(f"- {name} ({', '.join(info['moves'])})")
        else:
            suggestions = suggest_complements(team, roles_needed, meta_focus, concept)
            if not suggestions:
                st.write("条件に合う候補が見つかりませんでした。役割や環境条件を調整してください。")
            else:
                for name in suggestions:
                    info = POKEMON_DB[name]
                    badges = render_type_badges(info["types"])
                    st.markdown(f"**{name}**  {badges}", unsafe_allow_html=True)
                    st.write(f"役割: {', '.join(info['roles'])} | 対策タグ: {', '.join(info['meta_tags'])}")

        st.subheader("ロールバランスチェック")
        role_counts, missing_roles = team_role_balance(team)
        st.write(f"エース: {role_counts['エース']} / クッション: {role_counts['クッション']} / スイーパー: {role_counts['スイーパー']}")
        if missing_roles:
            st.warning(f"不足している役割: {', '.join(missing_roles)}")
        else:
            st.success("主要ロールは揃っています。")

        st.subheader("Sライン可視化")
        speed_table = build_speed_table(team)
        st.dataframe(speed_table, use_container_width=True, height=240)
        st.write("最速ライン目安（性格・努力値は未考慮の簡易判定）")
        speed_checks = speed_target_check(team)
        for target, ok in speed_checks.items():
            st.write(f"- {target}: {'抜ける' if ok else '抜けない'}")

        st.subheader("メタ対策チェック")
        missing_coverage, combo_alerts = meta_warnings(team)
        if missing_coverage:
            st.warning(f"上位ポケモンへの打点不足: {', '.join(missing_coverage)}")
        else:
            st.success("上位ポケモンへの打点は概ね確保されています。")
        if combo_alerts:
            st.error(f"対策必須の並び: {', '.join(combo_alerts)}")
        else:
            st.write("強力な並びへの致命的な不利は検出されませんでした。")

        st.subheader("構築の書き出し")
        export_text = export_showdown(team)
        st.text_area("Showdown形式 (コピー用)", export_text, height=240)
        st.download_button("テキストをダウンロード", export_text, file_name="pokemon_team.txt")

        st.subheader("構築メモ")
        st.write(
            "弱点が重なるタイプは要注意。コンセプトに合わせて役割を補完すると構築が安定します。"
        )
