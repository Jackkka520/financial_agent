import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_csv_data
from logger import print_usage

# ===== Session State =====
if "df" not in st.session_state:
    st.session_state.df = None

if "uploaded_file_key" not in st.session_state:
    st.session_state.uploaded_file_key = None

st.title("📋 Data Viewer")
st.caption("View and explore your financial data")

# ===== Upload + Sample =====
col1, col2 = st.columns([3, 0.8])

with col1:
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
        key="data_uploader",
    )

with col2:
    if st.button("📊 Sample", use_container_width=True):
        df = load_csv_data("financial_data.csv")
        if df is not None:
            st.session_state.df = df
            st.session_state.uploaded_file_key = None
            st.success("✅ Sample loaded")
            st.rerun()
        else:
            st.error("❌ Sample data not found")

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
            st.session_state.uploaded_file_key = file_key

            st.success(f"✅ Loaded: {uploaded_file.name} ({len(df)} rows, {len(df.columns)} columns)")
            print_usage()
            st.rerun()

        except Exception as e:
            st.error(f"❌ Failed to load: {e}")

# ===== No Data =====
if st.session_state.df is None:
    st.info("📂 Upload a file or click 'Sample' to start")
    st.stop()

df = st.session_state.df

st.divider()

# ===== Dropdown: Select Company =====
companies = ["All Companies"] + sorted(df["Company"].unique().tolist())
selected = st.selectbox("Select Company", companies)

if selected == "All Companies":
    display_df = df
else:
    display_df = df[df["Company"] == selected]

st.caption(f"Showing {len(display_df)} rows")

# ===== Data Table =====
st.subheader("📊 Data Preview")
st.dataframe(
    display_df,
    use_container_width=True,
    height=400,
)

st.divider()

# ===== Charts =====
st.subheader("📈 Financial Charts")

# 计算派生指标
plot_df = display_df.copy()
plot_df["Net Margin (%)"] = (plot_df["Net Income"] / plot_df["Total Revenue"]) * 100
plot_df["Debt Ratio (%)"] = (plot_df["Total Liabilities"] / plot_df["Total Assets"]) * 100

# Chart 1: Revenue Trend
if len(display_df) > 0:
    fig1 = px.line(
        plot_df,
        x="Year",
        y="Total Revenue",
        color="Company" if selected == "All Companies" else None,
        markers=True,
        title="Revenue by Company" if selected == "All Companies" else f"{selected} Revenue Trend",
        labels={"Total Revenue": "Revenue (USD M)", "Year": "Fiscal Year"}
    )
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Net Margin & Debt Ratio
if len(display_df) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        fig2 = px.bar(
            plot_df,
            x="Year",
            y="Net Margin (%)",
            color="Company" if selected == "All Companies" else None,
            title="Net Margin (%)" if selected == "All Companies" else f"{selected} Net Margin (%)",
            labels={"Net Margin (%)": "Net Margin (%)", "Year": "Fiscal Year"}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        fig3 = px.bar(
            plot_df,
            x="Year",
            y="Debt Ratio (%)",
            color="Company" if selected == "All Companies" else None,
            title="Debt Ratio (%)" if selected == "All Companies" else f"{selected} Debt Ratio (%)",
            labels={"Debt Ratio (%)": "Debt Ratio (%)", "Year": "Fiscal Year"}
        )
        st.plotly_chart(fig3, use_container_width=True)

# Chart 3: Revenue vs Net Income (Scatter)
if len(display_df) > 1 and selected != "All Companies":
    fig4 = px.scatter(
        plot_df,
        x="Total Revenue",
        y="Net Income",
        text="Year",
        title=f"{selected}: Revenue vs Net Income",
        labels={"Total Revenue": "Revenue (USD M)", "Net Income": "Net Income (USD M)"}
    )
    fig4.update_traces(textposition="top center")
    st.plotly_chart(fig4, use_container_width=True)