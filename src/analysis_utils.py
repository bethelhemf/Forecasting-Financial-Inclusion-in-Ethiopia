import pandas as pd

def get_growth_summary(df, indicator_code):
    """
    MODULAR: Calculates Year-over-Year growth for a specific indicator.
    """
    data = df[df['indicator_code'] == indicator_code].sort_values('observation_date').copy()
    
    if len(data) < 2:
        return "Not enough data points to calculate growth."
    
    data['growth_rate'] = data['value_numeric'].pct_change() * 100
    return data[['observation_date', 'value_numeric', 'growth_rate']]

def summarize_records(df):
    """
    DEFENSIVE: Checks for required columns before grouping.
    """
    required = ['record_type', 'pillar']
    if not all(col in df.columns for col in required):
        return "❌ Error: Missing required columns for summary."
        
    return df.groupby(['record_type', 'pillar']).size().unstack(fill_value=0)