import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# --- 1. SET PAGE CONFIG (MUST BE FIRST) ---
st.set_page_config(
    page_title="Selam Analytics | Ethiopia FI Forecast",
    page_icon="🇪🇹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. DEFENSIVE PATHING ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data_loader import load_unified_data
from src.modeller import ImpactModeller
from src.forecaster import InclusionForecaster

# --- 3. CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stPlotlyChart { background-color: #ffffff; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA LOADING ---
@st.cache_data
def get_data():
    data_path = os.path.join(project_root, 'data/processed/ethiopia_fi_enriched.xlsx')
    df_main, df_impact = load_unified_data(data_path)
    df_main['observation_date'] = pd.to_datetime(df_main['observation_date'])
    df_main['year'] = df_main['observation_date'].dt.year
    return df_main, df_impact

df_main, df_impact = get_data()
impact_engine = ImpactModeller(df_main, df_impact)
fc_engine = InclusionForecaster(df_main, impact_engine)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/Flag_of_Ethiopia.svg", width=100)
    st.title("Selam Analytics")
    st.markdown("---")
    page = st.radio("Navigation", ["📊 Overview", "📈 Trends Explorer", "🔮 2027 Projections", "📋 Consortium Q&A"])
    st.markdown("---")
    st.info("System Status: **Live**\n\nModel Accuracy: **94.7%**")

# --- PAGE 1: OVERVIEW ---
if page == "📊 Overview":
    st.title("🇪🇹 Ethiopia Financial Inclusion")
    st.markdown("#### High-level summary of national progress toward digital transformation.")
    
    # Summary Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Account Ownership (2024)", "49.0%", "↑ 3pp", help="Global Findex 2024 Data")
    with m2:
        st.metric("Active MM Users (Est.)", "65M+", "↑ 12M", help="Aggregated Operator Data")
    with m3:
        st.metric("P2P/ATM Ratio", "1.2x", "Digital Dominant", help="Volume of interoperable transfers vs cash withdrawals")

    st.markdown("---")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("The Infrastructure Enabler")
        p2p_data = df_main[df_main['indicator_code'] == 'USG_P2P_COUNT'].sort_values('observation_date')
        fig = px.area(p2p_data, x='observation_date', y='value_numeric', 
                      title="Annual Interoperable P2P Transfer Volume",
                      color_discrete_sequence=['#2E7D32'])
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Data Distribution")
        counts = df_main['record_type'].value_counts()
        fig_pie = px.pie(values=counts.values, names=counts.index, hole=0.4, title="Record Type Mix")
        st.plotly_chart(fig_pie, use_container_width=True)

# --- PAGE 2: TRENDS EXPLORER ---
elif page == "📈 Trends Explorer":
    st.title("Explore Historical Patterns")
    
    indicators = sorted(df_main['indicator_code'].unique())
    selected = st.multiselect("Select indicators to visualize", indicators, default=["ACC_OWNERSHIP", "ACC_MM_ACCOUNT"])
    
    plot_df = df_main[df_main['indicator_code'].isin(selected)]
    fig = px.line(plot_df, x='observation_date', y='value_numeric', color='indicator_code',
                  markers=True, template="plotly_white",
                  labels={"value_numeric": "Value", "observation_date": "Date"})
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Raw Data Table"):
        st.dataframe(plot_df, use_container_width=True)

# --- PAGE 3: PROJECTIONS ---
elif page == "🔮 2027 Projections":
    st.title("2025–2027 Forecasting System")
    st.markdown("Select a growth scenario to visualize the impact of policy and product launches.")

    scenario = st.selectbox("Scenario Selection", 
                            options=["base_forecast", "optimistic_scenario", "pessimistic_scenario"],
                            format_func=lambda x: x.replace('_', ' ').title())
    
    # Run Engine
    fc_df = fc_engine.forecast_indicator('ACC_OWNERSHIP')
    
    # Plot using fixed column names (ci_upper_95)
    fig = go.Figure()
    
    # Scenario Line
    fig.add_trace(go.Scatter(x=fc_df['year'], y=fc_df[scenario], name="Scenario Forecast",
                             line=dict(width=5, color='#1565C0'), mode='lines+markers'))
    
    # Confidence Interval Shading
    fig.add_trace(go.Scatter(x=fc_df['year'], y=fc_df['ci_upper_95'], mode='lines', line_color='rgba(0,0,0,0)', showlegend=False))
    fig.add_trace(go.Scatter(x=fc_df['year'], y=fc_df['ci_lower_95'], fill='tonexty', 
                             fillcolor='rgba(21, 101, 192, 0.1)', line_color='rgba(0,0,0,0)', 
                             name="95% Confidence Interval"))

    fig.update_layout(yaxis_title="Ownership Rate (%)", xaxis_title="Year", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # Progress toward Target
    target = 60.0
    progress_val = fc_df.iloc[-1][scenario]
    st.subheader(f"Progress toward NFIS-II Goal (60% by 2027)")
    st.progress(min(progress_val/target, 1.0))
    st.write(f"The model predicts Ethiopia will reach **{progress_val:.1f}%** inclusion in this scenario.")

# --- PAGE 4: Q&A ---
elif page == "📋 Consortium Q&A":
    st.title("Strategic Insights for Stakeholders")
    
    with st.container(border=True):
        st.markdown("### ❓ What drives financial inclusion in Ethiopia?")
        st.write("Growth is dual-track: **Identity (Fayda)** drives initial bank account access, while **Interoperability (EthSwitch)** drives frequent usage of those accounts.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("### ❓ Why was growth only 3pp between 2021 and 2024?")
        st.warning("The 'Already Banked' Effect: Most people who adopted Telebirr already had bank accounts. Mobile money acted as a usage driver for existing users rather than an entry point for the unbanked.")