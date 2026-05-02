import streamlit as st

st.set_page_config(page_title="Welcome to FitSync", page_icon=":sparkles:", layout="wide")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def inject_theme_css(dark):
    if dark:
        bg         = "#0e1117"
        surface    = "#1a1f2e"
        text       = "#fafafa"
        border     = "#2d3748"
        sidebar_bg = "#111827"
        title_color = "#58a6ff"
    else:
        bg         = "#ffffff"
        surface    = "#f0f2f6"
        text       = "#262730"
        border     = "#dde1e9"
        sidebar_bg = "#f0f2f6"
        title_color = "#1f77b4"

    st.markdown(f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg};
        color: {text};
    }}
    [data-testid="stHeader"] {{
        background-color: {bg};
        border-bottom: none;
    }}
    .main .block-container {{
      background-color: {bg};
      border: none;
    }}
    h1 {{
        color: {title_color};
    }}
    p, li, .stMarkdown, .stText {{ color: {text}; }}
    label {{ color: {text} !important; }}
    [data-testid="stToggle"] * {{ color: {text} !important; }}
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border};
    }}
    [data-testid="stSidebar"] * {{ color: {text} !important; }}
    </style>
    """, unsafe_allow_html=True)

inject_theme_css(st.session_state.dark_mode)

title_col, light_col, toggle_col = st.columns([13, 1, 2])
with light_col:
    st.write("🌞 *Light*")
with toggle_col:
    st.toggle("🌙 *Dark*", key="dark_mode")
    inject_theme_css(st.session_state.dark_mode)

st.title("Your Fitness Journey Starts Here! :muscle:")

st.write("Your personal health and fitness companion. Get ready to achieve your goals!")

st.write("FitSync is here to support you every step of the way.")