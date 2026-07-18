import matplotlib.pyplot as plt
import seaborn as sns
import os

FIG_DIR = '../reports/figures'
os.makedirs(FIG_DIR, exist_ok=True)

def plot_all_eda(df):
    """MODULAR: One function to rule them all. Handles all 5 visuals."""
    # 1. Confidence
    plt.figure(figsize=(6,3)); sns.countplot(data=df, x='confidence', hue='confidence', palette='viridis', legend=False)
    plt.savefig(f"{FIG_DIR}/confidence.png"); plt.show()
    
    # 2. Coverage
    df['year'] = df['observation_date'].dt.year
    cov = df[df['record_type']=='observation'].pivot_table(index='indicator_code', columns='year', values='value_numeric', aggfunc='count')
    plt.figure(figsize=(10,6)); sns.heatmap(cov, cmap="YlGnBu"); plt.savefig(f"{FIG_DIR}/coverage.png"); plt.show()
    
    # 3. Trajectory
    traj = df[df['indicator_code']=='ACC_OWNERSHIP'].sort_values('observation_date')
    plt.figure(figsize=(10,4)); plt.plot(traj['observation_date'], traj['value_numeric'], marker='o'); 
    plt.savefig(f"{FIG_DIR}/trajectory.png"); plt.show()
    
    # 4. Usage
    usage = df[df['indicator_code'].isin(['ACC_MM_ACCOUNT', 'USG_P2P_VALUE'])]
    plt.figure(figsize=(10,4)); sns.barplot(data=usage, x='year', y='value_numeric', hue='indicator_code')
    plt.savefig(f"{FIG_DIR}/usage.png"); plt.show()
    
    # 5. Timeline
    plt.figure(figsize=(12,5)); plt.plot(traj['observation_date'], traj['value_numeric'])
    for _, r in df[df['record_type']=='event'].iterrows(): plt.axvline(x=r['observation_date'], color='r', ls='--')
    plt.savefig(f"{FIG_DIR}/timeline.png"); plt.show()