import streamlit as st


def apply_custom_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&display=swap');

:root {
  --bg: #F8FAFC;
  --panel: #FFFFFF;
  --panel-border: #E2E8F0;
  --accent: #3B82F6;
  --text: #1E293B;
  --muted: #64748B;
  --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  --shadow-hover: 0 16px 36px rgba(15, 23, 42, 0.12);
}

body {
  background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
  color: var(--text);
  font-family: 'Inter', 'Noto Sans JP', sans-serif;
}
.main { padding-top: 0.75rem; }
section[data-testid="stSidebar"] {
  background: #F8FAFC;
  border-right: 1px solid var(--panel-border);
}

h1, h2, h3, h4, h5 {
  color: var(--text);
  font-family: 'Inter', 'Noto Sans JP', sans-serif;
  letter-spacing: 0.01em;
}

.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, #CBD5F5, transparent);
  margin: 0.75rem 0;
}

.card {
  position: relative;
  padding: 0.9rem 1rem;
  border-radius: 16px;
  background: var(--panel);
  border: 1px solid var(--panel-border);
  box-shadow: var(--shadow);
  margin-bottom: 0.9rem;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-hover);
  border-color: #CBD5E1;
}

.card-title {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.card-meta {
  color: var(--muted);
  font-size: 0.9rem;
}

.card-image {
  width: 96px;
  height: 96px;
  border-radius: 12px;
  background: #F1F5F9;
  border: 1px solid var(--panel-border);
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
  opacity: 0.08;
}

.badge {
  display: inline-block;
  padding: 0.18rem 0.55rem;
  border-radius: 999px;
  color: #FFFFFF;
  font-size: 0.78rem;
  font-weight: 700;
  margin-right: 0.25rem;
  box-shadow: inset 0 -2px 0 rgba(0,0,0,0.08);
}

div[data-testid="stSelectbox"] > div, div[data-testid="stMultiSelect"] > div {
  font-size: 1.05rem;
}

div.stButton > button {
  font-size: 1.05rem;
  padding: 0.7rem 1.1rem;
  border-radius: 12px;
  border: 1px solid var(--accent);
  background: var(--accent);
  color: #FFFFFF;
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.2);
}

div.stButton > button:hover {
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.25);
  transform: translateY(-1px);
}

.hero-section {
  position: relative;
  border-radius: 24px;
  padding: 2.2rem 2rem;
  overflow: hidden;
  background: var(--panel);
  border: 1px solid var(--panel-border);
  box-shadow: var(--shadow);
  margin-bottom: 1.2rem;
}

.hero-bg {
  position: absolute;
  inset: -10%;
  background-size: cover;
  background-position: center;
  opacity: 0.06;
  filter: saturate(110%);
}

.hero-title {
  position: relative;
  font-size: 2.1rem;
  z-index: 1;
}

.hero-sub {
  position: relative;
  z-index: 1;
  color: var(--muted);
}

.glass-panel {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: 20px;
  padding: 1rem 1.2rem;
  box-shadow: var(--shadow);
}

.pokemon-card {
  position: relative;
  border-radius: 20px;
  padding: 1rem 1.2rem;
  background: var(--panel);
  border: 1px solid var(--panel-border);
  box-shadow: var(--shadow);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.pokemon-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-hover);
  border-color: #CBD5E1;
}

.pokemon-card-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.pokemon-card img {
  width: 84px;
  height: 84px;
  object-fit: contain;
}

.stat-bar {
  position: relative;
  height: 10px;
  border-radius: 999px;
  background: #E2E8F0;
  overflow: hidden;
}

.stat-bar-fill {
  height: 100%;
  border-radius: 999px;
}

.stat-bar-label {
  font-size: 0.78rem;
  color: var(--muted);
  margin-bottom: 0.2rem;
}

div[data-testid="stTabs"] button {
  background: #F1F5F9 !important;
  color: var(--muted) !important;
  border-radius: 999px !important;
  padding: 0.5rem 1.2rem !important;
  border: 1px solid var(--panel-border) !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--text) !important;
  border-color: #93C5FD !important;
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.18);
  background: #FFFFFF !important;
}

.analysis-panel {
  background: #F8FAFC;
  border: 1px solid var(--panel-border);
  border-radius: 18px;
  padding: 1rem 1.2rem;
  box-shadow: var(--shadow);
}
</style>
""",
        unsafe_allow_html=True,
    )
