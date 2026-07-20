import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Set page config
st.set_page_config(page_title="Ethiopia FI Forecast", layout="wide")

# Add src to path
sys.path.append(os.path.abspath('../src'))
from data_loader import load_unified_data
from modeller import ImpactModeller
from forecaster import InclusionForecaster

# --- DATA LOADING ---
@st.cache_data
def get_data():
    df_main, df_impact = load_unified_data('../data/processed/ethiopia_fi_enriched.xlsx')
    # Ensure date objects
    df_main['observation_date'] = pd.to_datetime(df_main['observation_date'])
    df_main['year'] = df_main['observation_date'].dt.year
    return df_main, df_impact

df_main, df_impact = get_data()
impact_engine = ImpactModeller(df_main, df_impact)
forecaster = InclusionForecaster(df_main, impact_engine)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Selam Analytics")
page = st.sidebar.radio("Navigation", ["Overview", "Trends Exploration", "Inclusion Forecasts", "Consortium Q&A"])

# --- PAGE 1: OVERVIEW ---
if page == "Overview":
    st.title("🇪🇹 Financial Inclusion Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Account Ownership (2024)", "49%", "3pp")
    col2.metric("Digital Payments Usage", "35%", "11pp")
    col3.metric("P2P/ATM Crossover", "1.2x", "Digital Dominant")

    st.subheader("Key Progress Indicators")
    p2p_data = df_main[df_main['indicator_code'] == 'USG_P2P_COUNT'].sort_values('observation_date')
    fig = px.area(p2p_data, x='observation_date', y='value_numeric', title="Growth in Interoperable P2P Transfers")
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: TRENDS EXPLORATION ---
elif page == "Trends Exploration":
    st.title("📈 Historical Trends Exploration")
    
    indicators = df_main['indicator_code'].unique()
    selected_ind = st.multiselect("Select Indicators to Compare", indicators, default=["ACC_OWNERSHIP", "ACC_MM_ACCOUNT"])
    
    date_range = st.slider("Select Date Range", 2011, 2024, (2014, 2024))
    
    filtered_df = df_main[(df_main['year'] >= date_range[0]) & (df_main['year'] <= date_range[1])]
    plot_df = filtered_df[filtered_df['indicator_code'].isin(selected_ind)]
    
    fig = px.line(plot_df, x='observation_date', y='value_numeric', color='indicator_code', markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.download_button("Download Selected Data", plot_df.to_csv(), "filtered_data.csv")

# --- PAGE 3: INCLUSION FORECASTS ---
elif page == "Inclusion Forecasts":
    st.title("🔮 2025–2027 Projections")
    
    scenario = st.selectbox("Select Scenario", ["base_forecast", "optimistic_scenario", "pessimistic_scenario"])
    
    # Generate Forecast using our modular engine
    fc_df = forecaster.forecast_indicator('ACC_OWNERSHIP')
    
    fig = go.Figure()
    # Base Line
    fig.add_trace(go.Scatter(x=fc_df['year'], y=fc_df[scenario], name="Selected Scenario", line=dict(width=4)))
    # Confidence Interval
    fig.add_trace(go.Scatter(x=fc_df['year'], y=fc_df['ci_upper'], fill=None, mode='lines', line_color='rgba(0,0,255,0)', showlegend=False))
    fig.add_trace(go.Scatter(x=fc_df['year'], y=fc_df['ci_lower'], fill='tonexty', mode='lines', line_color='rgba(0,0,255,0)', name="95% Confidence Interval"))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Progress to 60% Target
    target = 60.0
    current_best = fc_df.iloc[-1][scenario]
    st.subheader(f"Progress Toward NFIS-II 60% Target")
    st.progress(min(current_best/target, 1.0))
    st.write(f"Model predicts reaching {current_best:.1f}% by 2027.")

# --- PAGE 4: Q&A ---
elif page == "Consortium Q&A":
    st.title("💡 Strategic Insights")
    st.info("**What drives inclusion?** Account opening is driven by Digital ID (Fayda), while usage is driven by interoperability.")
    st.warning("**Why the 3pp slowdown?** Market saturation of the 'already banked' segment using mobile money as a secondary tool.")