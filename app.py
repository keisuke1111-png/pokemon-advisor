# VSCodeターミナルで実行:
# pip install streamlit pandas plotly
# streamlit run app.py

from datetime import datetime

import pandas as pd
import streamlit as st

from constants import (
    CONCEPTS,
    META_THREATS,
    META_TOP_POKEMON,
    NO_SELECTION,
    TEAM_SLOTS,
    TYPES,
    TYPE_EMOJI,
    UI_ICONS,
)
from logic import (
    BATTLE_LOGS_PATH,
    SAVED_TEAMS_PATH,
    battle_log_summary,
    build_personal_warning,
    build_speed_ranking,
    build_synergy_network,
    build_tactical_plans,
    calc_defensive_table,
    calc_offensive_table,
    calculate_balance_score,
    counter_candidates,
    calc_stat_max,
    detect_critical_vulnerabilities,
    detect_cores,
    estimate_survivability,
    evaluate_cycle_score,
    export_showdown,
    filter_pokemon_names,
    get_image_url,
    get_all_moves,
    get_type_css_class,
    get_types,
    has_new_mechanic,
    meta_pressure,
    meta_threat_levels,
    meta_warnings,
    offense_hint,
    load_json_list,
    load_pokemon_db,
    recommended_tera,
    render_stat_bar,
    render_type_badges,
    save_json_list,
    speed_target_check,
    build_speed_cards,
    suggest_complements,
    suggest_tera_solutions,
    sweep_support_status,
    tactical_review,
    table_to_plotly,
    team_role_balance,
    team_slots_from_members,
)
from styles import apply_custom_css


st.set_page_config(page_title="ポケモン構築サポーター", layout="wide", initial_sidebar_state="collapsed")
apply_custom_css()


st.title("ポケモン構築サポーター")
st.write("軸ポケモンを決め、補完枠や弱点をスマホで直感的にチェックできます。")

POKEMON_DB = load_pokemon_db()

if "saved_teams" not in st.session_state:
    st.session_state.saved_teams = load_json_list(SAVED_TEAMS_PATH)
if "battle_logs" not in st.session_state:
    st.session_state.battle_logs = load_json_list(BATTLE_LOGS_PATH)
if "team_slots" not in st.session_state:
    st.session_state.team_slots = team_slots_from_members([])


def sync_slot_state() -> None:
    base_slots = st.session_state.get("team_slots", team_slots_from_members([]))
    for idx, slot in enumerate(base_slots):
        st.session_state.setdefault(f"slot_{idx}_pokemon", slot["pokemon"])
        st.session_state.setdefault(f"slot_{idx}_nickname", slot["nickname"])
        st.session_state.setdefault(f"slot_{idx}_item", slot["item"])
        st.session_state.setdefault(f"slot_{idx}_tera", slot["tera"])
        st.session_state.setdefault(f"slot_{idx}_role", slot["role"])


sync_slot_state()

team_slots = []
for idx in range(TEAM_SLOTS):
    team_slots.append(
        {
            "pokemon": st.session_state.get(f"slot_{idx}_pokemon", NO_SELECTION),
            "nickname": st.session_state.get(f"slot_{idx}_nickname", ""),
            "item": st.session_state.get(f"slot_{idx}_item", ""),
            "tera": st.session_state.get(f"slot_{idx}_tera", ""),
            "role": st.session_state.get(f"slot_{idx}_role", ""),
        }
    )
st.session_state.team_slots = team_slots
team = [slot["pokemon"] for slot in team_slots if slot["pokemon"] != NO_SELECTION]

hero_name = team[0] if team else None
hero_image = get_image_url(POKEMON_DB[hero_name]) if hero_name else ""
hero_title = "Pokemon Build Studio"
hero_sub = "プロフェッショナル・ライトモード構築ダッシュボード"
hero_bg = f"background-image: url('{hero_image}');" if hero_image else ""
st.markdown(
    f"""
<div class="hero-section">
  <div class="hero-bg" style="{hero_bg}"></div>
  <div class="hero-title">{hero_title}</div>
  <div class="hero-sub">{hero_sub}</div>
</div>
""",
    unsafe_allow_html=True,
)


