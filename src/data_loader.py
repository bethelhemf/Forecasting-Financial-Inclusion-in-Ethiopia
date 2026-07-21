import pandas as pd
import os

def load_unified_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    df_main = pd.read_excel(file_path, sheet_name='ethiopia_fi_unified_data')
    df_impact = pd.read_excel(file_path, sheet_name='Impact_sheet')
    df_main['observation_date'] = pd.to_datetime(df_main['observation_date'])
    return df_main, df_impact


def validate_categorical_data(df, ref_df, field_name):
    """
    MODULAR & DEFENSIVE: Validates data against the master reference table.
    - Filters reference table by 'field'
    - Ignores null values (expected for pillars in events)
    - Normalizes strings to prevent 'invisible' space errors
    """
    if field_name not in df.columns:
        print(f"⚠️ Validation Skipped: '{field_name}' not found.")
        return

    # 1. Filter Reference table for this specific field (e.g., indicator_code)
    valid_list = ref_df[ref_df['field'] == field_name]['code'].astype(str).str.strip().unique()
    
    # 2. Get current values from data, drop NaNs (Professional practice)
    current_values = df[field_name].dropna().astype(str).str.strip().unique()

    # 3. Find Mismatches
    mismatched = set(current_values) - set(valid_list)

    if not mismatched:
        print(f"✅ {field_name}: Data is 100% compliant with schema.")
    else:
        print(f"⚠️ {field_name} Mismatch Found: {list(mismatched)}")
        print(f"   (Note: These codes exist in data but are missing from the '{field_name}' section of reference_codes.xlsx)")