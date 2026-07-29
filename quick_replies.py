import pandas as pd

def quick_reply(query, df):
    """
    Fast path: answer common queries directly without calling LLM
    Returns None if no match (go to Agent)
    """
    query_lower = query.lower()

    # ===== 动态识别公司名 =====
    company = None
    for comp in df['Company'].unique():
        if comp.lower() in query_lower:
            company = comp
            break

    if not company:
        return None

    data = df[df['Company'] == company]
    if data.empty:
        return None

    latest = data.iloc[-1]

    # Revenue
    if 'revenue' in query_lower or 'sales' in query_lower:
        return f"📊 {company} {latest['Year']} Revenue: ${latest['Total Revenue']:,}M (${latest['Total Revenue']/1000:.1f}B)"

    # Profit / Net Income
    if 'profit' in query_lower or 'net income' in query_lower:
        net_margin = (latest['Net Income'] / latest['Total Revenue']) * 100 if latest['Total Revenue'] != 0 else 0
        return f"💰 {company} {latest['Year']} Net Income: ${latest['Net Income']:,}M, Net Margin: {net_margin:.1f}%"

    # Debt / Liabilities
    if 'debt' in query_lower or 'liabilities' in query_lower:
        debt_ratio = (latest['Total Liabilities'] / latest['Total Assets']) * 100 if latest['Total Assets'] != 0 else 0
        return f"🏦 {company} {latest['Year']}: Assets ${latest['Total Assets']:,}M, Liabilities ${latest['Total Liabilities']:,}M, Debt Ratio {debt_ratio:.1f}%"

    return None