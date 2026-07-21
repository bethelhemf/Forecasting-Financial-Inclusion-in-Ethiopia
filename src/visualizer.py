import plotly.express as px  # <--- THIS FIXES THE 'px' ERROR
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# DEFENSIVE: Path for saving figures
FIG_DIR = os.path.join(os.path.dirname(__file__), '../reports/figures')
os.makedirs(FIG_DIR, exist_ok=True)

def plot_indicator_trend(df, indicator_code, title_suffix="Trend"):
    """
    MODULAR: Professional trend plotter used by the notebook.
    Includes auto-saving and defensive data checks.
    """
    data = df[df['indicator_code'] == indicator_code].sort_values('observation_date')
    
    if data.empty:
        print(f"⚠️ Warning: No data found for {indicator_code}")
        return

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=data, x='observation_date', y='value_numeric', marker='o', color='#1E3A8A')
    plt.title(f"{indicator_code}: {title_suffix}")
    plt.ylabel("Value (%)")
    plt.grid(True, alpha=0.3)
    
    # Save the figure
    plt.savefig(os.path.join(FIG_DIR, f"{indicator_code.lower()}_trend.png"), bbox_inches='tight')
    plt.show()

def plot_confidence_distribution(df):
    """Visualizes data quality confidence levels."""
    if 'confidence' not in df.columns: return
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x='confidence', hue='confidence', palette='viridis', legend=False)
    plt.title("Data Confidence Distribution")
    plt.savefig(os.path.join(FIG_DIR, "confidence_distribution.png"), bbox_inches='tight')
    plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

def plot_temporal_coverage(df):
    """
    MODULAR: Creates a heatmap showing data availability over time.
    """
    # Defensive: check for required columns
    if 'indicator_code' not in df.columns or 'record_type' not in df.columns:
        print("❌ Error: Missing columns for heatmap.")
        return

    # Ensure 'year' column exists for the pivot
    if 'year' not in df.columns:
        df['year'] = pd.to_datetime(df['observation_date']).dt.year

    observations = df[df['record_type'] == 'observation']
    
    coverage = observations.pivot_table(
        index='indicator_code', 
        columns='year', 
        values='value_numeric', 
        aggfunc='count'
    )
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(coverage, cmap="YlGnBu", annot=False, cbar=False)
    plt.title("Data Availability by Indicator and Year")
    plt.show()

def plot_usage_vs_registered_comparison(df):
    """
    MODULAR: Compares Mobile Money accounts against usage drivers.
    Includes defensive checks to handle missing 'year' or indicators.
    """
    usage_indicators = ['ACC_MM_ACCOUNT', 'USG_P2P_VALUE', 'USG_TELEBIRR_USERS']
    
    # 1. Defensive Check: Ensure required columns exist
    if 'indicator_code' not in df.columns:
        print("❌ Error: 'indicator_code' column missing.")
        return

    # 2. Extract Year if not present
    if 'year' not in df.columns:
        df['year'] = pd.to_datetime(df['observation_date']).dt.year

    # 3. Filter data
    usage_df = df[df['indicator_code'].isin(usage_indicators)].sort_values('year')
    
    if usage_df.empty:
        print(f"⚠️ Warning: None of the indicators {usage_indicators} were found.")
        return

    # 4. Create Visualization
    fig = px.bar(
        usage_df, 
        x='year', 
        y='value_numeric', 
        color='indicator_code',
        barmode='group', 
        title="Usage Dynamics: Registered Accounts vs. Transaction Drivers",
        labels={'value_numeric': 'Count / Value', 'year': 'Year'},
        template="plotly_white"
    )
    
    fig.update_layout(hovermode="x unified")
    fig.show()

def plot_account_ownership_trajectory(df):
    """
    MODULAR: Visualizes Account Ownership with business-logic annotations.
    Includes defensive checks to prevent NameErrors and crashes.
    """
    # 1. Filter defensively (Handles the 'df' vs 'df_main' naming issue)
    data = df[df['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('observation_date').copy()
    
    if data.empty:
        print("⚠️ Warning: 'ACC_OWNERSHIP' data not found. Skipping plot.")
        return

    # 2. Build the interactive visualization
    fig = px.line(
        data, 
        x='observation_date', 
        y='value_numeric', 
        markers=True,
        title="Ethiopia Account Ownership Trajectory (2011-2024)",
        labels={'value_numeric': 'Account Ownership (%)', 'observation_date': 'Survey Year'},
        template="plotly_white"
    )

    # 3. Add Contextual Annotations (Addressing the 'Access Paradox')
    fig.add_annotation(x='2021-12-31', y=46, text="Telebirr Launch", showarrow=True, arrowhead=1)
    fig.add_annotation(x='2024-12-31', y=49, text="Velocity Drop (+3pp)", showarrow=True, arrowhead=1)
    
    fig.update_layout(hovermode="x unified")
    fig.show()

# ALIASES: These ensure your notebook calls don't break
def plot_account_trajectory(df): return plot_indicator_trend(df, 'ACC_OWNERSHIP', "Account Ownership Trajectory")
def plot_event_impact_timeline(df): return plot_indicator_trend(df, 'ACC_OWNERSHIP', "Impact of Events on Trends")