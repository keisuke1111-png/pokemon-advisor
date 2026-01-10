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
  --hero-glow-1: rgba(59, 130, 246, 0.16);
  --hero-glow-2: rgba(34, 197, 94, 0.12);
  --hero-glow-3: rgba(249, 115, 22, 0.12);
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
  transform-style: preserve-3d;
  perspective: 800px;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.card:hover {
  transform: translateY(-4px) rotateX(2deg) rotateY(-2deg);
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
  background: linear-gradient(120deg, var(--hero-glow-1), var(--hero-glow-2), var(--hero-glow-3));
  background-size: 300% 300%;
  border: 1px solid var(--panel-border);
  box-shadow: var(--shadow);
  margin-bottom: 1.2rem;
  isolation: isolate;
  animation: heroShift 18s ease-in-out infinite;
}

.hero-section::before {
  content: "";
  position: absolute;
  inset: -60% -40%;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.12), transparent 40%),
    radial-gradient(circle at 80% 40%, rgba(56, 189, 248, 0.12), transparent 45%),
    radial-gradient(circle at 30% 80%, rgba(34, 197, 94, 0.12), transparent 50%);
  opacity: 0.7;
  animation: patternDrift 28s linear infinite;
  z-index: 0;
  pointer-events: none;
}

.hero-bg {
  position: absolute;
  inset: -10%;
  background-size: cover;
  background-position: center;
  opacity: 0.06;
  filter: saturate(110%);
  animation: heroFloat 20s ease-in-out infinite;
  z-index: 0;
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
  border: 1px solid var(--type-color, var(--panel-border));
  box-shadow: var(--shadow);
  transform-style: preserve-3d;
  perspective: 900px;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.pokemon-card:hover {
  transform: translateY(-4px) rotateX(2deg) rotateY(-2deg);
  box-shadow: var(--shadow-hover), 0 18px 38px var(--type-glow, rgba(148, 163, 184, 0.16));
  border-color: var(--type-color, #CBD5E1);
}

.pokemon-card-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.pokemon-card .card-image {
  position: relative;
  overflow: visible;
}

.pokemon-card .card-image img {
  width: 84px;
  height: 84px;
  object-fit: contain;
  transition: transform 0.2s ease;
}

.pokemon-card:hover .card-image img {
  transform: translateY(-4px) scale(1.08);
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

.ai-panel {
  margin-top: 1rem;
  padding: 1.2rem 1.4rem;
  border-radius: 22px;
  background: #FFFFFF;
  border: 1px solid var(--panel-border);
  box-shadow: var(--shadow);
}

.ai-header {
  margin-bottom: 1rem;
}

.ai-title {
  font-weight: 700;
  font-size: 1.05rem;
}

.ai-sub {
  color: var(--muted);
  font-size: 0.88rem;
}

.ai-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.ai-card {
  border-radius: 18px;
  padding: 1rem 1.1rem;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
}

.ai-card-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.ai-line {
  color: var(--muted);
  font-size: 0.88rem;
  margin-bottom: 0.35rem;
}

.ai-footer .ai-card-title {
  margin-bottom: 0.6rem;
}

.ai-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 0.5rem;
}

.ai-badges.warn {
  margin-top: 0.4rem;
}

.score-ring {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: conic-gradient(var(--score-color, #3B82F6) calc(var(--score) * 1%), #E2E8F0 0);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin: 0.6rem auto 0;
}

.score-ring::after {
  content: "";
  position: absolute;
  inset: 12px;
  background: #FFFFFF;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px #E2E8F0;
}

.score-value {
  position: relative;
  font-size: 1.6rem;
  font-weight: 700;
  z-index: 1;
}

.score-label {
  position: relative;
  font-size: 0.8rem;
  color: var(--muted);
  z-index: 1;
  margin-top: -0.4rem;
}

.badge-good {
  background: #22C55E;
  color: #FFFFFF;
}

.badge-core {
  background: #3B82F6;
  color: #FFFFFF;
}

.alert-badge {
  background: #FEE2E2;
  color: #B91C1C;
  border-radius: 999px;
  padding: 0.2rem 0.6rem;
  font-weight: 700;
  font-size: 0.78rem;
  animation: badgePulse 2.6s ease-in-out infinite;
  box-shadow: 0 0 0 rgba(239, 68, 68, 0.2);
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.9rem;
  margin-top: 0.6rem;
}

.threat-card {
  border-radius: 16px;
  padding: 0.9rem 1rem;
  border: 1px solid var(--panel-border);
  background: #FFFFFF;
  box-shadow: var(--shadow);
}

.threat-title {
  font-weight: 700;
  font-size: 1rem;
}

.threat-meta {
  color: var(--muted);
  font-size: 0.82rem;
  margin: 0.2rem 0 0.6rem;
}

.threat-gauge {
  height: 8px;
  background: #E2E8F0;
  border-radius: 999px;
  overflow: hidden;
}

.threat-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.3s ease;
}

.threat-foot {
  color: var(--muted);
  font-size: 0.82rem;
  margin-top: 0.6rem;
}

.level-low .threat-fill { background: linear-gradient(90deg, #22C55E, #86EFAC); }
.level-mid .threat-fill { background: linear-gradient(90deg, #F59E0B, #FCD34D); }
.level-high .threat-fill { background: linear-gradient(90deg, #EF4444, #FCA5A5); }

.alert-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.8rem 0;
}

.alert-chip {
  background: #FEF3C7;
  color: #92400E;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge-warn {
  background: #F59E0B;
  color: #FFFFFF;
}

.badge-alert {
  background: #EF4444;
  color: #FFFFFF;
}

.panel-title {
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.panel-line {
  color: var(--muted);
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
}

.alert-banner {
  margin-top: 0.9rem;
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #991B1B;
  padding: 0.8rem 1rem;
  border-radius: 14px;
  font-weight: 600;
}

.speed-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.9rem;
  margin-top: 0.6rem;
}

.speed-card {
  border-radius: 16px;
  padding: 0.9rem 1rem;
  border: 1px solid var(--panel-border);
  background: #FFFFFF;
  box-shadow: var(--shadow);
}

.speed-title {
  font-weight: 700;
  font-size: 0.98rem;
}

.speed-meta {
  color: var(--muted);
  font-size: 0.82rem;
  margin: 0.2rem 0 0.6rem;
}

.speed-track {
  height: 8px;
  background: #E2E8F0;
  border-radius: 999px;
  overflow: hidden;
}

.speed-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #3B82F6, #93C5FD);
}

.speed-badge {
  display: inline-block;
  margin-left: 0.35rem;
  padding: 0.1rem 0.5rem;
  border-radius: 999px;
  font-size: 0.7rem;
  background: #DBEAFE;
  color: #1D4ED8;
  font-weight: 700;
}

.timeline {
  margin-top: 1rem;
  padding: 0.4rem 0.2rem;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  margin-bottom: 0.7rem;
}

.timeline-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 0.35rem;
  background: #94A3B8;
}

.timeline-item.ok .timeline-dot { background: #22C55E; }
.timeline-item.ng .timeline-dot { background: #EF4444; }

.timeline-title {
  font-weight: 700;
}

.timeline-meta {
  color: var(--muted);
  font-size: 0.82rem;
}

.risk-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.9rem;
  margin-top: 0.6rem;
}

.risk-card {
  border-radius: 16px;
  padding: 0.9rem 1rem;
  border: 1px solid var(--panel-border);
  background: #FFFFFF;
  box-shadow: var(--shadow);
}

.risk-title {
  font-weight: 700;
}

.risk-meta {
  color: var(--muted);
  font-size: 0.82rem;
  margin: 0.2rem 0 0.6rem;
}

.risk-track {
  height: 8px;
  background: #E2E8F0;
  border-radius: 999px;
  overflow: hidden;
}

.risk-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #EF4444, #FCA5A5);
}

.speed-rank-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 0.9rem;
  margin-top: 0.6rem;
}

.speed-rank-card {
  border-radius: 16px;
  padding: 0.9rem 1rem;
  border: 1px solid var(--panel-border);
  background: #FFFFFF;
  box-shadow: var(--shadow);
}

.speed-rank-title {
  font-weight: 700;
}

.speed-rank-meta {
  color: var(--muted);
  font-size: 0.82rem;
  margin: 0.2rem 0 0.6rem;
}

@keyframes heroShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes patternDrift {
  0% { transform: translate3d(-2%, -2%, 0); }
  50% { transform: translate3d(2%, 3%, 0); }
  100% { transform: translate3d(-2%, -2%, 0); }
}

@keyframes heroFloat {
  0% { transform: translate3d(0, 0, 0); }
  50% { transform: translate3d(1%, -1%, 0); }
  100% { transform: translate3d(0, 0, 0); }
}

@keyframes badgePulse {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.2); }
  70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0.0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.0); }
}

.card-normal { --type-color: #9CA3AF; --type-glow: rgba(156, 163, 175, 0.2); }
.card-fire { --type-color: #F97316; --type-glow: rgba(249, 115, 22, 0.22); }
.card-water { --type-color: #3B82F6; --type-glow: rgba(59, 130, 246, 0.22); }
.card-electric { --type-color: #F59E0B; --type-glow: rgba(245, 158, 11, 0.22); }
.card-grass { --type-color: #22C55E; --type-glow: rgba(34, 197, 94, 0.2); }
.card-ice { --type-color: #38BDF8; --type-glow: rgba(56, 189, 248, 0.2); }
.card-fighting { --type-color: #EF4444; --type-glow: rgba(239, 68, 68, 0.2); }
.card-poison { --type-color: #A855F7; --type-glow: rgba(168, 85, 247, 0.2); }
.card-ground { --type-color: #D97706; --type-glow: rgba(217, 119, 6, 0.2); }
.card-flying { --type-color: #60A5FA; --type-glow: rgba(96, 165, 250, 0.2); }
.card-psychic { --type-color: #EC4899; --type-glow: rgba(236, 72, 153, 0.2); }
.card-bug { --type-color: #84CC16; --type-glow: rgba(132, 204, 22, 0.2); }
.card-rock { --type-color: #B45309; --type-glow: rgba(180, 83, 9, 0.2); }
.card-ghost { --type-color: #8B5CF6; --type-glow: rgba(139, 92, 246, 0.2); }
.card-dragon { --type-color: #2563EB; --type-glow: rgba(37, 99, 235, 0.2); }
.card-dark { --type-color: #64748B; --type-glow: rgba(100, 116, 139, 0.2); }
.card-steel { --type-color: #94A3B8; --type-glow: rgba(148, 163, 184, 0.2); }
.card-fairy { --type-color: #F472B6; --type-glow: rgba(244, 114, 182, 0.2); }
</style>
""",
        unsafe_allow_html=True,
    )
