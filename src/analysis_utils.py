import pandas as pd

def summarize_records(df):
    """
    Production-grade summary: Handles missing values defensively.
    """
    # Defensive: Fill NaN pillars with 'EVENT/UNASSIGNED' for the summary table
    temp_df = df.copy()
    temp_df['pillar'] = temp_df['pillar'].fillna('EVENT/OTHER')
    
    summary = temp_df.groupby(['record_type', 'pillar']).size().unstack(fill_value=0)
    return summary

def get_growth_summary(df, indicator_code):
    """Calculates quantitative growth metrics (CAGR equivalent)."""
    data = df[df['indicator_code'] == indicator_code].sort_values('observation_date').copy()
    if len(data) < 2: return pd.DataFrame()
    data['growth_rate_pp'] = data['value_numeric'].diff()
    return data