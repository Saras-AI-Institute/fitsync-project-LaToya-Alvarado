import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from modules.processor import process_data

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="FitSync – Trends & Insights", layout="wide")

# ── Theme state ───────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


def inject_theme_css(dark):
    """Inject CSS for the chosen light/dark mode."""
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
    :root {{
        --background-color: {bg} !important;
        --secondary-background-color: {surface} !important;
        --text-color: {text} !important;
    }}
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg} !important;
    }}
    [data-testid="stHeader"] {{
        background-color: {header_bg} !important;
        border-bottom: 1px solid {border};
    }}
    .main .block-container {{ background-color: {bg} !important; }}

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


# ── Apply theme immediately ───────────────────────────────────────────────────
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

# ── Page title ────────────────────────────────────────────────────────────────
st.title("Trends & Insights")

# ── Resolve theme variables for Plotly charts ─────────────────────────────────
dark_mode  = st.session_state.dark_mode
plotly_tpl = "plotly_dark"  if dark_mode else "plotly_white"
paper_bg   = "#1a1f2e"      if dark_mode else "#f0f2f6"
plot_bg    = "#1a1f2e"      if dark_mode else "#f8f9fa"
font_col   = "#fafafa"      if dark_mode else "#262730"
grid_col   = "#2d3748"      if dark_mode else "#e5e7eb"


def chart_layout(title, extra=None):
    """Return a Plotly layout dict with the active theme applied."""
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
st.sidebar.markdown("**Filters**")
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
# SECTION 1 — SUMMARY STATISTICS
# Shows mean / min / max for the four key health metrics
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Summary Statistics")

METRICS = {
    "Recovery Score":  ("Recovery_score",  ".1f"),
    "Sleep Hours":     ("Sleep_Hours",     ".1f"),
    "Steps":           ("Steps",           ",.0f"),
    "Calories Burned": ("Calories_Burned", ".1f"),
}

# Metric cards row
stat_cols = st.columns(len(METRICS))
for col, (label, (field, fmt)) in zip(stat_cols, METRICS.items()):
    mean_val = filtered_df[field].mean()
    min_val  = filtered_df[field].min()
    max_val  = filtered_df[field].max()
    col.metric(
        label=label,
        value=f"{mean_val:{fmt}}",
        help=f"Min: {min_val:{fmt}}  |  Max: {max_val:{fmt}}",
    )

# Detailed stats table (mean / min / max / std) — custom HTML for dark mode support
surface = "#1a1f2e" if dark_mode else "#f0f2f6"
border  = "#2d3748" if dark_mode else "#dde1e9"
subtext = "#9ea3b0" if dark_mode else "#6b6f7a"

cols  = ["Recovery_score", "Sleep_Hours", "Steps", "Calories_Burned"]
stats = filtered_df[cols].agg(["mean", "min", "max", "std"]).round(2)

col_labels = ["", "Recovery Score", "Sleep Hours", "Steps", "Calories Burned"]
header_cells = "".join(
    f'<th style="padding:10px 16px; text-align:right; color:{subtext}; '
    f'border-bottom:2px solid {border};">{h}</th>' for h in col_labels
)

rows_html = ""
for stat in ["mean", "min", "max", "std"]:
    row_vals = stats.loc[stat]
    cells = f'<td style="padding:10px 16px; color:{subtext}; border-bottom:1px solid {border};">{stat}</td>'
    for val in row_vals:
        cells += (f'<td style="padding:10px 16px; text-align:right; color:{font_col}; '
                  f'border-bottom:1px solid {border};">{val:,.2f}</td>')
    rows_html += f"<tr>{cells}</tr>"

