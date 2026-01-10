import streamlit as st


def apply_custom_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Orbitron:wght@500;600;700&display=swap');

:root {
  --bg: #0b0f1a;
  --panel: rgba(11, 18, 32, 0.72);
  --panel-border: rgba(0, 212, 255, 0.18);
  --accent: #00d4ff;
  --text: #e6f1ff;
  --muted: #94a3b8;
  --glass: rgba(255, 255, 255, 0.06);
  --glass-border: rgba(255, 255, 255, 0.1);
}

body {
  background: radial-gradient(circle at top, #0b1229 0%, #020617 55%, #020617 100%);
  color: var(--text);
  font-family: 'Inter', sans-serif;
}
.main { padding-top: 0.5rem; }
section[data-testid="stSidebar"] { background: #0a0e17; }

h1, h2, h3, h4, h5 {
  color: var(--text);
  font-family: 'Orbitron', sans-serif;
  letter-spacing: 0.04em;
}

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

.hero-section {
  position: relative;
  border-radius: 28px;
  padding: 2.5rem 2rem;
  overflow: hidden;
  background: rgba(2, 6, 23, 0.65);
  border: 1px solid var(--glass-border);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(20px);
  margin-bottom: 1.2rem;
}

.hero-bg {
  position: absolute;
  inset: -10%;
  background-size: cover;
  background-position: center;
  opacity: 0.22;
  filter: saturate(120%) blur(0px);
}

.hero-title {
  position: relative;
  font-size: 2.2rem;
  z-index: 1;
}

.hero-sub {
  position: relative;
  z-index: 1;
  color: var(--muted);
}

.glass-panel {
  background: var(--glass);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 1rem 1.2rem;
  backdrop-filter: blur(20px);
  box-shadow: inset 0 0 30px rgba(0, 212, 255, 0.08);
}

.pokemon-card {
  position: relative;
  border-radius: 24px;
  padding: 1rem 1.2rem;
  background: rgba(8, 15, 34, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(20px);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.pokemon-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 50px rgba(0, 212, 255, 0.25);
  border-color: rgba(0, 212, 255, 0.55);
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
  background: rgba(255, 255, 255, 0.08);
  overflow: hidden;
}

.stat-bar-fill {
  height: 100%;
  border-radius: 999px;
  filter: drop-shadow(0 0 6px rgba(0, 212, 255, 0.45));
  animation: statGlow 2.6s ease-in-out infinite;
}

.stat-bar-label {
  font-size: 0.78rem;
  color: var(--muted);
  margin-bottom: 0.2rem;
}

@keyframes statGlow {
  0% { opacity: 0.65; }
  50% { opacity: 1; }
  100% { opacity: 0.75; }
}

div[data-testid="stTabs"] button {
  background: rgba(15, 23, 42, 0.6) !important;
  color: var(--muted) !important;
  border-radius: 999px !important;
  padding: 0.5rem 1.2rem !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
  color: #e6f1ff !important;
  border-color: rgba(0, 212, 255, 0.7) !important;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.45);
}

.analysis-panel {
  background: rgba(8, 15, 34, 0.72);
  border: 1px solid rgba(0, 212, 255, 0.25);
  border-radius: 20px;
  padding: 1rem 1.2rem;
  box-shadow: inset 0 0 30px rgba(0, 212, 255, 0.1);
}
</style>
""",
        unsafe_allow_html=True,
    )
