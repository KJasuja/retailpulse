"""RetailPulse dashboard.

Local:  reads data/raw/online_retail_II.xlsx if present.
Cloud:  falls back to the committed data/processed/transactions_sample.csv.

Run with: streamlit run dashboard/app.py
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))
from data_prep import clean_transactions  # noqa: E402
from features import build_rfm, cohort_matrix  # noqa: E402

st.set_page_config(page_title="RetailPulse", page_icon="📊", layout="wide")
st.title("📊 RetailPulse — Customer Analytics & Churn Intelligence")


@st.cache_data
def load_data() -> pd.DataFrame:
    xlsx = ROOT / "data" / "raw" / "online_retail_II.xlsx"
    csv = ROOT / "data" / "processed" / "transactions_sample.csv"
    if xlsx.exists():
        raw = pd.read_excel(xlsx, sheet_name=None)
        return clean_transactions(pd.concat(raw.values(), ignore_index=True))
    if csv.exists():
        df = pd.read_csv(csv, parse_dates=["invoice_date"])
        return df
    return pd.DataFrame()


df = load_data()
if df.empty:
    st.warning("No data found. Add data/raw/online_retail_II.xlsx locally, "
               "or commit data/processed/transactions_sample.csv for deployment.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"£{df['revenue'].sum():,.0f}")
c2.metric("Customers", f"{df['customer_id'].nunique():,}")
c3.metric("Orders", f"{df['invoice'].nunique():,}")
c4.metric("Avg order value", f"£{df['revenue'].sum()/df['invoice'].nunique():,.2f}")

tab1, tab2, tab3 = st.tabs(["Sales", "Retention", "Segments"])

with tab1:
    st.subheader("Monthly revenue")
    st.line_chart(df.set_index("invoice_date").resample("M")["revenue"].sum())
    st.subheader("Top 10 products")
    st.bar_chart(df.groupby("description")["revenue"].sum()
                   .sort_values(ascending=False).head(10))

with tab2:
    st.subheader("Cohort retention (%)")
    st.dataframe((cohort_matrix(df) * 100).round(0).fillna(""),
                 use_container_width=True)

with tab3:
    st.subheader("RFM segments")
    rfm = build_rfm(df)
    st.bar_chart(rfm["segment"].value_counts())
    st.dataframe(
        rfm.groupby("segment")[["recency_days", "frequency", "monetary"]].mean().round(1),
        use_container_width=True,
    )
