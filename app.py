import streamlit as st

st.set_page_config(
    page_title="Financial Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== Initialize session state =====
if "df" not in st.session_state:
    st.session_state.df = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ===== Navigation (Guide first = homepage) =====
guide = st.Page(
    "pages/guide.py",
    title="Home",
    icon="🏠",
    default=True,  # 设为默认页面
)

chat = st.Page(
    "pages/chat.py",
    title="Chat",
    icon="💬",
)

data = st.Page(
    "pages/data.py",
    title="Data",
    icon="📋",
)

pg = st.navigation(
    {
        "": [guide, chat, data]
    }
)


pg.run()