import streamlit as st


def apply_custom_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Impact&family=M+PLUS+Rounded+1c:wght@500;700;800&display=swap');

:root {
  --bg: #0B0F2A;
  --panel: #12183A;
  --panel-border: rgba(255, 215, 0, 0.5);
  --accent: #FFB800;
  --text: #F8FAFF;
  --muted: rgba(248, 250, 255, 0.72);
  --shadow: 0 16px 30px rgba(0, 0, 0, 0.45);
  --shadow-hover: 0 24px 40px rgba(0, 0, 0, 0.55);
  --hero-glow-1: rgba(255, 184, 0, 0.35);
  --hero-glow-2: rgba(0, 212, 255, 0.25);
  --hero-glow-3: rgba(255, 61, 87, 0.22);
}

body {
  background:
    radial-gradient(circle at center, rgba(255, 184, 0, 0.2), transparent 55%),
    radial-gradient(circle at 20% 30%, rgba(0, 212, 255, 0.18), transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 61, 87, 0.2), transparent 45%),
    #0B0F2A;
  color: var(--text);
  font-family: 'M PLUS Rounded 1c', sans-serif;
}
.main { padding-top: 0.75rem; }
section[data-testid="stSidebar"] {
  background: rgba(11, 15, 42, 0.95);
  border-right: 1px solid rgba(255, 215, 0, 0.3);
}

h1, h2, h3, h4, h5 {
  color: #FFF5CC;
  font-family: 'Impact', 'M PLUS Rounded 1c', sans-serif;
  letter-spacing: 0.03em;
  font-style: italic;
  text-shadow: 0 6px 18px rgba(0,0,0,0.6);
  -webkit-text-stroke: 1px rgba(0,0,0,0.5);
}

.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.8), transparent);
  margin: 0.75rem 0;
}

.card {
  position: relative;
  padding: 0.9rem 1rem;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(30, 35, 70, 0.95), rgba(18, 24, 58, 0.95));
  border: 1px solid rgba(255, 215, 0, 0.6);
  box-shadow: var(--shadow);
  margin-bottom: 0.9rem;
  transform-style: preserve-3d;
  perspective: 800px;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.card:hover {
  transform: translateY(-4px) rotateX(2deg) rotateY(-2deg);
  box-shadow: var(--shadow-hover);
  border-color: rgba(255, 215, 0, 0.9);
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
  background: radial-gradient(circle at top, #1E2C6D, #0F1534);
  border: 2px solid rgba(255, 215, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: inset 0 0 12px rgba(255, 215, 0, 0.3);
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
  box-shadow: inset 0 -2px 0 rgba(0,0,0,0.25);
}

div[data-testid="stSelectbox"] > div, div[data-testid="stMultiSelect"] > div {
  font-size: 1.05rem;
}

div.stButton > button {
  font-size: 1.05rem;
  padding: 0.75rem 1.3rem;
  border-radius: 999px;
  border: 2px solid rgba(255, 215, 0, 0.9);
  background: linear-gradient(180deg, #FFE799, #FFB800);
  color: #2B1A00;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.35), inset 0 -4px 8px rgba(154, 88, 0, 0.45);
  font-weight: 800;
  text-transform: uppercase;
}

div.stButton > button:hover {
  box-shadow: 0 14px 26px rgba(0, 0, 0, 0.45), inset 0 -6px 10px rgba(154, 88, 0, 0.6);
  transform: translateY(-2px);
}

.hero-section {
  position: relative;
  border-radius: 24px;
  padding: 2.2rem 2rem;
  overflow: hidden;
  background: linear-gradient(120deg, var(--hero-glow-1), var(--hero-glow-2), var(--hero-glow-3));
  background-size: 300% 300%;
  border: 2px solid rgba(255, 215, 0, 0.7);
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
  font-size: 2.8rem;
  z-index: 1;
}

.hero-sub {
  position: relative;
  z-index: 1;
  color: #FFF5CC;
  font-weight: 700;
}

.glass-panel {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: 20px;
  padding: 1rem 1.2rem;
  box-shadow: var(--shadow);
}

.pokemon-card,
.poke-card {
  position: relative;
  border-radius: 20px;
  padding: 1rem 1.2rem;
  background: linear-gradient(135deg, rgba(50, 10, 10, 0.92), rgba(12, 8, 30, 0.95));
  border: 2px solid rgba(255, 215, 0, 0.9);
  box-shadow: var(--shadow);
  transform-style: preserve-3d;
  perspective: 900px;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.pokemon-card:hover,
.poke-card:hover {
  transform: translateY(-4px) rotateX(2deg) rotateY(-2deg);
  box-shadow: var(--shadow-hover), 0 18px 38px var(--type-glow, rgba(255, 184, 0, 0.5));
  border-color: var(--type-color, rgba(255, 215, 0, 0.9));
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
  height: 12px;
  border-radius: 999px;
  background: rgba(15, 20, 50, 0.9);
  overflow: hidden;
  border: 1px solid rgba(255, 215, 0, 0.45);
}

.stat-bar-fill {
  height: 100%;
  border-radius: 999px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.45);
}

.stat-bar-fill::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, rgba(255,255,255,0.45), rgba(255,255,255,0.05));
  opacity: 0.6;
  animation: liquidFlow 2.8s linear infinite;
}

.stat-bar-label {
  font-size: 0.78rem;
  color: #FFF5CC;
  margin-bottom: 0.2rem;
}

div[data-testid="stTabs"] button {
  background: rgba(12, 16, 40, 0.9) !important;
  color: #FFF5CC !important;
  border-radius: 999px !important;
  padding: 0.5rem 1.2rem !important;
  border: 1px solid rgba(255, 215, 0, 0.6) !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
  color: #2B1A00 !important;
  border-color: rgba(255, 215, 0, 0.9) !important;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.35);
  background: linear-gradient(180deg, #FFE799, #FFB800) !important;
}

.analysis-panel {
  background: rgba(10, 14, 36, 0.95);
  border: 1px solid rgba(255, 215, 0, 0.6);
  border-radius: 18px;
  padding: 1rem 1.2rem;
  box-shadow: var(--shadow);
}

.deck-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.9rem;
  margin: 0.8rem 0 1.2rem;
}

