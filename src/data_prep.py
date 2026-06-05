"""Cleaning helpers for the Online Retail II dataset."""
from __future__ import annotations
import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize columns and drop invalid rows.

    Returns a tidy frame with: invoice, stock_code, description, quantity,
    invoice_date, price, customer_id, country, revenue.
    """
    df = df.rename(columns={
        "Invoice": "invoice", "StockCode": "stock_code",
        "Description": "description", "Quantity": "quantity",
        "InvoiceDate": "invoice_date", "Price": "price",
        "Customer ID": "customer_id", "Country": "country",
    })

    df = df.dropna(subset=["customer_id"]).copy()
    df["customer_id"] = df["customer_id"].astype(int)
    df["invoice"] = df["invoice"].astype(str)
    df["description"] = df["description"].str.strip()
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    # drop returns / cancellations / non-positive lines
    df = df[(df["quantity"] > 0) & (df["price"] > 0)]
    df = df[~df["invoice"].str.startswith("C")]

    df["revenue"] = df["quantity"] * df["price"]
    return df.reset_index(drop=True)


def summarize(df: pd.DataFrame) -> dict:
    """Quick data-quality snapshot."""
    return {
        "rows": len(df),
        "customers": df["customer_id"].nunique(),
        "invoices": df["invoice"].nunique(),
        "first_order": df["invoice_date"].min(),
        "last_order": df["invoice_date"].max(),
        "total_revenue": round(df["revenue"].sum(), 2),
    }
