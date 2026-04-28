import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="FitSync")

# ── Theme state ───────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def inject_theme_css(dark):
    """Inject CSS that recolors every Streamlit surface for the chosen mode."""
    if dark:
        bg             = "#0e1117"
        surface        = "#1a1f2e"
        text           = "#fafafa"
        subtext        = "#9ea3b0"
        border         = "#2d3748"
        sidebar_bg     = "#111827"
        header_bg      = "#0e1117"
        nav_active     = "#2d3748"
        nav_text       = "#ffffff"
        nav_hover      = "rgba(255,255,255,0.08)"
        header_color   = "#58a6ff"
        subheader_color= "#8b949e"
    else:
        bg             = "#ffffff"
        surface        = "#f0f2f6"
        text           = "#262730"
        subtext        = "#6b6f7a"
        border         = "#dde1e9"
        sidebar_bg     = "#f0f2f6"
        header_bg      = "#ffffff"
        nav_active     = "#e2e8f0"
        nav_text       = "#1a202c"
        nav_hover      = "rgba(0,0,0,0.06)"
        header_color   = "#1f77b4"
        subheader_color= "#666666"

    st.markdown(f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg};
    }}
    [data-testid="stHeader"] {{
        background-color: {header_bg};
        border-bottom: 1px solid {border};
    }}
    .main .block-container {{ background-color: {bg}; }}

    /* Centered hero title and subtitle */
    .main-header {{
        font-size: 3rem;
        font-weight: bold;
        color: {header_color};
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    .sub-header {{
        font-size: 1.2rem;
        color: {subheader_color};
        text-align: center;
        margin-bottom: 2rem;
    }}

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
    p, li, .stMarkdown, .stText {{ color: {text}; }}
    label {{ color: {subtext} !important; }}

    /* Toggle label text alignment */
    .toggle-label {{
        color: {text};
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 10px;
        display: block;
    }}
    </style>
    """, unsafe_allow_html=True)


# ── Apply theme before any widget renders ────────────────────────────────────
inject_theme_css(st.session_state.dark_mode)

# ── Resolve theme variables ───────────────────────────────────────────────────
dark_mode = st.session_state.dark_mode
font_col  = "#fafafa" if dark_mode else "#262730"

# ── Top bar: "☀️ Light mode" — toggle — "🌙 Dark mode" in top right ──────────
_, light_lbl, tog_col, dark_lbl = st.columns([6, 0.9, 0.5, 0.9])

with light_lbl:
    st.write("")
    st.markdown(
        f'<span class="toggle-label" style="text-align:right; display:block;">☀️ Light mode</span>',
        unsafe_allow_html=True,
    )
with tog_col:
    st.write("")
    st.toggle("", key="dark_mode", label_visibility="collapsed")
with dark_lbl:
    st.write("")
    st.markdown(
        f'<span class="toggle-label">🌙 Dark mode</span>',
        unsafe_allow_html=True,
    )

# Re-apply CSS immediately after the toggle fires
inject_theme_css(st.session_state.dark_mode)

# ── Hero: title and subtitle ──────────────────────────────────────────────────
st.markdown('<p class="main-header">FitSync - Personal Health Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Track your health metrics and optimize your recovery</p>', unsafe_allow_html=True)
