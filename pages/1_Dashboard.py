import sys
sys.path.append('/workspaces/fitsync-project-LaToya-Alvarado')

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from modules.processor import process_data

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="FitSync Dashboard", layout="wide")

# ── Theme state ───────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def inject_theme_css(dark):
    """Inject CSS that recolors every Streamlit surface for the chosen mode."""
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
    }}
    [data-testid="stHeader"] {{
        background-color: {header_bg};
        border-bottom: 1px solid {border};
    }}
    .main .block-container {{ background-color: {bg}; }}

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


# ── Apply theme before any widget renders ────────────────────────────────────
inject_theme_css(st.session_state.dark_mode)

# ── Header row: title left, dark-mode toggle right ───────────────────────────
title_col, _, toggle_col = st.columns([7, 1, 1])
with title_col:
    st.title("FitSync Health Dashboard")
with toggle_col:
    st.write("")
    st.toggle("🌙 Dark mode", key="dark_mode")
    inject_theme_css(st.session_state.dark_mode)   # re-apply after toggle

# ── Resolve theme variables (must come after toggle) ─────────────────────────
dark_mode          = st.session_state.dark_mode
plotly_tpl         = "plotly_dark"  if dark_mode else "plotly_white"
paper_bg           = "#1a1f2e"      if dark_mode else "#f0f2f6"
plot_bg            = "#1a1f2e"      if dark_mode else "#f8f9fa"
font_col           = "#fafafa"      if dark_mode else "#262730"
grid_col           = "#2d3748"      if dark_mode else "#e5e7eb"
section_header_col = "#58a6ff"      if dark_mode else "#1f77b4"


def chart_layout(title, extra=None):
    """Return a Plotly layout dict with the active theme applied.
    Title color is set explicitly so it stays readable in both modes."""
    layout = dict(
        title=dict(text=title, font=dict(size=15, color=font_col)),
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_col, size=13),
        margin=dict(t=60, b=50, l=60, r=40),
    )
    if extra:
        layout.update(extra)
    return layout


# ── Load & cache data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return process_data()

df = load_data()

# ── Sidebar: time-range filter ────────────────────────────────────────────────
st.sidebar.header("📊 Filters")
time_filter = st.sidebar.selectbox(
    "Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"],
)

max_date = df["Date"].max()
if time_filter == "Last 7 Days":
    filtered_df = df[df["Date"] >= max_date - timedelta(days=6)]
elif time_filter == "Last 30 Days":
    filtered_df = df[df["Date"] >= max_date - timedelta(days=29)]
else:
    filtered_df = df.copy()

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — 📈 KEY METRICS
# 4 cards: Avg Steps, Sleep, Heart Rate, Recovery Score — each with a delta
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f'<h2 style="color: {section_header_col};">📈 Key Metrics</h2>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)

avg_steps      = filtered_df["Steps"].mean()
avg_sleep      = filtered_df["Sleep_Hours"].mean()
avg_heart_rate = filtered_df["Heart_Rate_bpm"].mean()
avg_recovery   = filtered_df["Recovery_score"].mean()

m1.metric("Average Daily Steps",    f"{avg_steps:,.0f}",      f"{avg_steps - 7500:.0f} from goal")
m2.metric("Average Sleep (hours)",  f"{avg_sleep:.1f}",       f"{avg_sleep - 7:.1f} from recommended")
m3.metric("Average Heart Rate (bpm)", f"{avg_heart_rate:.0f}", f"{68 - avg_heart_rate:.0f} from baseline")
m4.metric("Average Recovery Score", f"{avg_recovery:.1f}",    f"{avg_recovery - 50:.1f} from baseline")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — 📉 RECOVERY SCORE & SLEEP TRENDS
# Left : Dual-axis line — Recovery Score & Sleep Hours over time
# Right: Scatter        — Recovery Score vs Steps, coloured by Sleep Hours
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f'<h2 style="color: {section_header_col};">📉 Recovery Score & Sleep Trends</h2>', unsafe_allow_html=True)
col_left, col_right = st.columns(2)

