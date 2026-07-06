import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as px_go
import os
from datetime import datetime

# Set page config to wide layout and set title and favicon
st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM GLASSMORPHIC DESIGN ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Main font override */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Outfit', sans-serif;
}

/* Base page background adjustments */
.main {
    background: #0B0F19;
    color: #E2E8F0;
}

/* Glassmorphic Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
}

section[data-testid="stSidebar"] .stMarkdown h2, 
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #F8FAFC;
    font-weight: 600;
}

/* Glassmorphic KPI Cards */
.kpi-card {
    background: rgba(22, 28, 45, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #6366F1, #A855F7, #EC4899);
}

.kpi-card:hover {
    transform: translateY(-6px);
    border-color: rgba(168, 85, 247, 0.4);
    box-shadow: 0 12px 40px 0 rgba(168, 85, 247, 0.2);
}

.kpi-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.kpi-title {
    font-size: 13px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.kpi-value {
    font-size: 34px;
    font-weight: 700;
    color: #F8FAFC;
    background: linear-gradient(120deg, #FFFFFF, #CBD5E1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}

.kpi-subtitle {
    font-size: 11px;
    color: #64748B;
    margin-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.custom-badge {
    padding: 3px 8px;
    border-radius: 9999px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: inline-block;
}

.custom-badge.success {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.custom-badge.warning {
    background-color: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.custom-badge.critical {
    background-color: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.custom-badge.info {
    background-color: rgba(59, 130, 246, 0.15);
    color: #60A5FA;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

/* Beautiful Title Banner */
.title-banner {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 20px;
    padding: 30px 40px;
    margin-bottom: 30px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    position: relative;
    overflow: hidden;
}

.title-banner::after {
    content: '';
    position: absolute;
    right: -10%;
    top: -50%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
    filter: blur(40px);
    pointer-events: none;
}

.title-banner h1 {
    font-size: 38px;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(90deg, #F8FAFC, #93C5FD, #C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}

.title-banner p {
    font-size: 15px;
    color: #94A3B8;
    margin-top: 10px;
    margin-bottom: 0;
}

/* Tab bar customization */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(15, 23, 42, 0.4);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"] {
    height: 40px;
    border-radius: 8px;
    background-color: transparent;
    border: none;
    color: #94A3B8;
    font-weight: 500;
    transition: all 0.2s ease;
    padding: 0 16px;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(99, 102, 241, 0.15) !important;
    color: #818CF8 !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    font-weight: 600 !important;
}

/* Scrollbars styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
}
::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.3);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.5);
}
</style>
""", unsafe_allow_html=True)

# Helper function to generate premium HTML metric cards
def make_kpi_card(title, value, subtitle=None, badge=None, badge_class="info"):
    badge_html = f'<span class="custom-badge {badge_class}">{badge}</span>' if badge else ''
    subtitle_html = f'<div class="kpi-subtitle"><span>{subtitle}</span>{badge_html}</div>' if subtitle else ''
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-card-header">
            <span class="kpi-title">{title}</span>
        </div>
        <div class="kpi-card-body">
            <div class="kpi-value">{value}</div>
        </div>
        {subtitle_html}
    </div>
    """

# --- DATA LOADING & CLEANING ---
@st.cache_data
def load_and_clean_data():
    csv_file = "dataset.csv"
    if not os.path.exists(csv_file):
        # Fallback to absolute path if needed
        csv_file = r"c:\Users\shriy\OneDrive\Desktop\project_1\Care_Transition_Analytics\dataset.csv"
    
    if not os.path.exists(csv_file):
        st.error(f"Error: Could not locate dataset: {csv_file}")
        return pd.DataFrame()
        
    df = pd.read_csv(csv_file)
    
    # Drop rows that are completely null or have no Date
    df = df.dropna(subset=['Date'])
    
    # Clean the column names (remove leading/trailing spaces)
    df.columns = [c.strip() for c in df.columns]
    
    # Standardize column mappings
    # Expected columns: Date, Children apprehended and placed in CBP custody*, Children in CBP custody, Children transferred out of CBP custody, Children in HHS Care, Children discharged from HHS Care
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date']) # Drop any date parsing failures
    
    # Clean numeric columns (remove commas, cast to numeric, fill NaN with 0)
    for col in df.columns:
        if col != 'Date':
            df[col] = df[col].astype(str).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
    # Sort by Date ascending
    df = df.sort_values('Date').reset_index(drop=True)
    return df

df_full = load_and_clean_data()

if df_full.empty:
    st.error("No data could be loaded. Please ensure the dataset is present in the workspace directory.")
    st.stop()

# --- SIDEBAR & FILTER CONTROLS ---
st.sidebar.markdown("## Dashboard Controls")
st.sidebar.markdown("Configure analytical dimensions and date filters.")

# Date Range Filter
min_date = df_full['Date'].min().to_pydatetime()
max_date = df_full['Date'].max().to_pydatetime()

start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Rolling Average Window
rolling_window = st.sidebar.slider(
    "Rolling Average Window (Days)",
    min_value=1,
    max_value=30,
    value=7,
    help="Smooth daily fluctuations. Default is 7-day rolling average."
)

# Backlog alert threshold configuration
backlog_threshold = st.sidebar.number_input(
    "CBP Backlog Alert Threshold",
    min_value=1,
    max_value=200,
    value=50,
    help="CBP custody levels exceeding this number will flag a warning."
)

# Temporal aggregation frequency
aggregation_freq = st.sidebar.selectbox(
    "Temporal Aggregation",
    options=["Daily", "Weekly Average", "Monthly Average"],
    index=0
)

# Filter dataset based on selected date range
mask = (df_full['Date'] >= pd.Timestamp(start_date)) & (df_full['Date'] <= pd.Timestamp(end_date))
df_filtered = df_full.loc[mask].copy()

if df_filtered.empty:
    st.warning("No data found for the selected date range. Please widen your range.")
    st.stop()

# Column Names for easy reference
col_apprehended = "Children apprehended and placed in CBP custody*"
col_in_cbp = "Children in CBP custody"
col_transferred = "Children transferred out of CBP custody"
col_in_hhs = "Children in HHS Care"
col_discharged = "Children discharged from HHS Care"

# Handle aggregation if selected
if aggregation_freq == "Weekly Average":
    df_chart = df_filtered.set_index('Date').resample('W').mean().reset_index()
    # Round metrics to integers for cleaner view
    for col in [col_apprehended, col_in_cbp, col_transferred, col_in_hhs, col_discharged]:
        df_chart[col] = df_chart[col].round(1)
    agg_label = "Weekly Avg"
elif aggregation_freq == "Monthly Average":
    df_chart = df_filtered.set_index('Date').resample('ME').mean().reset_index()
    for col in [col_apprehended, col_in_cbp, col_transferred, col_in_hhs, col_discharged]:
        df_chart[col] = df_chart[col].round(1)
    agg_label = "Monthly Avg"
else:
    df_chart = df_filtered.copy()
    agg_label = "Daily"

# Calculate rolling averages on filtered daily data for display in chart trends
df_filtered['Apprehended_Rolling'] = df_filtered[col_apprehended].rolling(window=rolling_window, center=True).mean()
df_filtered['Transferred_Rolling'] = df_filtered[col_transferred].rolling(window=rolling_window, center=True).mean()
df_filtered['Discharged_Rolling'] = df_filtered[col_discharged].rolling(window=rolling_window, center=True).mean()

# --- TOP HEADER BANNER ---
last_updated = df_full['Date'].max().strftime('%B %d, %Y')
date_range_str = f"{start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}"

st.markdown(f"""
<div class="title-banner">
    <h1>Care Transition Analytics Dashboard</h1>
    <p>Monitoring CBP-to-HHS custody transfers, backlog detection, and sponsor placement pipeline efficiency. 
    | <b>Selected Period:</b> {date_range_str} | <b>Dataset Max Date:</b> {last_updated}</p>
</div>
""", unsafe_allow_html=True)

# --- CALCULATING KEY METRICS ---
total_apprehended = df_filtered[col_apprehended].sum()
total_transferred = df_filtered[col_transferred].sum()
total_discharged = df_filtered[col_discharged].sum()

avg_cbp_custody = df_filtered[col_in_cbp].mean()
latest_cbp_custody = df_filtered[col_in_cbp].iloc[-1]
avg_hhs_care = df_filtered[col_in_hhs].mean()
latest_hhs_care = df_filtered[col_in_hhs].iloc[-1]

# Pipeline efficiency index (Transfers / Apprehensions)
if total_apprehended > 0:
    pipeline_efficiency = (total_transferred / total_apprehended)
else:
    pipeline_efficiency = 0.0

# Backlog status logic
if latest_cbp_custody > backlog_threshold * 1.5:
    backlog_status = "CRITICAL"
    backlog_class = "critical"
elif latest_cbp_custody > backlog_threshold:
    backlog_status = "WARNING"
    backlog_class = "warning"
else:
    backlog_status = "STABLE"
    backlog_class = "success"

# --- TOP METRICS GRID (5 columns) ---
m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)

with m_col1:
    st.markdown(make_kpi_card(
        title="Total Apprehensions",
        value=f"{total_apprehended:,}",
        subtitle=f"Daily Avg: {df_filtered[col_apprehended].mean():.1f} children",
        badge="CBP Incoming",
        badge_class="info"
    ), unsafe_allow_html=True)

with m_col2:
    st.markdown(make_kpi_card(
        title="Transferred to HHS",
        value=f"{total_transferred:,}",
        subtitle=f"Daily Avg: {df_filtered[col_transferred].mean():.1f} children",
        badge="CBP Outgoing",
        badge_class="info"
    ), unsafe_allow_html=True)

with m_col3:
    st.markdown(make_kpi_card(
        title="Pipeline Efficiency",
        value=f"{pipeline_efficiency:.2%}",
        subtitle="Ratio of Transfers/Apprehensions",
        badge="Healthy" if pipeline_efficiency >= 0.95 else "Bottleneck",
        badge_class="success" if pipeline_efficiency >= 0.95 else "warning"
    ), unsafe_allow_html=True)

with m_col4:
    st.markdown(make_kpi_card(
        title="CBP Custody Current",
        value=f"{latest_cbp_custody:,}",
        subtitle=f"Period Avg: {avg_cbp_custody:.1f}",
        badge=backlog_status,
        badge_class=backlog_class
    ), unsafe_allow_html=True)

with m_col5:
    st.markdown(make_kpi_card(
        title="HHS Care Current",
        value=f"{latest_hhs_care:,}",
        subtitle=f"Period Avg: {avg_hhs_care:,.1f}",
        badge="Shelter Load",
        badge_class="info"
    ), unsafe_allow_html=True)


# --- DASHBOARD TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 CBP Transitions & Backlog Detection",
    "🏠 HHS Care & Discharges",
    "🔍 Correlation & Operational Insights",
    "🗂️ Data Table Explorer"
])

# --- TAB 1: CBP TRANSITIONS & BACKLOG DETECTION ---
with tab1:
    st.markdown("### CBP-to-HHS Care Pipeline Dynamics")
    st.write("Analyze inflow (apprehensions) versus outflow (transfers) to detect bottlenecks and build-ups in short-term CBP custody.")
    
    # Custom color palette
    plotly_template = "plotly_dark"
    colors = {
        "apprehended": "#6366F1", # Indigo
        "transferred": "#10B981", # Emerald
        "custody": "#EF4444",     # Red
        "hhs_care": "#3B82F6",    # Blue
        "discharged": "#F59E0B",  # Amber
        "background": "#0F172A",
        "card_bg": "#1E293B",
        "grid": "#334155"
    }

    # Dual Column Layout for Transition Line Chart and Sankey Flow Diagram
    col_chart_left, col_chart_right = st.columns(2)

    with col_chart_left:
        # Chart 1: Apprehensions vs Transfers (Line plot with rolling avg)
        fig_transitions = px_go.Figure()
        
        # Daily or Aggregated raw lines
        fig_transitions.add_trace(px_go.Scatter(
            x=df_chart['Date'],
            y=df_chart[col_apprehended],
            mode='lines',
            name=f'{agg_label} Apprehended',
            line=dict(color=colors['apprehended'], width=1.5, dash='dot'),
            opacity=0.4
        ))
        
        fig_transitions.add_trace(px_go.Scatter(
            x=df_chart['Date'],
            y=df_chart[col_transferred],
            mode='lines',
            name=f'{agg_label} Transferred',
            line=dict(color=colors['transferred'], width=1.5, dash='dot'),
            opacity=0.4
        ))

        # Rolling averages (only show if daily to avoid double smoothing)
        if aggregation_freq == "Daily":
            fig_transitions.add_trace(px_go.Scatter(
                x=df_filtered['Date'],
                y=df_filtered['Apprehended_Rolling'],
                mode='lines',
                name=f'{rolling_window}-Day Avg Apprehended',
                line=dict(color=colors['apprehended'], width=3.5)
            ))
            
            fig_transitions.add_trace(px_go.Scatter(
                x=df_filtered['Date'],
                y=df_filtered['Transferred_Rolling'],
                mode='lines',
                name=f'{rolling_window}-Day Avg Transferred',
                line=dict(color=colors['transferred'], width=3.5)
            ))

        fig_transitions.update_layout(
            template=plotly_template,
            title="Children Apprehended vs. Transferred out of CBP Custody",
            xaxis_title="Date",
            yaxis_title="Number of Children",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor=colors['grid']),
            yaxis=dict(showgrid=True, gridcolor=colors['grid']),
            margin=dict(l=10, r=10, t=50, b=10),
            height=400
        )
        st.plotly_chart(fig_transitions, use_container_width=True)

    with col_chart_right:
        # Chart 2: Sankey Flow Diagram
        fig_sankey = px_go.Figure(data=[px_go.Sankey(
            node = dict(
              pad = 18,
              thickness = 15,
              line = dict(color = "rgba(0,0,0,0)", width = 0),
              label = [
                  f"Apprehensions ({total_apprehended:,})", 
                  f"In CBP Custody ({latest_cbp_custody:,})", 
                  f"Transferred to HHS ({total_transferred:,})", 
                  f"In HHS Shelter ({latest_hhs_care:,})", 
                  f"Discharged ({total_discharged:,})"
              ],
              color = [colors['apprehended'], colors['custody'], colors['transferred'], colors['hhs_care'], colors['discharged']]
            ),
            link = dict(
              source = [0, 0, 2, 2],
              target = [2, 1, 4, 3],
              value = [total_transferred, latest_cbp_custody, total_discharged, latest_hhs_care],
              color = ["rgba(99, 102, 241, 0.25)", "rgba(239, 68, 68, 0.25)", "rgba(16, 185, 129, 0.25)", "rgba(59, 130, 246, 0.25)"]
          ))])
        fig_sankey.update_layout(
            template=plotly_template,
            title_text="Visual Pipeline Flow (Sankey Transition Pathways)",
            font=dict(size=11, color="#F8FAFC", family="Outfit"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=50, b=10),
            height=400
        )
        st.plotly_chart(fig_sankey, use_container_width=True)

    st.markdown("---")
    
    # Chart 3: Cumulative Flow Diagram (CFD)
    df_cfd = df_filtered.sort_values('Date').copy()
    df_cfd['Cumulative Apprehensions'] = df_cfd[col_apprehended].cumsum()
    df_cfd['Cumulative Transfers'] = df_cfd[col_transferred].cumsum()
    df_cfd['Cumulative Placements'] = df_cfd[col_discharged].cumsum()
    
    fig_cfd = px_go.Figure()
    fig_cfd.add_trace(px_go.Scatter(
        x=df_cfd['Date'],
        y=df_cfd['Cumulative Apprehensions'],
        mode='lines',
        name='Cumulative Apprehended',
        line=dict(color=colors['apprehended'], width=2.5),
        fill='tonexty',
        fillcolor='rgba(99, 102, 241, 0.08)'
    ))
    fig_cfd.add_trace(px_go.Scatter(
        x=df_cfd['Date'],
        y=df_cfd['Cumulative Transfers'],
        mode='lines',
        name='Cumulative Transferred out of CBP',
        line=dict(color=colors['transferred'], width=2.5),
        fill='tonexty',
        fillcolor='rgba(16, 185, 129, 0.08)'
    ))
    fig_cfd.add_trace(px_go.Scatter(
        x=df_cfd['Date'],
        y=df_cfd['Cumulative Placements'],
        mode='lines',
        name='Cumulative Discharged from HHS',
        line=dict(color=colors['discharged'], width=2.5),
        fill='tozeroy',
        fillcolor='rgba(245, 158, 11, 0.08)'
    ))
    fig_cfd.update_layout(
        template=plotly_template,
        title="Cumulative Flow Diagram (Total Queue Influx & Efflux)",
        xaxis_title="Date",
        yaxis_title="Cumulative Number of Children",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor=colors['grid']),
        yaxis=dict(showgrid=True, gridcolor=colors['grid']),
        margin=dict(l=20, r=20, t=50, b=20),
        height=380
    )
    st.plotly_chart(fig_cfd, use_container_width=True)

    # Chart 4: CBP Custody Backlog Tracker
    st.markdown("---")
    st.markdown("### CBP Custody Levels & Backlog Alerting")
    
    fig_custody = px_go.Figure()
    
    # Area chart for children in CBP custody
    fig_custody.add_trace(px_go.Scatter(
        x=df_chart['Date'],
        y=df_chart[col_in_cbp],
        mode='lines',
        fill='tozeroy',
        name='Children in CBP Custody',
        line=dict(color=colors['custody'], width=2),
        fillcolor='rgba(239, 68, 68, 0.15)'
    ))
    
    # Horizontal line for backlog threshold
    fig_custody.add_shape(
        type="line",
        x0=df_chart['Date'].min(),
        y0=backlog_threshold,
        x1=df_chart['Date'].max(),
        y1=backlog_threshold,
        line=dict(color=colors['discharged'], width=2, dash="dash"),
        name="Warning Threshold"
    )
    
    # Annotation for threshold
    fig_custody.add_annotation(
        x=df_chart['Date'].median(),
        y=backlog_threshold + 5,
        text=f"Warning Threshold ({backlog_threshold} Children)",
        showarrow=False,
        font=dict(color=colors['discharged'], size=12),
        bgcolor="rgba(15, 23, 42, 0.8)",
        bordercolor=colors['discharged'],
        borderwidth=1,
        borderpad=4
    )

    fig_custody.update_layout(
        template=plotly_template,
        title="Children in CBP Custody Over Time vs. Policy Threshold",
        xaxis_title="Date",
        yaxis_title="Number of Children",
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor=colors['grid']),
        yaxis=dict(showgrid=True, gridcolor=colors['grid']),
        margin=dict(l=20, r=20, t=50, b=20),
        height=350
    )
    
    st.plotly_chart(fig_custody, use_container_width=True)

    # Context analysis
    critical_days = df_filtered[df_filtered[col_in_cbp] > backlog_threshold]
    pct_critical = len(critical_days) / len(df_filtered) * 100
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <h4 style="margin-top:0; color:#EF4444;">🚨 Backlog Analysis Summary</h4>
            <ul style="margin-bottom:0; font-size:14px; line-height:1.6;">
                <li><b>Days above threshold:</b> {len(critical_days)} out of {len(df_filtered)} days ({pct_critical:.1f}%)</li>
                <li><b>Peak CBP Custody:</b> {df_filtered[col_in_cbp].max()} children on {df_filtered.loc[df_filtered[col_in_cbp].idxmax(), 'Date'].strftime('%B %d, %Y')}</li>
                <li><b>Policy Context:</b> CBP facilities are designed for processing, not long-term care. A sustained volume above the warning line signifies a downstream bottleneck in HHS shelter placements.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c_col2:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <h4 style="margin-top:0; color:#10B981;">💡 Operational Mitigation Strategies</h4>
            <ul style="margin-bottom:0; font-size:14px; line-height:1.6;">
                <li><b>Fast-track transfers:</b> Scale up temporary holding facilities or prioritize cases matching existing shelter vacancies.</li>
                <li><b>Increase ORR Capacity:</b> Alert the Office of Refugee Resettlement (ORR) to activate surge capacity shelters when custody levels cross {backlog_threshold} for 3+ consecutive days.</li>
                <li><b>Discharge Flow Optimization:</b> Speed up sponsor vetting to release children from HHS, freeing up shelter beds for CBP transfers.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: HHS CARE & DISCHARGES ---
with tab2:
    st.markdown("### HHS Shelter Inventory & Discharge Analysis")
    st.write("Track the total active volume of children sheltered under HHS care and analyze their daily discharge rates to sponsors or other placements.")
    
    fig_hhs = px_go.Figure()
    
    # Children in HHS Care (line)
    fig_hhs.add_trace(px_go.Scatter(
        x=df_chart['Date'],
        y=df_chart[col_in_hhs],
        mode='lines',
        name='Children in HHS Shelter Care',
        line=dict(color=colors['hhs_care'], width=3)
    ))
    
    fig_hhs.update_layout(
        template=plotly_template,
        title="Children in HHS Care (Total Shelter Population)",
        xaxis_title="Date",
        yaxis_title="Total Children in Care",
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor=colors['grid']),
        yaxis=dict(showgrid=True, gridcolor=colors['grid']),
        margin=dict(l=20, r=20, t=50, b=20),
        height=350
    )
    
    st.plotly_chart(fig_hhs, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Daily Placements & Discharges from HHS Care")
    
    fig_discharges = px_go.Figure()
    
    # Daily/Aggregated Discharges (Bars)
    fig_discharges.add_trace(px_go.Bar(
        x=df_chart['Date'],
        y=df_chart[col_discharged],
        name=f'{agg_label} Discharged',
        marker=dict(color='rgba(245, 158, 11, 0.7)', line=dict(color=colors['discharged'], width=1))
    ))

    # Rolling average line (only if daily)
    if aggregation_freq == "Daily":
        fig_discharges.add_trace(px_go.Scatter(
            x=df_filtered['Date'],
            y=df_filtered['Discharged_Rolling'],
            mode='lines',
            name=f'{rolling_window}-Day Avg Discharges',
            line=dict(color=colors['discharged'], width=3)
        ))
        
    fig_discharges.update_layout(
        template=plotly_template,
        title="Discharged Children (Sponsor Placements/Releases)",
        xaxis_title="Date",
        yaxis_title="Number of Discharged Children",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor=colors['grid']),
        yaxis=dict(showgrid=True, gridcolor=colors['grid']),
        margin=dict(l=20, r=20, t=50, b=20),
        height=350
    )
    
    st.plotly_chart(fig_discharges, use_container_width=True)

    # Highlight metrics
    h_col1, h_col2, h_col3 = st.columns(3)
    with h_col1:
        st.metric(
            label="Peak HHS Shelter Load", 
            value=f"{df_filtered[col_in_hhs].max():,}",
            delta=f"Date: {df_filtered.loc[df_filtered[col_in_hhs].idxmax(), 'Date'].strftime('%b %d, %Y')}"
        )
    with h_col2:
        st.metric(
            label="Max Single-Day Placements",
            value=f"{int(df_filtered[col_discharged].max())}",
            delta=f"Date: {df_filtered.loc[df_filtered[col_discharged].idxmax(), 'Date'].strftime('%b %d, %Y')}"
        )
    with h_col3:
        avg_discharges = df_filtered[col_discharged].mean()
        # Estimate theoretical average length of stay context (Shelter Population / Daily discharges)
        approx_stay = avg_hhs_care / avg_discharges if avg_discharges > 0 else 0
        st.metric(
            label="Estimated Median Duration of Stay",
            value=f"{approx_stay:.1f} Days",
            delta="Derived (HHS Pop / Daily Discharges)",
            delta_color="off"
        )

# --- TAB 3: CORRELATION & OPERATIONAL INSIGHTS ---
with tab3:
    st.markdown("### Predictive Analytics & Operational Insights")
    st.write("Understand the mathematical relationships between pipeline variables to guide staffing, capacity, and logistical decisions.")
    
    o_col1, o_col2 = st.columns([2, 1])
    
    with o_col1:
        # Scatter plot of Apprehensions vs. CBP Custody
        fig_scatter = px.scatter(
            df_filtered,
            x=col_apprehended,
            y=col_in_cbp,
            color=col_transferred,
            labels={
                col_apprehended: "Apprehensions (Daily)",
                col_in_cbp: "In CBP Custody (Daily)",
                col_transferred: "Transfers to HHS"
            },
            title="Correlation: Apprehensions vs. CBP Custody (colored by Transfers)",
            color_continuous_scale=px.colors.sequential.Viridis,
            template=plotly_template
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor=colors['grid']),
            yaxis=dict(showgrid=True, gridcolor=colors['grid']),
            margin=dict(l=20, r=20, t=50, b=20),
            height=400
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with o_col2:
        # Visual Gauge Chart for Pipeline Efficiency
        fig_gauge = px_go.Figure(px_go.Indicator(
            mode = "gauge+number",
            value = pipeline_efficiency * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 150], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                'bar': {'color': "#6366F1"},
                'bgcolor': "rgba(30, 41, 59, 0.5)",
                'borderwidth': 2,
                'bordercolor': "rgba(255, 255, 255, 0.1)",
                'steps': [
                    {'range': [0, 95], 'color': 'rgba(239, 68, 68, 0.15)'},
                    {'range': [95, 100], 'color': 'rgba(245, 158, 11, 0.15)'},
                    {'range': [100, 150], 'color': 'rgba(16, 185, 129, 0.15)'}
                ],
                'threshold': {
                    'line': {'color': "#10B981", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "#F8FAFC", 'family': "Outfit"},
            title={'text': "Pipeline Transfer Efficiency (%)", 'font': {'size': 14, 'color': '#94A3B8'}, 'y': 0.82},
            height=180,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Statistical summary
        corr_val = df_filtered[col_apprehended].corr(df_filtered[col_in_cbp])
        corr_trans_custody = df_filtered[col_transferred].corr(df_filtered[col_in_cbp])
        
        st.markdown("#### Correlation Matrix & Drivers")
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.4); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); font-size: 13px;">
            <p><b>Apprehensions ⟷ CBP Custody Correlation:</b> <code style="color:#A855F7; font-size:14px; font-weight:bold;">{corr_val:.2f}</code></p>
            <p>A positive correlation indicates that higher apprehension rates directly lead to higher numbers of children in custody, signifying that transfer rates do not immediately match surge speeds.</p>
            <p><b>Transfers ⟷ CBP Custody Correlation:</b> <code style="color:#10B981; font-size:14px; font-weight:bold;">{corr_trans_custody:.2f}</code></p>
            <p>This reveals the dynamic between outgoing flow speed and remaining custody level.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Trend indicators
        recent_days = min(7, len(df_filtered))
        df_recent = df_filtered.tail(recent_days)
        df_prior = df_filtered.tail(recent_days * 2).head(recent_days)
        
        recent_app_mean = df_recent[col_apprehended].mean()
        prior_app_mean = df_prior[col_apprehended].mean()
        app_delta_pct = ((recent_app_mean - prior_app_mean) / prior_app_mean * 100) if prior_app_mean > 0 else 0
        
        recent_cbp_mean = df_recent[col_in_cbp].mean()
        prior_cbp_mean = df_prior[col_in_cbp].mean()
        cbp_delta_pct = ((recent_cbp_mean - prior_cbp_mean) / prior_cbp_mean * 100) if prior_cbp_mean > 0 else 0

        st.markdown("#### 7-Day Momentum Indicators")
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.4); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); font-size: 13px;">
            <p>📈 <b>Apprehension Trend (last 7d vs prior 7d):</b> <br/>
            Avg. {recent_app_mean:.1f} vs. {prior_app_mean:.1f} ({"+" if app_delta_pct>=0 else ""}{app_delta_pct:.1f}%)</p>
            <p>🚨 <b>CBP Custody Trend (last 7d vs prior 7d):</b> <br/>
            Avg. {recent_cbp_mean:.1f} vs. {prior_cbp_mean:.1f} ({"+" if cbp_delta_pct>=0 else ""}{cbp_delta_pct:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)

    # Monthly Seasonality Analysis
    st.markdown("---")
    st.markdown("### Seasonality Matrix: Average Daily Apprehensions & Transfers by Month")
    
    # Extract month and year from date
    df_seasonal = df_filtered.copy()
    df_seasonal['Month'] = df_seasonal['Date'].dt.strftime('%B')
    df_seasonal['MonthNum'] = df_seasonal['Date'].dt.month
    df_seasonal['Year'] = df_seasonal['Date'].dt.year
    
    # Group by Month/Year
    df_monthly_avg = df_seasonal.groupby(['Year', 'MonthNum', 'Month']).agg({
        col_apprehended: 'mean',
        col_transferred: 'mean',
        col_discharged: 'mean'
    }).reset_index().sort_values(['Year', 'MonthNum'])
    
    # Plot Monthly Seasonality Patterns
    fig_seasonal = px.bar(
        df_monthly_avg,
        x='Month',
        y=col_apprehended,
        color='Year',
        barmode='group',
        labels={col_apprehended: "Avg. Daily Apprehensions"},
        title="Seasonality: Average Daily Apprehensions by Month across Years",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template=plotly_template
    )
    
    fig_seasonal.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor=colors['grid']),
        yaxis=dict(showgrid=True, gridcolor=colors['grid']),
        margin=dict(l=20, r=20, t=50, b=20),
        height=350
    )
    
    st.plotly_chart(fig_seasonal, use_container_width=True)

# --- TAB 4: DATA TABLE EXPLORER ---
with tab4:
    st.markdown("### Raw & Filtered Data Explorer")
    st.write("Browse, search, sort, and download the underlying dataset for independent analysis or offline reporting.")
    
    # Search functionality
    search_query = st.text_input("🔍 Search by Date or Values (e.g. '2025-12', 'December')", "")
    
    df_explorer = df_filtered.copy()
    
    # Reorder columns for logical presentation
    display_cols = [
        'Date', 
        col_apprehended, 
        col_in_cbp, 
        col_transferred, 
        col_in_hhs, 
        col_discharged
    ]
    df_explorer = df_explorer[display_cols]
    
    if search_query:
        # Convert date to string to allow string matches
        df_str = df_explorer.astype(str)
        mask_search = df_str.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        df_explorer = df_explorer.loc[mask_search]
        
    st.dataframe(
        df_explorer.sort_values('Date', ascending=False),
        use_container_width=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            col_apprehended: st.column_config.NumberColumn("Apprehended", format="%d"),
            col_in_cbp: st.column_config.NumberColumn("In CBP Custody", format="%d"),
            col_transferred: st.column_config.NumberColumn("Transferred Out", format="%d"),
            col_in_hhs: st.column_config.NumberColumn("In HHS Care", format="%d"),
            col_discharged: st.column_config.NumberColumn("Discharged from HHS", format="%d")
        }
    )
    
    # Download Cleaned Data
    csv_data = df_explorer.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned CSV Dataset",
        data=csv_data,
        file_name=f"HHS_CBP_Care_Transition_Cleaned_{start_date}_to_{end_date}.csv",
        mime="text/csv",
        help="Export the filtered and cleaned data directly to a CSV file."
    )
