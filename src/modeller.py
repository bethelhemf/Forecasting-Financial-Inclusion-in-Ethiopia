import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class ImpactModeller:
    def __init__(self, df_main, df_impact):
        self.df_events = df_main[df_main['record_type'] == 'event'].copy()
        self.df_impacts = df_impact.copy()
        self.matrix = None

    def build_association_matrix(self):
        """
        Sub-task: Build Event-Indicator Matrix.
        Rows: Events, Columns: Indicators, Values: Magnitudes.
        """
        # Defensive check: Ensure columns exist
        if self.df_impacts.empty:
            return "❌ Error: Impact sheet is empty."

        # Pivot to create the matrix
        matrix = self.df_impacts.pivot_table(
            index='parent_id', 
            columns='related_indicator', 
            values='impact_magnitude',
            aggfunc='first'
        ).fillna(0)
        
        self.matrix = matrix
        return matrix

    def get_event_details(self):
        """Sub-task: Join impact data with event details."""
        merged = pd.merge(
            self.df_impacts, 
            self.df_events[['indicator_code', 'observation_date', 'category']], 
            left_on='parent_id', 
            right_on='indicator_code', 
            how='inner'
        )
        return merged

    def calculate_total_shock(self, target_indicator, target_date):
        """
        Sub-task: Model temporal effects and combine multiple events.
        Representing event effects over time with lags.
        """
        merged = self.get_event_details()
        relevant_impacts = merged[merged['related_indicator'] == target_indicator]
        
        total_pp_change = 0
        target_date = pd.to_datetime(target_date)

        for _, row in relevant_impacts.iterrows():
            event_date = pd.to_datetime(row['observation_date'])
            # Apply Lag logic: Impact only starts after 'lag_months'
            effective_date = event_date + pd.DateOffset(months=row['lag_months'])
            
            if target_date >= effective_date:
                magnitude = row['impact_magnitude']
                # Convert direction to multiplier
                direction = 1 if row['impact_direction'] == 'positive' else -1
                total_pp_change += (magnitude * direction)
        
        return total_pp_change