.deck-slot {
  text-align: center;
}

.deck-frame {
  width: 96px;
  height: 96px;
  margin: 0 auto 0.4rem;
  border-radius: 50%;
  background: radial-gradient(circle at top, #1B2C6D, #0B0F2A);
  border: 3px solid rgba(255, 215, 0, 0.9);
  box-shadow: 0 10px 18px rgba(0, 0, 0, 0.5), inset 0 0 12px rgba(255, 215, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.deck-frame img {
  width: 84px;
  height: 84px;
  object-fit: contain;
}

.deck-name {
  font-weight: 700;
  color: #FFF5CC;
  text-shadow: 0 4px 10px rgba(0,0,0,0.6);
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

.insight-highlight {
  margin-top: 0.8rem;
  padding: 0.9rem 1.1rem;
  border-radius: 16px;
  background: linear-gradient(120deg, rgba(30, 64, 175, 0.12), rgba(15, 23, 42, 0.08));
  border: 1px solid rgba(59, 130, 246, 0.35);
  color: #1E293B;
  font-weight: 700;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
}

.insight-card {
  border-radius: 18px;
  padding: 1rem 1.2rem;
  border: 1px solid var(--panel-border);
  background: #FFFFFF;
  box-shadow: var(--shadow);
  margin-top: 0.6rem;
}

.insight-card.good {
  background: #ECFDF3;
  border-color: #BBF7D0;
  color: #166534;
  font-weight: 600;
}

.insight-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.insight-line {
  color: var(--muted);
  font-size: 0.88rem;
  margin-bottom: 0.35rem;
}

.insight-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 0.6rem;
}

.insight-meter {
  height: 8px;
  background: #E2E8F0;
  border-radius: 999px;
  overflow: hidden;
}

.insight-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #38BDF8, #2563EB);
}

.scenario-card {
  border-radius: 18px;
  padding: 1rem 1.2rem;
  border: 1px solid var(--panel-border);
  background: #F8FAFC;
  box-shadow: var(--shadow);
  margin-top: 0.6rem;
}

.scenario-step {
  margin-bottom: 0.4rem;
  font-weight: 600;
  color: #1E293B;
}

.plan-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.9rem;
  margin-top: 0.6rem;
}

.plan-card {
  border-radius: 18px;
  padding: 1rem 1.1rem;
  background: #FFFFFF;
  border: 1px solid var(--panel-border);
  box-shadow: var(--shadow);
}

.plan-card.highlight {
  border-color: rgba(239, 68, 68, 0.5);
  background: linear-gradient(135deg, rgba(254, 202, 202, 0.4), rgba(219, 234, 254, 0.6));
  box-shadow: 0 16px 32px rgba(239, 68, 68, 0.15);
}

.plan-title {
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.plan-body {
  color: #1E293B;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.plan-meta {
  color: var(--muted);
  font-size: 0.86rem;
  margin-bottom: 0.2rem;
}

.tera-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.8rem;
  margin-top: 0.6rem;
}

.tera-card {
  border-radius: 14px;
  padding: 0.8rem 1rem;
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  font-weight: 600;
  color: #1D4ED8;
}

.survive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.7rem;
  margin-top: 0.6rem;
}

.survive-card {
  border-radius: 14px;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--panel-border);
  background: #FFFFFF;
  font-weight: 600;
}

.survive-card.安定 { border-color: #86EFAC; background: #ECFDF3; color: #166534; }
.survive-card.互角 { border-color: #CBD5E1; background: #F8FAFC; color: #334155; }
.survive-card.要注意 { border-color: #FCD34D; background: #FFFBEB; color: #92400E; }
.survive-card.危険 { border-color: #FCA5A5; background: #FEF2F2; color: #991B1B; }

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

@keyframes liquidFlow {
  0% { transform: translateX(-40%); }
  100% { transform: translateX(40%); }
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
