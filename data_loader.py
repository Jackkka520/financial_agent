import pandas as pd

def load_csv_data(path):
    """Load data from CSV file (raw data only, no derived metrics)"""
    return pd.read_csv(path)