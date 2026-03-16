# AI-Powered Project Management Dashboard

> **Roles targeted:** Junior Project Manager | Data Analyst | Business Analyst

[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## Business Problem

Project managers often rely on gut feel and outdated spreadsheets to track status, forecast budgets, and spot risks. This dashboard replaces that with real-time, AI-driven insights — giving PMs and stakeholders a single source of truth.

---

## What I Built

A Python-based intelligent PM dashboard that combines data analytics, business intelligence, and machine learning to support smarter project delivery decisions.

| Feature | Description |
|---|---|
| Real-Time KPI Tracking | Live project health metrics: schedule, budget, scope, quality |
| Predictive Budget Forecasting | ML model predicts budget overruns before they happen |
| Risk Intelligence | Automated risk scoring and early-warning alerts |
| Resource Optimization | Identifies team bottlenecks and allocation gaps |
| Timeline Analysis | Planned vs actual progress with milestone tracking |
| Stakeholder Reporting | Auto-generated status reports and executive summaries |

---

## Key Outcomes & Business Impact

- Automated risk detection identifies project issues **2-3 weeks earlier** than manual review
- Budget forecasting model achieves **~85% accuracy** on holdout project data
- Resource optimization reduces idle time and bottlenecks by an estimated **20%**
- Stakeholder report generation cuts reporting time from hours to **minutes**
- KPI dashboard replaces 5+ manual spreadsheets with a single automated view

---

## Tech Stack

| Category | Tools |
|---|---|
| Programming | Python 3.8+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn (forecasting, risk scoring) |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit / Flask |
| Data Storage | SQLite, CSV |

---

## Project Structure

```
ai-project-management-dashboard/
├── src/
│   ├── data_processing/        # ETL and data preparation modules
│   ├── models/                 # ML forecasting and risk models
│   ├── dashboard/              # UI components and layout
│   └── reports/                # Report generation utilities
├── data/                       # Sample project datasets
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/ChidghanaH/ai-project-management-dashboard.git
cd ai-project-management-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
python src/dashboard/app.py
```

---

## Skills Demonstrated

- Project management domain knowledge: KPIs, risk registers, resource planning, milestone tracking
- Machine learning for forecasting and classification (budget overrun, risk scoring)
- Business intelligence dashboard design and stakeholder reporting
- Translating PM workflows into automated, data-driven systems
- Python software design: modular architecture, clean separation of concerns

---

## Author

**Chidghana Hemantharaju** — MSc Business Analytics | Munich, Germany

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/chidghana-hemantharaju/)
