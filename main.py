import streamlit as st

st.set_page_config(page_title="FitSync | Home", page_icon="💪", layout="wide")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


def inject_theme_css(dark):
    if dark:
        bg         = "#0e1117"
        surface    = "#1a1f2e"
        text       = "#fafafa"
        subtext    = "#9ea3b0"
        border     = "#2d3748"
        sidebar_bg = "#111827"
        nav_active = "#2d3748"
        nav_text   = "#ffffff"
        nav_hover  = "rgba(255,255,255,0.08)"
        accent     = "#58a6ff"
        hero_grad  = "linear-gradient(135deg, #0d1b2a 0%, #1a1f2e 50%, #0e1117 100%)"
        card_bg    = "#1a1f2e"
        muted      = "rgba(255,255,255,0.6)"
    else:
        bg         = "#ffffff"
        surface    = "#f0f2f6"
        text       = "#262730"
        subtext    = "#6b6f7a"
        border     = "#dde1e9"
        sidebar_bg = "#f0f2f6"
        nav_active = "#e2e8f0"
        nav_text   = "#1a202c"
        nav_hover  = "rgba(0,0,0,0.06)"
        accent     = "#1f77b4"
        hero_grad  = "linear-gradient(135deg, #e8f0fe 0%, #dce8ff 50%, #f0f4ff 100%)"
        card_bg    = "#ffffff"
        muted      = "rgba(0,0,0,0.55)"

    st.markdown(f"""
    <style>
    :root {{
        --background-color: {bg} !important;
        --secondary-background-color: {surface} !important;
        --text-color: {text} !important;
    }}
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg} !important;
        color: {text};
    }}
    [data-testid="stHeader"] {{ display: none; }}
    .main .block-container {{ background-color: {bg}; border: none; padding-top: 1rem; }}
    p, li, .stMarkdown, .stText {{ color: {text}; }}
    label {{ color: {text} !important; }}
    [data-testid="stToggle"] * {{ color: {text} !important; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border};
    }}
    [data-testid="stSidebar"] * {{ color: {text} !important; }}
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background-color: {surface};
        border-color: {border};
    }}

    /* Sidebar nav links */
    [data-testid="stSidebarNav"] a {{
        color: {text} !important;
        background-color: transparent !important;
    }}
    [data-testid="stSidebarNav"] a span {{ color: {text} !important; }}
    [data-testid="stSidebarNav"] a:hover {{
        background-color: {nav_hover} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"],
    [data-testid="stSidebarNav"] li[aria-selected="true"] > a {{
        background-color: {nav_active} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] span,
    [data-testid="stSidebarNav"] li[aria-selected="true"] > a span {{
        color: {nav_text} !important;
        font-weight: 600;
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {{ color: {text} !important; }}

    /* Metric cards */
    [data-testid="metric-container"] {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 18px 22px;
    }}
    [data-testid="stMetricValue"] {{ color: {text} !important; }}
    [data-testid="stMetricLabel"] {{ color: {subtext} !important; }}

    /* Divider & selectbox */
    hr {{ border-color: {border}; }}
    div[data-baseweb="select"] > div {{
        background-color: {surface};
        border-color: {border};
        color: {text};
    }}
    div[data-baseweb="select"] svg {{ fill: {subtext}; }}

    /* Hero */

    .hero-section {{
        background: {hero_grad};
        border-radius: 20px;
        padding: 60px 42px;
        margin-bottom: 30px;
        border: 1px solid {border};
        text-align: center;
    }}
    .hero-title {{
        font-size: 3.52rem;
        font-weight: 800;
        color: {accent};
        margin: 0 0 12px 0;
    }}
    .hero-subtitle {{
        font-size: 1.25rem;
        color: {text};
        margin: 0 0 8px 0;
    }}
    .hero-tagline {{
        font-size: 0.95rem;
        color: {muted};
        margin: 0;
    }}
    .nav-card {{
        background: {card_bg};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 36px 28px;
        text-align: center;
        height: 100%;
    }}
    .nav-card-icon  {{ font-size: 2.8rem; margin-bottom: 12px; }}
    .nav-card-title {{ font-size: 1.25rem; font-weight: 700; color: {accent}; margin-bottom: 8px; }}
    .nav-card-desc  {{ font-size: 0.95rem; color: {muted}; }}
    .footer-hint    {{ text-align: center; color: {muted}; font-size: 0.85rem; margin-top: 18px; }}
    </style>
    """, unsafe_allow_html=True)


inject_theme_css(st.session_state.dark_mode)

# ── Sidebar: theme toggle ─────────────────────────────────────────────────────
with st.sidebar:
    lc, rc = st.columns([1, 1.5], vertical_alignment="center")
    with lc:
        st.write("🌞 Light")
    with rc:
        _toggled = st.toggle("🌙 Dark", value=st.session_state.dark_mode)
if _toggled != st.session_state.dark_mode:
    st.session_state.dark_mode = _toggled
    st.rerun()
inject_theme_css(st.session_state.dark_mode)
st.sidebar.divider()

# ── Resolve theme ─────────────────────────────────────────────────────────────
dark_mode = st.session_state.dark_mode
accent    = "#58a6ff" if dark_mode else "#1f77b4"
muted     = "rgba(255,255,255,0.6)" if dark_mode else "rgba(0,0,0,0.55)"
text      = "#fafafa" if dark_mode else "#262730"

# ── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">💪 FitSync</div>
    <div class="hero-subtitle">Your Personal Health &amp; Fitness Analytics Platform</div>
    <div class="hero-tagline">Track your steps · sleep · heart rate · recovery — all in one place</div>
</div>
""", unsafe_allow_html=True)

# ── About FitSync ─────────────────────────────────────────────────────────────
st.markdown(f'<h2 style="color:{accent}; margin-bottom:10px;">About FitSync</h2>',
            unsafe_allow_html=True)
st.markdown(f"""
<p style="color:{text}; font-size:1.05rem; line-height:1.7;">
FitSync is a personal health analytics dashboard designed to turn your daily fitness data into
clear, actionable insights. By tracking key metrics — steps, sleep, heart rate, and calories —
FitSync calculates a personalised <strong>Recovery Score</strong> that reflects how well your
body is responding to activity and rest each day. Whether you're optimising athletic performance
or simply building healthier habits, FitSync gives you the visibility to make informed decisions
about your health.
</p>
""", unsafe_allow_html=True)

st.divider()

# ── How to Use ────────────────────────────────────────────────────────────────
st.markdown(f'<h2 style="color:{accent}; margin-bottom:10px;">How to Use</h2>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="nav-card">
        <div class="nav-card-icon">📊</div>
        <div class="nav-card-title">Dashboard</div>
        <div class="nav-card-desc" style="text-align:left;">
            Use the <strong>Dashboard</strong> page for a daily overview. View your key metrics
            at a glance, explore how recovery relates to sleep and steps, and monitor heart rate
            and calorie trends. Use the sidebar filter to focus on the last 7 days, 30 days,
            or your full history.
        </div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="nav-card">
        <div class="nav-card-icon">📈</div>
        <div class="nav-card-title">Trends &amp; Insights</div>
        <div class="nav-card-desc" style="text-align:left;">
            Use the <strong>Trends &amp; Insights</strong> page to go deeper. Review statistical
            summaries including mean, min, max, and standard deviation. Track monthly recovery
            patterns and explore how your metrics are distributed over time.
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown(f'<div class="footer-hint">👈 Use the sidebar to navigate between pages</div>',
            unsafe_allow_html=True)
