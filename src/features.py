"""Feature builders: RFM, cohorts, and churn labels."""
from __future__ import annotations
import pandas as pd


def build_rfm(df: pd.DataFrame, as_of: pd.Timestamp | None = None) -> pd.DataFrame:
    """Compute Recency / Frequency / Monetary + 1-5 scores and a segment label."""
    as_of = as_of or (df["invoice_date"].max() + pd.Timedelta(days=1))

    rfm = df.groupby("customer_id").agg(
        recency_days=("invoice_date", lambda s: (as_of - s.max()).days),
        frequency=("invoice", "nunique"),
        monetary=("revenue", "sum"),
    ).reset_index()

    rfm["r_score"] = pd.qcut(rfm["recency_days"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["rfm_total"] = rfm[["r_score", "f_score", "m_score"]].sum(axis=1)
    rfm["segment"] = rfm.apply(_segment, axis=1)
    return rfm


def _segment(row) -> str:
    if row.r_score >= 4 and row.f_score >= 4:
        return "Champions"
    if row.f_score >= 4:
        return "Loyal"
    if row.r_score >= 4:
        return "New / Promising"
    if row.r_score <= 2 and row.f_score <= 2:
        return "At Risk"
    return "Needs Attention"


def cohort_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Customer-count retention matrix indexed by cohort month vs. month offset."""
    d = df.copy()
    d["order_month"] = d["invoice_date"].dt.to_period("M")
    d["cohort"] = d.groupby("customer_id")["invoice_date"].transform("min").dt.to_period("M")
    d["offset"] = (d["order_month"] - d["cohort"]).apply(lambda x: x.n)

    counts = (d.groupby(["cohort", "offset"])["customer_id"]
                .nunique().reset_index())
    matrix = counts.pivot(index="cohort", columns="offset", values="customer_id")
    return matrix.div(matrix[0], axis=0)  # as retention %


def churn_labels(df: pd.DataFrame, inactive_days: int = 90) -> pd.DataFrame:
    """Label customers churned if no purchase in the last `inactive_days`.

    Returns a per-customer frame of features + a 0/1 `churned` target,
    ready to feed into a classifier.
    """
    rfm = build_rfm(df)
    rfm["churned"] = (rfm["recency_days"] > inactive_days).astype(int)
    return rfm[["customer_id", "recency_days", "frequency", "monetary",
                "r_score", "f_score", "m_score", "churned"]]
