# 🛍️ Amazon India Fashion Sales Analytics

> End-to-end data analytics project on 1,20,378 Amazon India fashion orders — from raw CSV to MySQL database, Python ML model, and a 4-page Power BI dashboard.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)
![XGBoost](https://img.shields.io/badge/XGBoost-95%25%20Accuracy-green)
![SHAP](https://img.shields.io/badge/SHAP-Explainability-purple)

---

## 📌 Project Overview

This project analyzes real Amazon India fashion sales data (Apr–Jun 2022) to uncover business insights, identify cancellation patterns, and predict which orders are likely to be cancelled using machine learning.

**Business Problem:** 14.28% of all orders are cancelled — costing the brand an estimated ₹1.1 crore in lost revenue. This project identifies *why* cancellations happen and *which* orders are at risk.

---

## 🎯 Key Findings

- 📦 **1,20,378 total orders** processed across April–June 2022
- 💰 **₹6.7 Crore** total revenue generated
- ❌ **14.28% cancellation rate** — 17,185 orders cancelled
- 🏆 **Set (50%)** and **Kurta (27%)** dominate category revenue
- 📍 **Maharashtra** is the #1 state by both revenue and cancellations
- 🚚 **Amazon fulfilment** has lower cancellation rate than Merchant
- 🤖 **Order Quantity (qty)** is the #1 driver of cancellations per SHAP analysis

---

## 🏗️ Project Architecture

```
Raw CSV Data
     ↓
MySQL Database (4 tables, 15 SQL queries)
     ↓
Python — EDA + Cleaning + Feature Engineering
     ↓
XGBoost ML Model (95% accuracy, AUC 0.96)
     ↓
SHAP Explainability Analysis
     ↓
Predictions written back to MySQL
     ↓
Power BI Dashboard (4 pages, live SQL connection)
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Database | MySQL 8.0, MySQL Workbench |
| Language | Python 3.11 |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn, XGBoost |
| Explainability | SHAP |
| Dashboard | Power BI Desktop |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```
amazon-india-sales-analytics/
│
├── data/
│   ├── Amazon Sale Report.csv
│   ├── Sale Report.csv
│   ├── May-2022.csv
│   └── International sale Report.csv
│
├── sql/
│   └── MySQL_Complete_Guide.sql
│
├── notebooks/
│   └── EDA_Analysis.py
│
├── charts/
│   ├── chart1_monthly_revenue.png
│   ├── chart2_category_revenue.png
│   ├── chart3_cancellation_by_category.png
│   ├── chart4_state_revenue.png
│   ├── chart5_fulfilment_comparison.png
│   ├── chart6_b2b_vs_b2c.png
│   ├── chart7_correlation_heatmap.png
│   ├── chart8_feature_importance.png
│   └── chart9_shap_summary.png
│
├── models/
│   └── cancellation_model.pkl
│
├── dashboard/
│   └── Amazon_Fashion_Dashboard.pbix
│
└── README.md
```

---

## 📊 Dashboard Pages

### Page 1 — Executive Overview
- Total Revenue, Cancellations, Returns, Avg Order Value KPIs
- Monthly Revenue Trend (Mar–Jun 2022)
- Revenue by Category
- Amazon vs Merchant Fulfilment Split

### Page 2 — Sales Analysis
- Revenue by State (Top 10)
- Category Revenue Split (pie chart)
- Units Sold by Size

### Page 3 — Cancellation Analysis
- Cancellations by Category
- Amazon vs Merchant Cancellation comparison
- Cancellations by State (Top 10)

### Page 4 — ML Predictions
- XGBoost model results (95% accuracy, AUC 0.96)
- SHAP explainability chart
- Feature importance chart
- Avg cancellation risk score + predicted high risk orders

---

## 🤖 ML Model Results

| Metric | Score |
|---|---|
| Accuracy | 95% |
| AUC-ROC | 0.96 |
| Precision | 0.96 |
| Recall | 0.95 |
| Model | XGBoost Classifier |

**Top cancellation drivers (SHAP):**
1. Order Quantity (qty) — strongest predictor
2. Service Level (Standard vs Expedited)
3. Fulfilment method (Amazon vs Merchant)

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/amazon-india-sales-analytics.git
cd amazon-india-sales-analytics
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn xgboost shap sqlalchemy pymysql joblib
```

### 3. Set up MySQL
- Open MySQL Workbench
- Run `sql/MySQL_Complete_Guide.sql`
- This creates the database and all 4 tables

### 4. Import data
```bash
python import_data.py
```
Update the MySQL password in the script before running.

### 5. Run EDA + ML
```bash
python EDA_Analysis.py
```
This generates all 9 charts and trains the XGBoost model.

### 6. Open Power BI Dashboard
- Open `dashboard/Amazon_Fashion_Dashboard.pbix`
- Or connect Power BI to the CSV files in the data folder

---

## 📈 Business Insights

1. **Revenue declined** from ₹245L (April) to ₹200L (June) — seasonality pattern
2. **Set category** alone drives 50% of total revenue
3. **Maharashtra + Karnataka** = 30% of all India revenue
4. **Amazon fulfilment** has 13% cancellation rate vs Merchant's 17%
5. **B2B orders** have 12% higher average order value (₹681 vs ₹609)
6. **M, L, XL sizes** account for 60%+ of all units sold

---

## 👩‍💻 Author

**Srishti**
- Final Year Student — Data Analytics
- 📧 Connect on [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)
- 🐙 [GitHub](https://github.com/YOUR_USERNAME)

---

## ⭐ If you found this project useful, please give it a star!