# Left — dual-axis line chart
with col_left:
    fig_trend = go.Figure()

    # Primary Y-axis: Recovery Score
    fig_trend.add_trace(go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Recovery_score"],
        name="Recovery Score",
        mode="lines",
        line=dict(color="#636EFA", width=2),
    ))

    # Secondary Y-axis: Sleep Hours
    fig_trend.add_trace(go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Sleep_Hours"],
        name="Sleep Hours",
        mode="lines",
        line=dict(color="#EF553B", width=2),
        yaxis="y2",
    ))

    fig_trend.update_layout(**chart_layout(
        "Recovery Score & Sleep Trend",
        extra=dict(
            xaxis=dict(title="Date", gridcolor=grid_col),
            yaxis=dict(title="Recovery Score", gridcolor=grid_col),
            yaxis2=dict(
                title="Sleep Hours",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom", y=1.02,
                xanchor="right",  x=1,
            ),
        ),
    ))
    st.plotly_chart(fig_trend, use_container_width=True)

# Right — scatter: Recovery Score vs Steps, colour = Sleep Hours
with col_right:
    fig_steps_scatter = px.scatter(
        filtered_df,
        x="Steps",
        y="Recovery_score",
        color="Sleep_Hours",
        color_continuous_scale="Viridis",
        labels={
            "Steps":          "Daily Steps",
            "Recovery_score": "Recovery Score",
            "Sleep_Hours":    "Sleep Hrs",
        },
        template=plotly_tpl,
    )
    fig_steps_scatter.update_layout(**chart_layout(
        "Recovery Score vs Daily Steps",
        extra=dict(
            xaxis=dict(gridcolor=grid_col),
            yaxis=dict(gridcolor=grid_col),
        ),
    ))
    st.plotly_chart(fig_steps_scatter, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — ❤️ HEART RATE & CALORIES
# Left : Scatter — Recovery Score vs Resting Heart Rate
# Right: Line    — Calories Burned over time
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f'<h2 style="color: {section_header_col};">❤️ Heart Rate & Calories</h2>', unsafe_allow_html=True)
col_left2, col_right2 = st.columns(2)

# Left — scatter: Recovery Score vs Resting Heart Rate
with col_left2:
    fig_hr_scatter = px.scatter(
        filtered_df,
        x="Heart_Rate_bpm",
        y="Recovery_score",
        color="Recovery_score",
        color_continuous_scale="RdYlGn",
        labels={
            "Heart_Rate_bpm": "Resting Heart Rate (bpm)",
            "Recovery_score": "Recovery Score",
        },
        template=plotly_tpl,
    )
    fig_hr_scatter.update_layout(**chart_layout(
        "Recovery Score vs Resting Heart Rate",
        extra=dict(
            xaxis=dict(gridcolor=grid_col),
            yaxis=dict(gridcolor=grid_col),
        ),
    ))
    st.plotly_chart(fig_hr_scatter, use_container_width=True)

# Right — line chart: Calories Burned over time
with col_right2:
    fig_cal = px.line(
        filtered_df,
        x="Date",
        y="Calories_Burned",
        labels={"Date": "Date", "Calories_Burned": "Calories Burned"},
        template=plotly_tpl,
    )
    fig_cal.update_traces(line=dict(color="#00CC96", width=2))
    fig_cal.update_layout(**chart_layout(
        "Daily Calories Burned Trend",
        extra=dict(
            xaxis=dict(gridcolor=grid_col),
            yaxis=dict(gridcolor=grid_col),
        ),
    ))
    st.plotly_chart(fig_cal, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — 📊 HEALTH TRENDS
# Row 1: Daily Steps line | Sleep Hours line
# Row 2: Heart Rate line  | Recovery Score line
# Each chart has a reference baseline/goal line
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f'<h2 style="color: {section_header_col};">📊 Health Trends</h2>', unsafe_allow_html=True)

