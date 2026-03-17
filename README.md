# JETA Africa Holding — Business Intelligence Dashboard

Interactive dashboard for exploring lead data across JETA's African business verticals.

🔗 **Live:** [jeta-africa-dashboard.streamlit.app](https://jeta-africa-dashboard.streamlit.app)

## Data

| Vertical | Companies | High Potential | With Email |
|----------|-----------|---------------|------------|
| Pharma   | 37        | 24            | 29         |
| Fintech  | 36        | 21            | 17         |

Covering **17 countries** across Africa.

## Features

- **Overview** — Key metrics, country distribution, priority markets
- **Pharma / Fintech** — Filterable tables, Top 10 cards, analytics charts
- **Company Explorer** — Detailed view per company
- **Export Data** — Download as CSV / Excel

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech Stack

Streamlit · Pandas · Plotly · OpenPyXL
