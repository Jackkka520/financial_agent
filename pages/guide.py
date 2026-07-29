import streamlit as st

st.title("📊 Financial Data Analyst")
st.caption("AI-powered financial data analysis tool")

# ===== Quick Start =====
st.markdown("""
## 🚀 Quick Start

1. **Load Data** → Upload CSV/Excel or click **Sample** in Chat page
2. **Ask Questions** → Introduce itself, stock recommendations (risk or safe)
3. **Explore** → View data tables and interactive charts in Data page

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **💬 Chat** | Ask financial questions, get instant answers with AI |
| **📊 Data** | View data tables, filter by company, interactive charts |
| **⚡ Quick Questions** | One-click common queries (Revenue, Profit, Growth, Recommend) |
| **📝 Normal / Short Mode** | Toggle between detailed analysis and concise answers |
| **📥 Export** | Download chat history as text file |

---

## 💬 Chat Page Guide

| What | How |
|------|-----|
| **Ask a question** | Type in the chat input at the bottom |
| **Quick question** | Click one of the Quick Question buttons |
| **Load sample data** | Click **Sample** button |
| **Upload your data** | Use the file uploader |
| **Export chat** | Click **Download** button |
| **Switch response mode** | Use the dropdown next to chat input |

**Example questions:**
- "What is the revenue of the first company?"
- "Recommend a conservative stock"
- "Calculate revenue growth for Micron"

---

## 📊 Data Page Guide

| What | How |
|------|-----|
| **View data** | Upload a file or load sample data |
| **Filter by company** | Use the dropdown to select a specific company |
| **See charts** | Scroll down below the table |
| **Understand metrics** | Charts show Revenue, Net Margin, Debt Ratio |

**Charts available:**
- Revenue trend (line chart)
- Net margin (bar chart)
- Debt ratio (bar chart)

---

## 📁 Data Format

Required columns: `Company`, `Year`, `Total Revenue`, `Net Income`, `Total Assets`, `Total Liabilities`, `Operating Cash Flow`

> 💡 Sample data is built-in — click **Sample** to try it.

---

## 🤖 AI Model & Limitations

| Aspect | Description |
|--------|-------------|
| **Model** | GLM-4-Flash (智谱 AI) |
| **Context Window** | 128K tokens |
| **Data Source** | Only uses data from uploaded CSV/Excel |
| **No Real-time Data** | Does not fetch live market data |
| **No External Knowledge** | Only analyzes data you provide |

**Important Notes:**
- The AI **does not have access to real-time stock prices** or market data
- All analysis is based **only on the data you upload**
- Recommendations are **for educational purposes only**, not financial advice
- Always **verify critical numbers** against original source documents

---

## ⚠️ Disclaimer

This tool is designed for **educational and demonstration purposes only**.

- **Not financial advice** — Do not make investment decisions based solely on this tool
- **Data accuracy** — The AI may make errors; always cross-check with original data
- **Privacy** — Your data is processed locally; no data is sent to external servers
- **Use at your own risk** — The creators assume no liability for any decisions made using this tool

""")

