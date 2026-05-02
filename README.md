# 🏃 FitSync — Personal Health Analytics Platform

> *Turn raw health data into clear, actionable insights — all in your browser.*

---

## 📌 Project Overview

FitSync is a multi-page personal health analytics dashboard built to surface meaningful patterns from daily fitness and recovery data. The platform ingests CSV-based health records, cleans and enriches them with a custom recovery-score algorithm, and presents the results through an interactive Streamlit interface. Three purpose-built pages give users a quick snapshot on the home screen, deep KPI analysis on the Dashboard, and long-term trend exploration on the Trends & Insights page. This project demonstrates end-to-end data product ownership — from raw data processing and feature engineering through to polished, recruiter-ready visualization.

---

## ✨ Key Features

**Home**
- Hero landing page with navigation cards guiding users to each analytical section

**Dashboard**
- 4 KPI metric cards — Steps, Sleep, Heart Rate, Recovery Score — each with a delta vs goal or baseline
- Dual-axis trend line: Recovery Score and Sleep Hours overlaid on one chart
- Scatter plots: Recovery vs Steps (coloured by Sleep Hours) and Recovery vs Resting Heart Rate with OLS trendline
- 2 × 2 health trend grid with goal/baseline reference lines for every metric
- Correlation heatmap and Recovery Score distribution histogram for combined analysis
- Sidebar time-range filter (Last 7 Days / Last 30 Days / All Time) as the single source of truth for every chart on the page

**Trends & Insights**
- Summary statistics table showing mean, min, max, and standard deviation for all key metrics
- **Automated plain-English Key Insights** — sentences generated directly from the filtered data values, updating in real time as the time range changes
- Monthly average Recovery Score trend line grouped by calendar month
- 4-panel distribution histogram grid across Steps, Calories, Recovery Score, and Sleep Hours

**Platform-wide**
- 🌙 **Dark / light mode toggle** ☀️ — persists across all pages via Streamlit session state
- ⚡ **Performance caching** via `@st.cache_data` — data loads once per session, not on every interaction
- 🧮 **Custom Recovery Score algorithm** — a purpose-built formula combining sleep hours, resting heart rate, and daily steps into a single 0–100 health metric

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.1-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.17-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![GitHub Codespaces](https://img.shields.io/badge/GitHub_Codespaces-181717?style=for-the-badge&logo=github&logoColor=white)
![Continue Agent](https://img.shields.io/badge/Continue_Agent-AI_Assisted-6366F1?style=for-the-badge&logoColor=white)

---

## 📂 Project Structure

```
fitsync/
├── .streamlit/
│   └── config.toml          # Dark theme configuration
├── data/
│   └── health_data.csv      # Source health metrics
├── modules/
│   └── processor.py         # Data cleaning + recovery score logic
├── pages/
│   ├── 1_Dashboard.py       # KPIs and chart analysis
│   └── 2_Trends.py          # Histograms, monthly trends, stats
├── main.py                  # Home page
└── requirements.txt
```

---

## 📊 Pages at a Glance

| Page | Description |
|------|-------------|
| **Main** | Welcome screen with key metric overview and time-filtered charts |
| **Dashboard** | 3 KPI cards · Dual-axis trend line · Recovery vs Steps scatter · HR vs Recovery · Calories trend |
| **Trends & Insights** | Summary stats table · Monthly avg recovery line · 4-panel histogram grid |

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Toya0754/fitsync-project-LaToya-Alvarado.git
```

**2. Open in GitHub Codespaces**

Click the green **Code** button on the repository page → **Codespaces** → **Create codespace on main**.

**3. Run the app**
```bash
streamlit run main.py
```

The app will open automatically in a browser tab inside Codespaces. Use the sidebar to filter by time range and the dark-mode toggle (🌙) in the top-right to switch themes.

---

## 🤖 Built with AI

This project was developed with the assistance of **Continue Agent** inside GitHub Codespaces, used as an in-editor pair programmer to accelerate Streamlit syntax lookup, Plotly layout options, and CSS theming patterns. All architectural decisions — the data pipeline design, recovery-score algorithm, page structure, and chart selection — were planned and owned independently. Continue Agent helped reduce time spent on boilerplate so more focus could go toward the analytical logic and user experience.

---

## 📄 License

This project is for educational and portfolio purposes.
