import pandas as pd
import numpy as np

class ImpactModeller:
    def __init__(self, df_main, df_impact):
        # 1. Clean Column Names
        df_main.columns = df_main.columns.str.strip().str.lower()
        df_impact.columns = df_impact.columns.str.strip().str.lower()

        self.df_main = df_main.copy()
        self.df_impacts = df_impact.copy()
        
        # 2. Sync IDs (Descriptive to Generic)
        id_map = {
            'EVT_TELEBIRR': 'EVT_0001', 'EVT_SAFARICOM': 'EVT_0002',
            'EVT_MPESA': 'EVT_0003', 'EVT_FAYDA': 'EVT_0004',
            'EVT_FX_REFORM': 'EVT_0005', 'EVT_CROSSOVER': 'EVT_0007',
            'EVT_MPESA_INTEROP': 'EVT_0008', 'EVT_NFIS2': 'EVT_0010'
        }
        self.df_main['indicator_code'] = self.df_main['indicator_code'].astype(str).str.strip().str.upper()
        self.df_main['indicator_code'] = self.df_main['indicator_code'].replace(id_map)
        
        # 3. Create a Date Lookup Dictionary
        event_df = self.df_main[self.df_main['record_type'].str.lower().str.strip() == 'event']
        self.date_lookup = pd.Series(
            event_df.observation_date.values, 
            index=event_df.indicator_code
        ).to_dict()

        # 4. Magnitude Map
        self.mag_map = {'high': 5.0, 'medium': 2.0, 'low': 0.5, '0': 0.0, '0.0': 0.0}

    def build_association_matrix(self):
        """Builds a numeric matrix for the heatmap."""
        df_num = self.df_impacts.copy()
        df_num['magnitude_num'] = df_num['impact_magnitude'].astype(str).str.lower().str.strip().map(self.mag_map).fillna(0.0)
        
        matrix = df_num.pivot_table(
            index='parent_id', 
            columns='related_indicator', 
            values='magnitude_num', 
            aggfunc='first'
        ).fillna(0.0)
        return matrix.astype(float)

    def calculate_total_shock(self, target_indicator, target_date):
        """Calculates combined shock using the Date Lookup dictionary."""
        try:
            target_dt = pd.to_datetime(target_date)
            target_ind = str(target_indicator).strip().upper()

            relevant = self.df_impacts[self.df_impacts['related_indicator'].str.upper().str.strip() == target_ind].copy()
            
            if relevant.empty:
                return 0.0

            total_shock = 0.0
            for _, row in relevant.iterrows():
                parent_id = str(row['parent_id']).strip().upper()
                
                if parent_id in self.date_lookup:
                    event_dt = pd.to_datetime(self.date_lookup[parent_id])
                    
                    try:
                        lag = int(float(row['lag_months'])) if pd.notnull(row['lag_months']) else 0
                    except:
                        lag = 0
                    
                    effective_dt = event_dt + pd.DateOffset(months=lag)
                    
                    if target_dt >= effective_dt:
                        mag_str = str(row['impact_magnitude']).lower().strip()
                        mag_num = self.mag_map.get(mag_str, 0.0)
                        
                        # Robust Direction Check
                        dir_str = str(row['impact_direction']).lower().strip()
                        positive_terms = ['positive', 'increase', 'up', '+', 'pos', 'higher']
                        is_positive = any(term in dir_str for term in positive_terms)
                        
                        direction = 1 if is_positive else -1
                        total_shock += (mag_num * direction)
            
            return float(total_shock)
        except Exception as e:
            print(f"⚠️ Modeller Error: {e}")
            return 0.0