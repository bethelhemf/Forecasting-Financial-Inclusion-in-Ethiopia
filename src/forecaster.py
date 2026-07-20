import pandas as pd
import numpy as np

class InclusionForecaster:
    def __init__(self, df_main, impact_engine):
        """
        InclusionForecaster connects historical baseline trends with 
        event shock multipliers from the ImpactModeller.
        """
        self.df_main = df_main.copy()
        self.engine = impact_engine

    def get_historical_baseline(self, indicator_code):
        """Extracts historical observation points for an indicator."""
        ind_code = indicator_code.strip().upper()
        data = self.df_main[
            (self.df_main['record_type'].str.lower().str.strip() == 'observation') & 
            (self.df_main['indicator_code'].str.upper().str.strip() == ind_code)
        ].copy()
        
        data = data.dropna(subset=['value_numeric', 'observation_date']).sort_values('observation_date')
        data['year'] = pd.to_datetime(data['observation_date']).dt.year
        return data

    def fit_linear_trend(self, indicator_code):
        """Fits a simple linear regression on historical observation points."""
        hist = self.get_historical_baseline(indicator_code)
        if len(hist) < 2:
            # Fallback if sparse: default to flat rate or last known value
            latest_val = hist['value_numeric'].iloc[-1] if not hist.empty else 49.0
            return lambda yr: latest_val, 0.0

        x = hist['year'].values
        y = hist['value_numeric'].values
        slope, intercept = np.polyfit(x, y, 1)
        
        # Calculate standard residual error for confidence intervals
        y_pred = slope * x + intercept
        residuals = y - y_pred
        std_error = np.std(residuals) if len(residuals) > 2 else 1.5
        
        return (lambda yr: slope * yr + intercept), std_error

    def forecast_indicator(self, indicator_code, target_years=[2025, 2026, 2027]):
        """
        Generates Base, Optimistic, and Pessimistic forecasts with 95% Confidence Bounds.
        """
        trend_fn, std_err = self.fit_linear_trend(indicator_code)
        results = []

        for yr in target_years:
            target_date = f"{yr}-12-31"
            
            # 1. Baseline projection (Pure trend)
            baseline = float(trend_fn(yr))
            
            # 2. Event Shock from ImpactModeller (Task 3 Engine)
            shock = self.engine.calculate_total_shock(indicator_code, target_date)
            
            # 3. Base Scenario (Baseline + Full Shock)
            base_forecast = min(100.0, max(0.0, baseline + shock))
            
            # 4. Scenarios
            # Optimistic: +20% shock multiplier + 1.96*std_err
            optimistic = min(100.0, base_forecast + 0.2 * abs(shock) + 1.96 * std_err)
            
            # Pessimistic: -30% shock delay/decay - 1.96*std_err
            pessimistic = max(0.0, base_forecast - 0.3 * abs(shock) - 1.96 * std_err)
            
            # 5. Confidence Bounds (95% CI around base)
            ci_lower = max(0.0, base_forecast - 1.96 * std_err)
            ci_upper = min(100.0, base_forecast + 1.96 * std_err)

            results.append({
                'year': yr,
                'indicator_code': indicator_code,
                'baseline_trend': round(baseline, 2),
                'event_shock_pp': round(shock, 2),
                'base_forecast': round(base_forecast, 2),
                'optimistic_scenario': round(optimistic, 2),
                'pessimistic_scenario': round(pessimistic, 2),
                'ci_lower_95': round(ci_lower, 2),
                'ci_upper_95': round(ci_upper, 2)
            })

        return pd.DataFrame(results)