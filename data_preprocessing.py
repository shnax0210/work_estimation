import pandas as pd

def filter_estimated_tasks(df):
    return df[df['normal'] != '?'].copy()

def prepare_data_for_calculation_of_normal(df):
    estimated_df = filter_estimated_tasks(df)
    estimated_df['normal'] = estimated_df['normal'].astype(float)
    estimated_df = estimated_df.rename(columns={"id": "id", "normal": "estimate"})
    return estimated_df[['id', 'estimate']]

def prepare_data_with_all_estimations(df):
    full_estimated_df = filter_estimated_tasks(df)
    full_estimated_df['normal'] = full_estimated_df['normal'].astype(float)
    full_estimated_df['min'] = full_estimated_df['min'].astype(float)
    full_estimated_df['max'] = full_estimated_df['max'].astype(float)

    return full_estimated_df
