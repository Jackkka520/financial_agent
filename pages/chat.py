import streamlit as st
import pandas as pd
from datetime import datetime

from data_loader import load_csv_data
from agent import run_agent
from quick_replies import quick_reply
from logger import print_usage

# ===== Session State =====
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

if "uploaded_file_key" not in st.session_state:
    st.session_state.uploaded_file_key = None

if "mode" not in st.session_state:
    st.session_state.mode = "Normal"

st.title("💬 Financial Agent Chatbot")
st.caption("Ask about revenue, profit, growth, debt, or compare companies")

# ===== Upload + Sample + Download =====
col1, col2, col3 = st.columns([3, 0.8, 0.8])

with col1:
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
        key="chat_uploader",
    )

with col2:
    if st.button("📊 Sample", use_container_width=True):
        st.session_state.df = load_csv_data("financial_data.csv")
        st.session_state.messages = []
        st.session_state.page = "Chat"
        st.session_state.uploaded_file_key = None
        st.success("✅ Sample loaded")
        st.rerun()

with col3:
    if st.button("📥 Export chat", use_container_width=True):
        if st.session_state.messages:
            export_text = f"Financial Data Analyst - Chat Export\n"
            export_text += f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            export_text += "=" * 50 + "\n\n"
            
            for msg in st.session_state.messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                export_text += f"[{role}]\n{msg['content']}\n\n"
            
            st.download_button(
                label="📥 Download",
                data=export_text,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="download_chat"
            )
        else:
            st.warning("⚠️ No messages to export")

# ===== Upload =====
if uploaded_file is not None:
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"
    
    if file_key != st.session_state.uploaded_file_key:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state.df = df
            st.session_state.messages = []
            st.session_state.page = "Chat"
            st.session_state.uploaded_file_key = file_key

            st.success(f"✅ Loaded: {uploaded_file.name} ({len(df)} rows)")
            print_usage()
            st.rerun()

        except Exception as e:
            st.error(f"❌ Failed: {e}")

# ===== No Data =====
if st.session_state.df is None:
    st.warning("⚠️ No data. Upload a file or click Sample.")
    st.stop()

st.divider()

# ===== History =====
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===== Quick Questions =====
st.markdown("**⚡ Quick Questions**")

cols = st.columns(3)

questions = [
    ("🤖 What can you do?", "What can you do?"),
    ("🛡️ Recommend (Conservative)", "Recommend a conservative stock from the data"),
    ("🚀 Recommend (High Growth)", "Recommend a high growth stock from the data"),
]

for i, (label, q) in enumerate(questions):
    with cols[i]:
        if st.button(label, use_container_width=True):
            st.session_state.query = q
            st.rerun()

# ===== Chat Input with Mode Dropdown (左边) =====
st.markdown("---")

mode_col, input_col = st.columns([1, 5])

with mode_col:
    mode = st.selectbox(
        "Mode",
        options=["Normal", "Short"],
        index=0 if st.session_state.get("mode") == "Normal" else 1,
        label_visibility="collapsed"
    )
    st.session_state.mode = mode

with input_col:
    query = st.chat_input(
        "Ask about revenue, profit, growth, debt, or compare..."
    )

# ===== Process Query =====
if st.session_state.get("query"):
    query = st.session_state.pop("query")

if query:
    df = st.session_state.df

    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = quick_reply(query, df)

            if response is None:
                mode_lower = st.session_state.get("mode", "normal").lower()
                response = run_agent(
                    query,
                    df,
                    st.session_state.messages,
                    mode=mode_lower
                )

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    print_usage()
    st.rerun()
    
