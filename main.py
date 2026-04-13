import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.processor import process_data

# Page configuration
st.set_page_config(layout="wide", page_title="FitSync")

# Initialize session state for theme
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Theme toggle in top right corner
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Dynamic CSS based on theme
if st.session_state.dark_mode:
    # Dark mode
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #58a6ff;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #8b949e;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #fafafa !important;
        }
        .stMarkdown {
            color: #fafafa;
        }
        /* Metric labels styling */
        [data-testid="stMetricLabel"] {
            color: #fafafa !important;
        }
        [data-testid="stMetricValue"] {
            color: #fafafa !important;
        }
        [data-testid="stMetricDelta"] {
            color: #8b949e !important;
        }
        /* Data table styling */
        [data-testid="stDataFrame"] {
            background-color: #1e2130 !important;
        }
        [data-testid="stDataFrame"] table {
            background-color: #1e2130 !important;
        }
        [data-testid="stDataFrame"] th {
            background-color: #262c3e !important;
            color: #fafafa !important;
        }
        [data-testid="stDataFrame"] td {
            background-color: #1e2130 !important;
            color: #fafafa !important;
        }
        [data-testid="stDataFrame"] * {
            color: #fafafa !important;
        }
        div[data-testid="stHorizontalBlock"] {
            background-color: #0e1117;
        }
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1e2130 !important;
        }
        [data-testid="stSidebar"] * {
            color: #fafafa !important;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #58a6ff !important;
        }
        /* Sidebar selectbox styling */
        [data-testid="stSidebar"] [data-testid="stSelectbox"] {
            background-color: #262c3e !important;
        }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] * {
            color: #fafafa !important;
        }
        </style>
        """, unsafe_allow_html=True)
    plotly_template = 'plotly_dark'
    bg_color = '#0e1117'
    plot_bg_color = '#0e1117'
    font_color = '#fafafa'
    section_header_color = '#58a6ff'
else:
    # Light mode
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #0e1117;
        }
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #0e1117 !important;
        }
        .stMarkdown {
            color: #0e1117;
        }
        /* Metric labels styling */
        [data-testid="stMetricLabel"] {
            color: #0e1117 !important;
        }
        [data-testid="stMetricValue"] {
            color: #0e1117 !important;
        }
        [data-testid="stMetricDelta"] {
            color: #666 !important;
        }
        /* Data table styling */
        [data-testid="stDataFrame"] {
            background-color: #f8f9fa !important;
        }
        [data-testid="stDataFrame"] table {
            background-color: #ffffff !important;
        }
        [data-testid="stDataFrame"] th {
            background-color: #e9ecef !important;
            color: #0e1117 !important;
        }
        [data-testid="stDataFrame"] td {
            background-color: #ffffff !important;
            color: #0e1117 !important;
        }
        [data-testid="stDataFrame"] * {
            color: #0e1117 !important;
        }
        div[data-testid="stHorizontalBlock"] {
            background-color: #ffffff;
        }
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa !important;
        }
        [data-testid="stSidebar"] * {
            color: #0e1117 !important;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #1f77b4 !important;
        }
        /* Sidebar selectbox styling */
        [data-testid="stSidebar"] [data-testid="stSelectbox"] {
            background-color: #e9ecef !important;
        }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] * {
            color: #0e1117 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    plotly_template = 'plotly_white'
    bg_color = '#ffffff'
    plot_bg_color = '#ffffff'
    font_color = '#0e1117'
    section_header_color = '#1f77b4'

# Header
st.markdown('<p class="main-header">FitSync - Personal Health Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Track your health metrics and optimize your recovery</p>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_processed_data():
    """Load and cache the processed data."""
    return process_data()

try:
    df = load_processed_data()
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    time_range = st.sidebar.selectbox(
        "Select Time Range", 
        options=["Last 7 Days", "Last 30 Days", "All time"], 
        index=2
    )
    
    # Filter DataFrame based on selection
    if time_range == "Last 7 Days":
        cutoff_date = df['Date'].max() - pd.Timedelta(days=7)
        filtered_df = df[df['Date'] >= cutoff_date]
    elif time_range == "Last 30 Days":
        cutoff_date = df['Date'].max() - pd.Timedelta(days=30)
        filtered_df = df[df['Date'] >= cutoff_date]
    else:  # All time
        filtered_df = df
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About FitSync")
    st.sidebar.info(
        "FitSync helps you monitor your health metrics and optimize your recovery. "
        "Track your steps, sleep, heart rate, and recovery score over time."
    )
    
    # Key Metrics
    st.markdown(f'<h2 style="color: {section_header_color};">📈 Key Metrics</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_steps = filtered_df['Steps'].mean()
        st.metric(
            label="Average Daily Steps",
            value=f"{avg_steps:,.0f}",
            delta=f"{(avg_steps - 7500):.0f} from goal"
        )
    
    with col2:
        avg_sleep = filtered_df['Sleep_Hours'].mean()
        st.metric(
            label="Average Sleep (hours)",
            value=f"{avg_sleep:.1f}",
            delta=f"{(avg_sleep - 7):.1f} from recommended"
        )
    
    with col3:
        avg_heart_rate = filtered_df['Heart_Rate_bpm'].mean()
        st.metric(
            label="Average Heart Rate (bpm)",
            value=f"{avg_heart_rate:.0f}",
            delta=f"{(68 - avg_heart_rate):.0f} from baseline"
        )
    
    with col4:
        avg_recovery = filtered_df['Recovery_score'].mean()
        st.metric(
            label="Average Recovery Score",
            value=f"{avg_recovery:.1f}",
            delta=f"{(avg_recovery - 50):.1f} from baseline"
        )
    
    st.markdown("---")
    
    # Visualizations
    st.markdown(f'<h2 style="color: {section_header_color};">📊 Health Trends</h2>', unsafe_allow_html=True)
    
    # Row 1: Steps and Sleep
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<h3 style="color: {font_color};">👣 Daily Steps</h3>', unsafe_allow_html=True)
        fig_steps = px.line(
            filtered_df, 
            x='Date', 
            y='Steps',
            labels={'Steps': 'Steps', 'Date': 'Date'},
            template=plotly_template
        )
        fig_steps.add_hline(y=7500, line_dash="dash", line_color="green", 
                           annotation_text="Recommended (7,500)")
        fig_steps.update_traces(line_color='#1f77b4', line_width=2)
        fig_steps.update_layout(
            height=350,
            paper_bgcolor=bg_color,
            plot_bgcolor=plot_bg_color,
            font=dict(color=font_color)
        )
        st.plotly_chart(fig_steps, use_container_width=True)
    
    with col2:
        st.markdown(f'<h3 style="color: {font_color};">😴 Sleep Hours</h3>', unsafe_allow_html=True)
        fig_sleep = px.line(
            filtered_df, 
            x='Date', 
            y='Sleep_Hours',
            labels={'Sleep_Hours': 'Sleep (hours)', 'Date': 'Date'},
            template=plotly_template
        )
        fig_sleep.add_hline(y=7, line_dash="dash", line_color="green", 
                           annotation_text="Recommended (7 hrs)")
        fig_sleep.update_traces(line_color='#ff7f0e', line_width=2)
        fig_sleep.update_layout(
            height=350,
            paper_bgcolor=bg_color,
            plot_bgcolor=plot_bg_color,
            font=dict(color=font_color)
        )
        st.plotly_chart(fig_sleep, use_container_width=True)
    
    # Row 2: Heart Rate and Recovery Score
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<h3 style="color: {font_color};">❤️ Heart Rate</h3>', unsafe_allow_html=True)
        fig_hr = px.line(
            filtered_df, 
            x='Date', 
            y='Heart_Rate_bpm',
            labels={'Heart_Rate_bpm': 'Heart Rate (bpm)', 'Date': 'Date'},
            template=plotly_template
        )
        fig_hr.add_hline(y=68, line_dash="dash", line_color="green", 
                        annotation_text="Baseline (68 bpm)")
        fig_hr.update_traces(line_color='#d62728', line_width=2)
        fig_hr.update_layout(
            height=350,
            paper_bgcolor=bg_color,
            plot_bgcolor=plot_bg_color,
            font=dict(color=font_color)
        )
        st.plotly_chart(fig_hr, use_container_width=True)
    
    with col2:
        st.markdown(f'<h3 style="color: {font_color};">🔄 Recovery Score</h3>', unsafe_allow_html=True)
        fig_recovery = px.line(
            filtered_df, 
            x='Date', 
            y='Recovery_score',
            labels={'Recovery_score': 'Recovery Score', 'Date': 'Date'},
            template=plotly_template
        )
        fig_recovery.add_hline(y=50, line_dash="dash", line_color="gray", 
                              annotation_text="Baseline (50)")
        fig_recovery.update_traces(line_color='#2ca02c', line_width=2)
        fig_recovery.update_layout(
            height=350,
            yaxis_range=[0, 100],
            paper_bgcolor=bg_color,
            plot_bgcolor=plot_bg_color,
            font=dict(color=font_color)
        )
        st.plotly_chart(fig_recovery, use_container_width=True)
    
    st.markdown("---")
    
    # Combined Analysis
    st.markdown(f'<h2 style="color: {section_header_color};">🔍 Combined Analysis</h2>', unsafe_allow_html=True)
    
    # Correlation heatmap
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'<h3 style="color: {font_color};">Correlation Matrix</h3>', unsafe_allow_html=True)
        corr_columns = ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm', 'Recovery_score']
        correlation_matrix = filtered_df[corr_columns].corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto='.2f',
            color_continuous_scale='RdBu_r',
            aspect='auto',
            labels=dict(color="Correlation"),
            template=plotly_template
        )
        fig_corr.update_layout(
            height=400,
            paper_bgcolor=bg_color,
            plot_bgcolor=plot_bg_color,
            font=dict(color=font_color)
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        st.markdown(f'<h3 style="color: {font_color};">Recovery Score Distribution</h3>', unsafe_allow_html=True)
        fig_dist = px.histogram(
            filtered_df, 
            x='Recovery_score',
            nbins=20,
            labels={'Recovery_score': 'Recovery Score', 'count': 'Frequency'},
            template=plotly_template
        )
        fig_dist.update_traces(marker_color='#2ca02c')
        fig_dist.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor=bg_color,
            plot_bgcolor=plot_bg_color,
            font=dict(color=font_color)
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    st.markdown("---")
    
    # Data Table
    st.markdown(f'<h2 style="color: {section_header_color};">📋 Detailed Data</h2>', unsafe_allow_html=True)
    
    # Format the dataframe for display
    display_df = filtered_df.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    display_df['Steps'] = display_df['Steps'].apply(lambda x: f"{x:,.0f}")
    display_df['Sleep_Hours'] = display_df['Sleep_Hours'].apply(lambda x: f"{x:.1f}")
    display_df['Heart_Rate_bpm'] = display_df['Heart_Rate_bpm'].apply(lambda x: f"{x:.0f}")
    display_df['Recovery_score'] = display_df['Recovery_score'].apply(lambda x: f"{x:.1f}")
    
    # Display table with option to download
    st.dataframe(
        display_df.tail(30), 
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="fitsync_health_data.csv",
        mime="text/csv",
    )
    
except FileNotFoundError:
    st.error("❌ Error: Could not find the health data file. Please ensure 'data/health_data.csv' exists.")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.info("Please check that your data file is properly formatted and all required columns are present.")

# Footer
st.markdown("---")
footer_color = '#8b949e' if st.session_state.dark_mode else '#666'
st.markdown(
    f"<div style='text-align: center; color: {footer_color}; padding: 20px;'>" 
    "FitSync Dashboard | Built with Streamlit | © 2024"
    "</div>", 
    unsafe_allow_html=True
)
