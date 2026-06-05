# RetailPulse — Customer Analytics & Churn Intelligence

End-to-end analytics on a real e-commerce dataset that answers three business questions:
**Why do customers leave? Where does revenue come from? Which marketing efforts actually pay off?**

Built with **SQL + Python**, with a live **Streamlit dashboard** on top.

![status](https://img.shields.io/badge/status-portfolio%20project-blue) ![python](https://img.shields.io/badge/python-3.9+-green) ![license](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Why this project

Most analyst portfolios stop at a few charts. RetailPulse goes the full distance — raw data → SQL cleaning → analysis notebooks → predictive model → interactive dashboard — so it reads like real product-analyst work, not a homework assignment.

## The data

[**Online Retail II**](https://archive.ics.uci.edu/dataset/502/online+retail+ii) (UCI Machine Learning Repository) — ~1M transactions from a UK online retailer (2009–2011), including invoice numbers, products, quantities, prices, dates, and customer IDs.

Place `online_retail_II.xlsx` in `data/raw/` (download it from the link above).

## What's inside

| Pillar | Question | Techniques |
|---|---|---|
| **Retention & Churn** | Why and when do customers stop buying? | Cohort retention (monthly), RFM segmentation, churn model (XGBoost / Logistic Regression) |
| **Sales & Revenue** | Where does revenue come from and where is it heading? | Revenue trends, top products/countries, MoM growth, time-series forecast (Prophet) |
| **Marketing / Acquisition** | Which customers and channels are worth the spend? | CAC vs. LTV, customer value tiers, A/B-test analysis |

## Repository structure

```
retailpulse/
├── data/raw/            # place online_retail_II.xlsx here (gitignored)
├── sql/                 # cleaning & KPI queries (4 files)
├── notebooks/           # 01_eda, 02_churn_retention, 03_sales_revenue, 04_marketing_ltv
├── src/                 # download_data, data_prep, features
├── dashboard/app.py     # Streamlit app
├── reports/figures/     # exported charts
├── requirements.txt
└── README.md
```

## Quickstart

```bash
git clone https://github.com/<your-username>/retailpulse.git
cd retailpulse
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# place online_retail_II.xlsx in data/raw/
jupyter lab                        # run notebooks 01 → 04
streamlit run dashboard/app.py     # launch the dashboard
```

> macOS note: if XGBoost fails to load, run `brew install libomp`.

## Key findings

Analysis of **805,549 transactions** from **5,878 customers** (~**£17.7M** total revenue, 2009–2011):

- **Revenue concentration:** the top **20% of customers drive 77% of revenue** — a textbook Pareto distribution that argues for prioritizing retention of high-value accounts.
- **Churn model:** a behaviour-based classifier (frequency + monetary) predicts 90-day churn, deliberately excluding recency-derived features to avoid target leakage and keep the AUC defensible.
- **Markets & products:** the **United Kingdom** dominates revenue; top sellers include the *Regency Cakestand 3 Tier* and *White Hanging Heart T-Light Holder*.
- **Marketing:** RFM segmentation splits customers into Champions, Loyal, At Risk, and others; the **Champions** segment shows by far the strongest CAC:LTV ratio.
- **Retention email A/B test (simulated):** variant lifted repurchase ~2.5 points (11.0% → 13.5%), illustrating the test-and-measure workflow.

## Sample dashboard

![dashboard](reports/figures/dashboard_preview.png)

## Resume bullets

- Built an **end-to-end customer-analytics pipeline** on **805K+ transactions** using **SQL and Python**, analysing cohort retention and surfacing that the **top 20% of customers drive 77% of revenue**.
- Developed a **churn-prediction model (XGBoost / Logistic Regression)** with **RFM segmentation** to flag at-risk customers and prioritize retention outreach, engineering features carefully to avoid target leakage.
- Built an interactive **Streamlit dashboard** with revenue, retention, and segment views, plus a simulated **A/B test** quantifying a retention-email lift — communicating insights to non-technical stakeholders.

## Tech stack

`Python` · `pandas` · `scikit-learn` · `XGBoost` · `SQL (DuckDB/PostgreSQL)` · `matplotlib` / `seaborn` · `Streamlit`

## License

MIT — see [LICENSE](LICENSE).
