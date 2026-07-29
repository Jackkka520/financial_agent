import pandas as pd

def get_company_data(df, company):
    data = df[df['Company'] == company]
    if data.empty:
        return None
    return data.iloc[-1]

def query_value(df, company, metric, year=None):
    data = df[df['Company'] == company]
    if year:
        data = data[data['Year'] == year]
    if data.empty:
        return None
    return data.iloc[-1][metric]

def calculate_growth(df, company, metric, start_year, end_year):
    start = df[(df['Company'] == company) & (df['Year'] == start_year)]
    end = df[(df['Company'] == company) & (df['Year'] == end_year)]
    if start.empty or end.empty:
        return None
    start_val = start.iloc[0][metric]
    end_val = end.iloc[0][metric]
    return ((end_val - start_val) / start_val) * 100

def compare_companies(df, metric, companies=None):
    if companies is None:
        companies = df['Company'].unique().tolist()
    latest = df.groupby('Company').last()
    result = {}
    for c in companies:
        if c in latest.index:
            result[c] = latest.loc[c][metric]
    return result

def get_trend(df, company, metric):
    data = df[df['Company'] == company][['Year', metric]]
    return data.to_dict('records')

def detect_intent(query):
    q = query.lower()
    if 'growth' in q or 'increase' in q or 'trend' in q:
        return 'growth'
    if 'compare' in q or 'vs' in q or 'versus' in q:
        return 'compare'
    if 'highest' in q or 'lowest' in q or 'best' in q or 'worst' in q:
        return 'rank'
    if 'summary' in q or 'overview' in q:
        return 'summary'
    return 'query'