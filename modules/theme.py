import streamlit as st


def inject_theme_css(dark):
    if dark:
        bg         = "#0e1117"
        surface    = "#1a1f2e"
        text       = "#fafafa"
        subtext    = "#9ea3b0"
        border     = "#2d3748"
        sidebar_bg = "#111827"
        header_bg  = "#0e1117"
        nav_active = "#2d3748"
        nav_text   = "#ffffff"
        nav_hover  = "rgba(255,255,255,0.08)"
    else:
        bg         = "#ffffff"
        surface    = "#f0f2f6"
        text       = "#262730"
        subtext    = "#6b6f7a"
        border     = "#dde1e9"
        sidebar_bg = "#f0f2f6"
        header_bg  = "#ffffff"
        nav_active = "#e2e8f0"
        nav_text   = "#1a202c"
        nav_hover  = "rgba(0,0,0,0.06)"

    st.markdown(f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg};
        color: {text};
    }}
    [data-testid="stHeader"] {{
        background-color: {header_bg};
        border-bottom: none;
        display: block;
    }}
    .main .block-container {{
        background-color: {bg};
        border: none;
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
    [data-testid="stToggle"] * {{ color: {text} !important; }}

    /* Metric cards */
    [data-testid="metric-container"] {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 18px 22px;
    }}
    [data-testid="stMetricValue"] {{ color: {text} !important; }}
    [data-testid="stMetricLabel"] {{ color: {subtext} !important; }}
    [data-testid="stMetricDelta"] {{ color: {subtext} !important; }}

    /* Divider & selectbox */
    hr {{ border-color: {border}; }}
    div[data-baseweb="select"] > div {{
        background-color: {surface};
        border-color: {border};
        color: {text};
    }}
    div[data-baseweb="select"] svg {{ fill: {subtext}; }}
    </style>
    """, unsafe_allow_html=True)
