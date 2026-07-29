import pandas as pd
from openai import OpenAI
from config import ZHIPU_API_KEY, MODEL_NAME, BASE_URL
from logger import log_usage

client = OpenAI(
    api_key=ZHIPU_API_KEY,
    base_url=BASE_URL
)

SYSTEM_PROMPT_NORMAL = """You are a financial data analyst. Use the provided data to answer questions.

**Calculation Rules (ALWAYS follow):**
- Net Margin = Net Income / Total Revenue * 100
- Revenue Growth = (Current Year - Previous Year) / Previous Year * 100  
- Debt Ratio = Total Liabilities / Total Assets * 100
- Cash/Revenue Ratio = Operating Cash Flow / Total Revenue * 100

**Recommendation Rules (MANDATORY when asked):**
1. You MUST pick ONE company
2. Use these exact criteria:
   - Conservative: lowest debt ratio + stable profit margin + positive cash flow
   - High Growth: highest revenue growth + improving net margin + cash flow growth
3. Format your recommendation:
   **Recommendation:** [Company]
   **Reasons:** (3 bullet points with numbers)
   **Risk:** (1 bullet point)

**Context Rules:**
- If user says "How about 2024?" and you were just talking about a company, answer about that company's 2024
- Maintain conversation context

Use English. Be direct, data-driven, and DECISIVE."""

SYSTEM_PROMPT_SHORT = """You are a financial data analyst. Answer with ONLY the key numbers, no explanations.

Rules:
- Just give the number, nothing else
- For revenue: "$XXXM"
- For net income: "$XXXM"
- For margin: "X.X%"
- For growth: "X.X%"
- For recommendation: just the company name

Example:
User: What is Micron's revenue?
Assistant: $37,378M

User: Recommend a conservative stock
Assistant: Seagate

Be extremely brief. Just the number or company name."""

def get_company_data_summary(df):
    lines = ["=== FINANCIAL DATA ===\n"]
    for company in df['Company'].unique():
        data = df[df['Company'] == company]
        lines.append(f"【{company}】")
        for _, row in data.iterrows():
            year = int(row['Year'])
            revenue = row['Total Revenue']
            net_income = row['Net Income']
            assets = row['Total Assets']
            liabilities = row['Total Liabilities']
            cash_flow = row['Operating Cash Flow']
            lines.append(f"  {year}: Revenue {revenue}M, Net Income {net_income}M, Assets {assets}M, Liabilities {liabilities}M, Cash Flow {cash_flow}M")
        lines.append("")
    return "\n".join(lines)

def run_agent(query, df, history=None, mode="normal"):
    """Run the Agent with LLM"""
    if df is None or df.empty:
        return "No data. Please upload a CSV or Excel file first."

    data_summary = get_company_data_summary(df)

    # 根据模式选择 Prompt
    system_prompt = SYSTEM_PROMPT_SHORT if mode == "short" else SYSTEM_PROMPT_NORMAL
    max_tokens = 256 if mode == "short" else 1024

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{data_summary}\n\nUser question: {query}"}
    ]

    if history and len(history) > 0:
        recent = history[-6:]
        for msg in recent:
            messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.1,
            max_tokens=max_tokens
        )

        answer = response.choices[0].message.content
        usage = response.usage

        log_usage(
            question=query,
            answer=answer,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens
        )

        return answer
    except Exception as e:
        return f"Error: {str(e)}"

def quick_answer(company, df):
    if df is None or df.empty:
        return "No data. Please upload a CSV file first."

    data = df[df['Company'] == company]
    if data.empty:
        return f"No data found for {company}"

    latest = data.iloc[-1]
    revenue = latest['Total Revenue']
    net_income = latest['Net Income']
    net_margin = (net_income / revenue) * 100 if revenue != 0 else 0
    debt_ratio = (latest['Total Liabilities'] / latest['Total Assets']) * 100 if latest['Total Assets'] != 0 else 0

    answer = f"""{company} {latest['Year']}:
  Revenue: ${revenue:,}M
  Net Income: ${net_income:,}M
  Net Margin: {net_margin:.1f}%
  Debt Ratio: {debt_ratio:.1f}%"""

    log_usage(
        question=f"[Quick] {company} latest data",
        answer=answer,
        prompt_tokens=0,
        completion_tokens=0,
        total_tokens=0
    )

    return answer