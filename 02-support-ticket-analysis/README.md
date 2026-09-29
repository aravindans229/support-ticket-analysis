# IT Support Ticket / SLA Analysis (ITSM)

Analysis of a year of IT service desk tickets to find which categories and
channels breach SLA most, how ticket volume relates to breach rate over time,
and how SLA breaches affect customer satisfaction.

## Why This Project
This mirrors the kind of data produced by ITSM tools like ServiceNow,
Freshservice or Jira Service Management — the same kind of data I work with
day to day as a Technical Support Analyst, analyzed here with SQL and Pandas
instead of a built-in reporting dashboard.

## Problem
A service desk wants to know: which ticket categories and channels are most
likely to breach SLA, whether breaches actually hurt customer satisfaction,
and whether ticket volume spikes are driving those breaches.

## Dataset
`data/support_tickets.csv` — 2,510 tickets from 2024 with Category, Priority,
Channel, SLA target hours, resolution hours, SLA breach flag, and CSAT score.
(Synthetic data, generated with `generate_data.py`, modeled on typical
ITIL-style priority/SLA targets — P1: 4h, P2: 8h, P3: 24h, P4: 48h.)

## Approach
1. **Clean** — removed duplicate rows, imputed missing CSAT scores with the median.
2. **SQL (SQLite)** — SLA breach rate by category, average resolution time vs
   SLA target by priority, monthly ticket volume and breach rate (subquery),
   channel-level SLA performance (CTE).
3. **Pandas** — CSAT score by breach status, visualized with boxplots and bar
   charts; monthly volume vs breach rate trend.

## Key Findings
- Network and Application Support tickets breach SLA most often.
- Breached tickets score meaningfully lower on CSAT than tickets resolved on time.
- Ticket volume and breach rate rise together in certain months, suggesting
  under-staffing relative to demand during peaks.
- Some intake channels show a higher breach rate than others.

## Tools
Python · Pandas · SQLite (SQL) · Matplotlib · Seaborn

## Files
- `support_ticket_analysis.ipynb` — full analysis notebook
- `generate_data.py` — synthetic dataset generator
- `data/support_tickets.csv` — the dataset
- `charts/` — exported chart images

## How to Run
```bash
pip install pandas numpy matplotlib seaborn
jupyter notebook support_ticket_analysis.ipynb
```