# Row 1: Steps and Sleep
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<h3 style="color: {font_col};">👣 Daily Steps</h3>', unsafe_allow_html=True)
    fig_steps = px.line(
        filtered_df,
        x="Date",
        y="Steps",
        labels={"Steps": "Steps", "Date": "Date"},
        template=plotly_tpl,
    )
    fig_steps.add_hline(y=7500, line_dash="dash", line_color="green",
                        annotation_text="Recommended (7,500)")
    fig_steps.update_traces(line_color="#1f77b4", line_width=2)
    fig_steps.update_layout(
        height=350,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_col),
    )
    st.plotly_chart(fig_steps, use_container_width=True)

with col2:
    st.markdown(f'<h3 style="color: {font_col};">😴 Sleep Hours</h3>', unsafe_allow_html=True)
    fig_sleep = px.line(
        filtered_df,
        x="Date",
        y="Sleep_Hours",
        labels={"Sleep_Hours": "Sleep (hours)", "Date": "Date"},
        template=plotly_tpl,
    )
    fig_sleep.add_hline(y=7, line_dash="dash", line_color="green",
                        annotation_text="Recommended (7 hrs)")
    fig_sleep.update_traces(line_color="#ff7f0e", line_width=2)
    fig_sleep.update_layout(
        height=350,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_col),
    )
    st.plotly_chart(fig_sleep, use_container_width=True)

# Row 2: Heart Rate and Recovery Score
col3, col4 = st.columns(2)

with col3:
    st.markdown(f'<h3 style="color: {font_col};">❤️ Heart Rate</h3>', unsafe_allow_html=True)
    fig_hr_line = px.line(
        filtered_df,
        x="Date",
        y="Heart_Rate_bpm",
        labels={"Heart_Rate_bpm": "Heart Rate (bpm)", "Date": "Date"},
        template=plotly_tpl,
    )
    fig_hr_line.add_hline(y=68, line_dash="dash", line_color="green",
                          annotation_text="Baseline (68 bpm)")
    fig_hr_line.update_traces(line_color="#d62728", line_width=2)
    fig_hr_line.update_layout(
        height=350,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_col),
    )
    st.plotly_chart(fig_hr_line, use_container_width=True)

with col4:
    st.markdown(f'<h3 style="color: {font_col};">🔄 Recovery Score</h3>', unsafe_allow_html=True)
    fig_recovery = px.line(
        filtered_df,
        x="Date",
        y="Recovery_score",
        labels={"Recovery_score": "Recovery Score", "Date": "Date"},
        template=plotly_tpl,
    )
    fig_recovery.add_hline(y=50, line_dash="dash", line_color="gray",
                           annotation_text="Baseline (50)")
    fig_recovery.update_traces(line_color="#2ca02c", line_width=2)
    fig_recovery.update_layout(
        height=350,
        yaxis_range=[0, 100],
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_col),
    )
    st.plotly_chart(fig_recovery, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — 🔍 COMBINED ANALYSIS
# Left (2/3 width) : Correlation heatmap of key metrics
# Right (1/3 width): Recovery Score distribution histogram
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f'<h2 style="color: {section_header_col};">🔍 Combined Analysis</h2>', unsafe_allow_html=True)
col_wide, col_narrow = st.columns([2, 1])

# Left — correlation matrix heatmap
with col_wide:
    st.markdown(f'<h3 style="color: {font_col};">Correlation Matrix</h3>', unsafe_allow_html=True)
    corr_columns = ["Steps", "Sleep_Hours", "Heart_Rate_bpm", "Recovery_score"]
    correlation_matrix = filtered_df[corr_columns].corr()

    fig_corr = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        labels=dict(color="Correlation"),
        template=plotly_tpl,
    )
    fig_corr.update_layout(
        height=400,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_col),
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# Right — Recovery Score distribution
with col_narrow:
    st.markdown(f'<h3 style="color: {font_col};">Recovery Score Distribution</h3>', unsafe_allow_html=True)
    fig_dist = px.histogram(
        filtered_df,
        x="Recovery_score",
        nbins=20,
        labels={"Recovery_score": "Recovery Score", "count": "Frequency"},
        template=plotly_tpl,
    )
    fig_dist.update_traces(marker_color="#2ca02c")
    fig_dist.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_col),
    )
    st.plotly_chart(fig_dist, use_container_width=True)