with st.sidebar:
    st.header("構築設定")
    st.write("大量データ向けに検索フィルタを用意しました。")
    search_filter = st.text_input("検索フィルタ", "")
    st.header("構築コンセプト")
    concept = st.selectbox("コンセプト", list(CONCEPTS.keys()), key="concept_select")
    st.header("役割の希望")
    roles_needed = st.multiselect(
        "必要な役割",
        ["エース", "クッション", "スイーパー", "起点作成", "サポート", "ブレイカー", "受け", "ストッパー", "サイクル", "トリックルーム"],
    )
    st.header("環境対策")
    meta_focus = st.multiselect("意識したい環境", list(META_THREATS.keys()))
    st.header("Sライン補正")
    speed_nature = st.selectbox("性格補正 (S)", ["無補正", "ようき", "おくびょう", "ゆうかん"])

    st.header("構築の保存/呼び出し")
    team_name = st.text_input("保存名", "")
    st.text_area("メモ", height=80, key="memo_input")
    save_clicked = st.button("構築を保存")
    if save_clicked:
        current_slots = st.session_state.get("team_slots", team_slots_from_members([]))
        team_data = {
            "name": team_name or f"未命名-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "members": [slot for slot in current_slots if slot["pokemon"] != NO_SELECTION],
            "concept": st.session_state.get("concept_select", concept),
            "memo": st.session_state.get("memo_input", ""),
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
            loaded_slots = team_slots_from_members(team_data.get("members", []))
            st.session_state.team_slots = loaded_slots
            for idx, slot in enumerate(loaded_slots):
                st.session_state[f"slot_{idx}_pokemon"] = slot["pokemon"]
                st.session_state[f"slot_{idx}_nickname"] = slot["nickname"]
                st.session_state[f"slot_{idx}_item"] = slot["item"]
                st.session_state[f"slot_{idx}_tera"] = slot["tera"]
                st.session_state[f"slot_{idx}_role"] = slot["role"]
            st.session_state.concept_select = team_data.get("concept", concept)
            st.session_state.memo_input = team_data.get("memo", "")
            st.rerun()

concept = st.session_state.get("concept_select", concept)


tabs = st.tabs(["構築", "相性表", "メタ対策", "Sライン", "戦績ログ"])

with tabs[0]:
    st.subheader("パーティ構築")
    st.write(CONCEPTS[concept])

    filtered_names = filter_pokemon_names(POKEMON_DB, search_filter)
    slot_options_base = [NO_SELECTION] + filtered_names

    slot_cols = st.columns(2)
    for idx in range(TEAM_SLOTS):
        with slot_cols[idx % 2]:
            st.markdown(f"### スロット {idx + 1}")
            current_pokemon = st.session_state.get(f"slot_{idx}_pokemon", NO_SELECTION)
            options = slot_options_base
            if current_pokemon not in options:
                options = [current_pokemon] + options
            st.selectbox("ポケモン", options, key=f"slot_{idx}_pokemon")

            selected_pokemon = st.session_state.get(f"slot_{idx}_pokemon", NO_SELECTION)
            if selected_pokemon != NO_SELECTION:
                info = POKEMON_DB[selected_pokemon]
                st.image(get_image_url(info), width=96)
                st.caption(f"タイプ: {', '.join(get_types(info))}")
                st.text_input(
                    "持ち物",
                    key=f"slot_{idx}_item",
                    placeholder=", ".join(info.get("recommended_items", [])),
                )
                tera_options = ["未設定"] + TYPES
                current_tera = st.session_state.get(f"slot_{idx}_tera", "未設定") or "未設定"
                if current_tera not in tera_options:
                    tera_options = ["未設定", current_tera] + TYPES
                tera_index = tera_options.index(current_tera) if current_tera in tera_options else 0
                st.selectbox("テラスタイプ", tera_options, index=tera_index, key=f"slot_{idx}_tera")

    team = [slot["pokemon"] for slot in st.session_state.team_slots if slot["pokemon"] != NO_SELECTION]
    if not team:
        st.info("まずはポケモンを1体選んでください。")
    else:
        st.write(f"現在のメンバー数: {len(team)} / 6")
        cols = st.columns(3)
        for idx, slot in enumerate(st.session_state.team_slots):
            name = slot["pokemon"]
            if name == NO_SELECTION:
                continue
            info = POKEMON_DB[name]
            badges = render_type_badges(get_types(info))
            extra_badge = " <span class='badge' style='background:#3B82F6;'>NEW</span>" if has_new_mechanic(info) else ""
            watermark = TYPE_EMOJI.get(get_types(info)[0], "")
            image_url = get_image_url(info)
            item = slot["item"].strip() or (info["recommended_items"][0] if info["recommended_items"] else "未設定")
            tera = slot["tera"].strip() or (recommended_tera(info)[0] if recommended_tera(info) else "未設定")
            role = ", ".join(info["role_labels"])
            moves = get_all_moves(info)
            stats = info["stats"]
            speed_actual = calc_stat_max(stats["S"], speed_nature, "S")
            card_title = name
            type_class = get_type_css_class(info)
            stat_rows = "".join(
                [
                    render_stat_bar(stats["H"], "HP"),
                    render_stat_bar(stats["A"], "ATK"),
                    render_stat_bar(stats["B"], "DEF"),
                    render_stat_bar(stats["C"], "SPA"),
                    render_stat_bar(stats["D"], "SPD"),
                    render_stat_bar(stats["S"], "SPE"),
                ]
            )
            card_html = (
                f'<div class="pokemon-card {type_class}">'
                f'<div class="type-watermark">{watermark}</div>'
                f'<div class="pokemon-card-header">'
                f'  <div class="card-image"><img src="{image_url}" alt="{name}"/></div>'
                f'  <div>'
                f'    <div class="card-title">{card_title} {extra_badge}</div>'
                f'    <div>{badges}</div>'
                f'  </div>'
                f'</div>'
                f'<div class="divider"></div>'
                f'<div class="card-meta">{UI_ICONS["role"]} 役割: {role}</div>'
                f'<div class="card-meta">{UI_ICONS["ability"]} 特性: {", ".join(info["abilities"])}</div>'
                f'<div class="card-meta">{UI_ICONS["item"]} 持ち物: {item}</div>'
                f'<div class="card-meta">{UI_ICONS["speed"]} S実数値: {speed_actual}</div>'
                f'<div class="card-meta">テラ: {tera}</div>'
                f'<div class="card-meta">主要技: {", ".join(moves[:3])}</div>'
                f'<div class="divider"></div>'
                f'{stat_rows}'
                f'<div class="divider"></div>'
                f'<div class="card-meta">{offense_hint(info)}</div>'
                f'</div>'
            )
            with cols[idx % 3]:
                st.markdown(card_html, unsafe_allow_html=True)

        st.subheader("戦術プラン")
        plans = build_tactical_plans(team, POKEMON_DB)
        if plans:
            plan_items = "".join([f"<div>• {p}</div>" for p in plans])
            st.markdown(
                f"""
<div class="analysis-panel">
  <div style="font-weight:600; margin-bottom:0.5rem;">AI分析中...</div>
  {plan_items}
</div>
""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
<div class="analysis-panel">
  <div style="font-weight:600; margin-bottom:0.5rem;">AI分析中...</div>
  <div>現時点では明確な勝ち筋が不足しています。起点作成やエースを追加してください。</div>
</div>
""",
                unsafe_allow_html=True,
            )

        st.subheader("補完候補")
        suggestions = suggest_complements(team, roles_needed, meta_focus, concept, POKEMON_DB)
        if not suggestions:
            st.write("条件に合う候補が見つかりませんでした。")
        else:
            option_map = {f"{s['name']} (理由: {', '.join(s['reasons'])})": s for s in suggestions}
            selected = st.radio("候補を選択", list(option_map.keys()))
            info = POKEMON_DB[option_map[selected]["name"]]
            st.write(f"推奨テラスタイプ: {', '.join(recommended_tera(info))}")
            st.write(f"採用理由: {', '.join(option_map[selected]['reasons'])}")

        st.subheader("ロールバランスチェック")
        role_counts, missing_roles = team_role_balance(team, POKEMON_DB)
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
        def_table = calc_defensive_table(team, POKEMON_DB)
        off_table = calc_offensive_table(team, POKEMON_DB)
        st.plotly_chart(table_to_plotly(def_table, "防御相性"), use_container_width=True)
        st.plotly_chart(table_to_plotly(off_table, "攻撃相性"), use_container_width=True)
        st.subheader("相性ネットワーク")
        st.plotly_chart(build_synergy_network(team, POKEMON_DB), use_container_width=True)

with tabs[2]:
    st.subheader("メタ対策")
    if not team:
        st.info("メンバーを選択するとメタ対策が表示されます。")
    else:
        st.write("環境上位への対策状況をダッシュボードで可視化します。")
        threat_rows = meta_threat_levels(team, POKEMON_DB)
        panels = []
        for row in threat_rows:
            counters = counter_candidates(team, META_TOP_POKEMON[row["name"]], POKEMON_DB)
            counter_text = ", ".join(counters[:3]) if counters else "不足"
            panels.append(
                f"""
<div class="threat-card {row["level"]}">
  <div class="threat-title">{row["name"]}</div>
  <div class="threat-meta">弱点: {row["weak"]} / 耐性: {row["resist"]} / 無効: {row["immune"]}</div>
  <div class="threat-gauge">
    <div class="threat-fill level-{row["level"]}" style="width:{min(100, row["score"] * 40 + 10)}%;"></div>
  </div>
  <div class="threat-foot">対策候補: {counter_text}</div>
</div>
"""
            )
        st.markdown('<div class="analysis-grid">' + "".join(panels) + "</div>", unsafe_allow_html=True)

        warnings = meta_pressure(team, POKEMON_DB)
        if warnings:
            alert_items = "".join([f"<div class='alert-chip'>{w}</div>" for w in warnings])
            st.markdown(f"<div class='alert-row'>{alert_items}</div>", unsafe_allow_html=True)

        missing_coverage, combo_alerts = meta_warnings(team, POKEMON_DB)
        if missing_coverage or combo_alerts:
            missing_html = ""
            if missing_coverage:
                missing_html = "".join([f"<span class='badge badge-warn'>{n}</span>" for n in missing_coverage])
            combo_html = ""
            if combo_alerts:
                combo_html = "".join([f"<span class='badge badge-alert'>{n}</span>" for n in combo_alerts])
            st.markdown(
                f"""
<div class="analysis-panel">
  <div class="panel-title">要注意シグナル</div>
  <div class="panel-line">打点不足: {missing_html or "なし"}</div>
  <div class="panel-line">危険コンボ: {combo_html or "なし"}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        personal_warning = build_personal_warning(st.session_state.battle_logs, team, POKEMON_DB)
        if personal_warning:
            st.markdown(f"<div class='alert-banner'>{personal_warning}</div>", unsafe_allow_html=True)

with tabs[3]:
    st.subheader("Sライン")
    if not team:
        st.info("メンバーを選択するとSラインが表示されます。")
    else:
        st.write("パーティ内Sラインをビジュアルで確認できます。")
        speed_cards = build_speed_cards(team, POKEMON_DB, speed_nature)
        speed_items = []
        for card in speed_cards:
            badge = "<span class='speed-badge'>最速</span>" if card["is_fastest"] else ""
            speed_items.append(
                f"""
<div class="speed-card">
  <div class="speed-title">{card["name"]} {badge}</div>
  <div class="speed-meta">{card["type"]} / S種族値 {card["base"]} / 実数 {card["actual"]}</div>
  <div class="speed-track">
    <div class="speed-fill" style="width:{int(card["ratio"] * 100)}%;"></div>
  </div>
</div>
"""
            )
        st.markdown('<div class="speed-grid">' + "".join(speed_items) + "</div>", unsafe_allow_html=True)

        speed_checks = speed_target_check(team, POKEMON_DB, speed_nature)
        timeline_items = []
        for target, data in speed_checks.items():
            state = "ok" if data["ok"] else "ng"
            label = "クリア" if data["ok"] else "未達"
            timeline_items.append(
                f"""
<div class="timeline-item {state}">
  <div class="timeline-dot"></div>
  <div class="timeline-body">
    <div class="timeline-title">{target}</div>
    <div class="timeline-meta">目安 {data["target"]} · {label}</div>
  </div>
</div>
"""
            )
        st.markdown('<div class="timeline">' + "".join(timeline_items) + "</div>", unsafe_allow_html=True)

    st.subheader("全ポケモンSライン比較")
    st.write("性格補正込みの最速実数値でランキング表示します。")
    speed_query = st.text_input("名前で絞り込み", "", key="speed_query")
    speed_limit = st.slider("表示件数", 20, 200, 60, step=20)
    speed_df = build_speed_ranking(POKEMON_DB, speed_nature)
    if speed_query:
        speed_df = speed_df[speed_df["ポケモン"].str.contains(speed_query)]
    ranked = speed_df.head(speed_limit)
    speed_rows = []
    max_val = ranked["S最大実数"].max() if not ranked.empty else 0
    for _, row in ranked.iterrows():
        ratio = 0 if max_val == 0 else row["S最大実数"] / max_val
        speed_rows.append(
            f"""
<div class="speed-rank-card">
  <div class="speed-rank-title">{row["ポケモン"]}</div>
  <div class="speed-rank-meta">{row["タイプ"]} · S種族値 {row["S種族値"]} · 実数 {row["S最大実数"]}</div>
  <div class="speed-track">
    <div class="speed-fill" style="width:{int(ratio * 100)}%;"></div>
  </div>
</div>
"""
        )
    st.markdown('<div class="speed-rank-grid">' + "".join(speed_rows) + "</div>", unsafe_allow_html=True)

    st.subheader("構築の書き出し")
    export_text = export_showdown(team, POKEMON_DB)
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
            risk_cards = []
            top_count = ranking[0][1]
            for name, count in ranking[:10]:
                ratio = 0 if top_count == 0 else count / top_count
                risk_cards.append(
                    f"""
<div class="risk-card">
  <div class="risk-title">{name}</div>
  <div class="risk-meta">被害回数: {count}</div>
  <div class="risk-track">
    <div class="risk-fill" style="width:{int(ratio * 100)}%;"></div>
  </div>
</div>
"""
                )
            st.markdown('<div class="risk-grid">' + "".join(risk_cards) + "</div>", unsafe_allow_html=True)
        else:
            st.write("まだ負け試合の記録がありません。")

        st.subheader("戦績データの出力")
        df_logs = pd.DataFrame(st.session_state.battle_logs)
        csv_data = df_logs.to_csv(index=False)
        st.download_button("CSVをダウンロード", csv_data, file_name="battle_logs.csv")

st.subheader("AI戦術参謀のレポート")
if not team:
    st.info("パーティを選択するとAIが戦術レポートを提示します。")
else:
    score_pack = calculate_balance_score(team, POKEMON_DB)
    sweep_status = sweep_support_status(team, POKEMON_DB)
    critical = detect_critical_vulnerabilities(team, POKEMON_DB)
    cores = detect_cores(team, POKEMON_DB)
    cycle_score = evaluate_cycle_score(team, POKEMON_DB)
    survivals = estimate_survivability(team, POKEMON_DB)
    tera_solutions = suggest_tera_solutions(team, POKEMON_DB)
    review = tactical_review(team, POKEMON_DB)

    score_value = score_pack["score"]
    if score_value >= 80:
        score_color = "#2563EB"
    elif score_value >= 60:
        score_color = "#F59E0B"
    else:
        score_color = "#EF4444"
    strengths = score_pack["strengths"] or ["即戦力の尖りはまだ未確定"]
    weaknesses = score_pack["weaknesses"] or ["致命的な弱点は見当たりません"]
    core_labels = [c["name"] for c in cores] or ["未検出"]

    strengths_html = "".join([f"<span class='badge badge-good'>{s}</span>" for s in strengths])
    weaknesses_html = "".join([f"<span class='alert-badge'>{w}</span>" for w in weaknesses])
    cores_html = "".join([f"<span class='badge badge-core'>{c}</span>" for c in core_labels])

    sweep_text = " / ".join(sweep_status["sweepers"]) if sweep_status["sweepers"] else "未確定"
    support_text = "起点作成あり" if sweep_status["has_setup"] else "起点作成不足"
    critical_text = " / ".join([c["name"] for c in critical]) if critical else "なし"

    st.markdown(
        f"""
<div class="ai-panel">
  <div class="ai-header">
    <div class="ai-title">AI戦術参謀 · 思考中...</div>
    <div class="ai-sub">構築の意図と環境メタを照合しています。</div>
  </div>
  <div class="ai-grid">
    <div class="ai-card">
      <div class="ai-card-title">総合バランススコア</div>
      <div class="score-ring" style="--score:{score_value}; --score-color:{score_color};">
        <div class="score-value">{score_value}</div>
        <div class="score-label">/ 100</div>
      </div>
    </div>
    <div class="ai-card">
      <div class="ai-card-title">抜き性能チェック</div>
      <div class="ai-line">スイーパー: {sweep_text}</div>
      <div class="ai-line">サポート: {support_text}</div>
      <div class="ai-line">致命的な脆弱性: {critical_text}</div>
    </div>
    <div class="ai-card">
      <div class="ai-card-title">コア認識</div>
      <div class="ai-badges">{cores_html}</div>
    </div>
  </div>
  <div class="ai-footer">
    <div class="ai-card-title">結論</div>
    <div class="ai-badges">{strengths_html}</div>
    <div class="ai-badges warn">{weaknesses_html}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.subheader("タクティカル・レビュー")
    if not review["alerts"]:
        st.markdown("<div class='insight-card good'>大きな警告はありません。戦術の完成度が高いです。</div>", unsafe_allow_html=True)
    else:
        alert_html = "".join([f"<span class='alert-badge'>{a}</span>" for a in review["alerts"]])
        reason_html = "".join([f"<div class='insight-line'>{r}</div>" for r in review["reasons"]])
        st.markdown(
            f"""
<div class="insight-card">
  <div class="insight-title">プロ視点の警告</div>
  <div class="insight-badges">{alert_html}</div>
  {reason_html}
</div>
""",
            unsafe_allow_html=True,
        )

    st.subheader("勝利へのシナリオ")
    if review["wins"]:
        wins_html = "".join([f"<div class='scenario-step'>• {w}</div>" for w in review["wins"]])
        st.markdown(
            f"""
<div class="scenario-card">
  <div class="insight-title">推奨ルート</div>
  {wins_html}
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='scenario-card'>起点作成役と勝ち筋の連携が不足しています。</div>",
            unsafe_allow_html=True,
        )

    st.subheader("対面操作の評価")
    pivots_text = ", ".join(cycle_score["pivot_names"]) if cycle_score["pivot_names"] else "なし"
    cushions_text = ", ".join(cycle_score["cushions"]) if cycle_score["cushions"] else "なし"
    st.markdown(
        f"""
<div class="insight-card">
  <div class="insight-title">サイクル評価: {cycle_score["label"]}</div>
  <div class="insight-line">入れ替え技: {pivots_text}</div>
  <div class="insight-line">受け出し要員: {cushions_text}</div>
  <div class="insight-meter">
    <div class="insight-fill" style="width:{cycle_score["score"]}%;"></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if tera_solutions:
        st.subheader("テラスタル解決案")
        tera_rows = []
        for s in tera_solutions:
            cands = " / ".join(s["candidates"])
            tera_rows.append(
                f"<div class='tera-card'>弱点 {s['weak_type']} → {s['tera']}テラス提案 ({cands})</div>"
            )
        st.markdown("<div class='tera-grid'>" + "".join(tera_rows) + "</div>", unsafe_allow_html=True)

    if survivals:
        st.subheader("耐久ラインの論理判定")
        verdicts = []
        for row in survivals:
            verdicts.append(
                f"<div class='survive-card {row['verdict']}'>{row['name']} vs {row['threat']}: {row['verdict']}</div>"
            )
        st.markdown("<div class='survive-grid'>" + "".join(verdicts) + "</div>", unsafe_allow_html=True)