st.markdown(f"""
<table style="width:100%; border-collapse:collapse; background:{surface};
              border-radius:10px; overflow:hidden; border:1px solid {border};">
  <thead><tr>{header_cells}</tr></thead>
  <tbody>{rows_html}</tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1b — KEY INSIGHTS
# Auto-generated plain-English sentences driven by the filtered data values.
# Each metric has three tiers (good / moderate / poor) so the language changes
# depending on the selected time range.
# ─────────────────────────────────────────────────────────────────────────────
accent = "#58a6ff" if dark_mode else "#1f77b4"

avg_recovery = filtered_df["Recovery_score"].mean()
avg_sleep    = filtered_df["Sleep_Hours"].mean()
avg_steps    = filtered_df["Steps"].mean()
avg_hr       = filtered_df["Heart_Rate_bpm"].mean()

if avg_recovery >= 70:
    recovery_insight = (
        f"✅ **Recovery Score {avg_recovery:.1f}** — above the strong threshold. "
        "Your body is responding well to your current activity and rest balance."
    )
elif avg_recovery >= 50:
    recovery_insight = (
        f"🟡 **Recovery Score {avg_recovery:.1f}** — moderate, above baseline. "
        "There is room to improve through more consistent sleep or reduced overtraining."
    )
else:
    recovery_insight = (
        f"🔴 **Recovery Score {avg_recovery:.1f}** — below the 50-point baseline. "
        "Prioritise sleep quality and consider reducing high-intensity days."
    )

if avg_sleep >= 7:
    sleep_insight = (
        f"✅ **Sleep {avg_sleep:.1f} hrs/night** — meeting the recommended minimum. "
        "Consistent sleep is the strongest single driver of your recovery score."
    )
elif avg_sleep >= 6:
    sleep_insight = (
        f"🟡 **Sleep {avg_sleep:.1f} hrs/night** — slightly below the 7-hour recommendation. "
        "Even 30 extra minutes per night can measurably lift your recovery score."
    )
else:
    sleep_insight = (
        f"🔴 **Sleep {avg_sleep:.1f} hrs/night** — well below recommended levels. "
        "Poor sleep is the single biggest drag on recovery — this is the first thing to address."
    )

if avg_steps >= 7500:
    steps_insight = (
        f"✅ **{avg_steps:,.0f} steps/day** — above the 7,500-step goal. "
        "You are consistently hitting an active lifestyle threshold."
    )
elif avg_steps >= 5000:
    steps_insight = (
        f"🟡 **{avg_steps:,.0f} steps/day** — approaching the 7,500 goal. "
        "Small, consistent increases each day will close this gap."
    )
else:
    steps_insight = (
        f"🔴 **{avg_steps:,.0f} steps/day** — below the active threshold. "
        "Sustained low activity can reduce recovery scores over time."
    )

if avg_hr <= 65:
    hr_insight = (
        f"✅ **Resting HR {avg_hr:.0f} bpm** — excellent. "
        "A resting heart rate this low is a strong indicator of cardiovascular fitness."
    )
elif avg_hr <= 75:
    hr_insight = (
        f"🟡 **Resting HR {avg_hr:.0f} bpm** — within the healthy range. "
        "Sustained aerobic activity over weeks will gradually lower this further."
    )
else:
    hr_insight = (
        f"🔴 **Resting HR {avg_hr:.0f} bpm** — elevated above the 68 bpm baseline. "
        "This can reflect accumulated stress or insufficient recovery time."
    )

st.markdown(
    f'<h2 style="color:{accent}; margin-bottom:4px;">💡 Key Insights</h2>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<p style="color:{subtext}; font-size:0.9rem; margin-bottom:16px;">'
    f'Generated from your {time_filter.lower()} data</p>',
    unsafe_allow_html=True,
)

for insight in [recovery_insight, sleep_insight, steps_insight, hr_insight]:
    st.markdown(insight)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — TREND CHARTS (2 columns)
# Left : Dual line — Recovery Score & Sleep Hours over time
# Right: Scatter   — Recovery Score vs Steps, coloured by Sleep Hours
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Recovery Score & Sleep Trends")
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
# SECTION 3 — HEART RATE & CALORIES CHARTS (2 columns)
# Left : Scatter — Recovery Score vs Resting Heart Rate
# Right: Line    — Calories Burned over time
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Heart Rate & Calories")
col_left2, col_right2 = st.columns(2)

# Left — scatter: Recovery Score vs Resting Heart Rate
with col_left2:
    fig_hr = px.scatter(
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
    fig_hr.update_layout(**chart_layout(
        "Recovery Score vs Resting Heart Rate",
        extra=dict(
            xaxis=dict(gridcolor=grid_col),
            yaxis=dict(gridcolor=grid_col),
        ),
    ))
    st.plotly_chart(fig_hr, use_container_width=True)

# Right — line chart: Calories Burned over time
with col_right2:
    fig_cal = px.line(
        filtered_df,
        x="Date",
        y="Calories_Burned",
        labels={
            "Date":            "Date",
            "Calories_Burned": "Calories Burned",
        },
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
# SECTION 4 — MONTHLY AVERAGE RECOVERY SCORE
# Line chart grouped by month
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Monthly Average Recovery Score")

monthly = (
    filtered_df.copy()
    .assign(Month=lambda d: d["Date"].dt.to_period("M").dt.to_timestamp())
    .groupby("Month", as_index=False)["Recovery_score"]
    .mean()
)

fig_monthly = px.line(
    monthly,
    x="Month",
    y="Recovery_score",
    markers=True,
    labels={"Month": "Month", "Recovery_score": "Avg Recovery Score"},
    template=plotly_tpl,
)
fig_monthly.update_traces(
    line=dict(color="#636EFA", width=2.5),
    marker=dict(size=7, color="#636EFA"),
)
fig_monthly.update_layout(**chart_layout(
    "Average Recovery Score by Month",
    extra=dict(
        xaxis=dict(title="Month", gridcolor=grid_col),
        yaxis=dict(title="Avg Recovery Score", gridcolor=grid_col),
    ),
))
st.plotly_chart(fig_monthly, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — DISTRIBUTIONS (2 × 2 histogram grid)
# Steps, Calories Burned, Recovery Score, Sleep Hours
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Distributions")

HIST_CONFIGS = [
    ("Steps",           "Daily Steps",     "#636EFA"),
    ("Calories_Burned", "Calories Burned", "#EF553B"),
    ("Recovery_score",  "Recovery Score",  "#00CC96"),
    ("Sleep_Hours",     "Sleep Hours",     "#AB63FA"),
]

row1_l, row1_r = st.columns(2)
row2_l, row2_r = st.columns(2)
hist_cols = [row1_l, row1_r, row2_l, row2_r]

for col, (field, x_label, color) in zip(hist_cols, HIST_CONFIGS):
    with col:
        fig_hist = px.histogram(
            filtered_df,
            x=field,
            nbins=25,
            labels={field: x_label},
            template=plotly_tpl,
            color_discrete_sequence=[color],
        )
        fig_hist.update_layout(**chart_layout(
            f"Distribution of {x_label}",
            extra=dict(
                xaxis=dict(title=x_label, gridcolor=grid_col),
                yaxis=dict(title="Count",  gridcolor=grid_col),
                bargap=0.05,
            ),
        ))
        st.plotly_chart(fig_hist, use_container_width=True)
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df)
