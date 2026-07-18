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
    if field_name not in df.columns: return
    valid = ref_df[ref_df['field'] == field_name]['code'].astype(str).str.strip().unique()
    current = df[field_name].astype(str).str.strip().unique()
    mismatch = set(current) - set(valid)
    if not mismatch: print(f"✅ {field_name} valid.")
    else: print(f"⚠️ {field_name} Mismatch: {list(mismatch)[:3]}")