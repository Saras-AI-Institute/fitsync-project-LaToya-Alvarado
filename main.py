import streamlit as st

st.set_page_config(page_title="Welcome to FitSync", page_icon=":sparkles:", layout="wide")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def inject_theme_css(dark):
    if dark:
        bg         = "#0e1117"
        surface    = "#1a1f2e"
        text       = "#fafafa"
        subtext    = "#9ea3b0"
        border     = "#2d3748"
        sidebar_bg = "#111827"
        title_color = "#58a6ff"
    else:
        bg         = "#ffffff"
        surface    = "#f0f2f6"
        text       = "#262730"
        subtext    = "#6b6f7a"
        border     = "#dde1e9"
        sidebar_bg = "#f0f2f6"
        title_color = "#1f77b4"

    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg};
        color: {text};
    }}
    .main .block-container {{ 
      background-color: {bg};
      border: 1px solid {border};
    }}
    h1 {{
        color: {title_color};
    }}
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border};
    }}
    [data-testid="stSidebar"] * {{ color: {text} !important; }}
    </style>
    """, unsafe_allow_html=True)

inject_theme_css(st.session_state.dark_mode)

col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.experimental_rerun()

st.title("Your Fitness Journey Starts Here! :muscle:")

st.write("Your personal health and fitness companion. Get ready to achieve your goals!")

st.write("FitSync is here to support you every step of the way.")