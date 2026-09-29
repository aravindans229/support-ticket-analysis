"""
Generates a synthetic ITSM-style support ticket dataset:
ticket category, priority, created/resolved timestamps, SLA target, and
whether the SLA was breached. Modeled on typical ITSM/ITIL ticketing data
(similar to what ServiceNow / Freshservice / Jira Service Management export).
"""
import numpy as np
import pandas as pd

np.random.seed(7)

N = 2500

categories = ["Network", "Hardware", "Software", "Access Management", "Email", "Application Support"]
priorities = ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"]
priority_p = [0.05, 0.20, 0.45, 0.30]

# SLA target hours by priority (typical ITIL-style targets)
sla_targets = {
    "P1 - Critical": 4,
    "P2 - High": 8,
    "P3 - Medium": 24,
    "P4 - Low": 48,
}

channels = ["Phone", "Email", "Portal", "Chat"]

dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")

rows = []
for i in range(N):
    created = pd.Timestamp(np.random.choice(dates)) + pd.Timedelta(
        hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))
    category = np.random.choice(categories, p=[0.22, 0.18, 0.25, 0.15, 0.10, 0.10])
    priority = np.random.choice(priorities, p=priority_p)
    channel = np.random.choice(channels, p=[0.35, 0.25, 0.30, 0.10])
    sla_target = sla_targets[priority]

    # Resolution time: mostly within SLA, but with realistic overruns
    # Some categories (Network, Application Support) run slower on average
    slowness_factor = {"Network": 1.4, "Application Support": 1.3, "Hardware": 1.1,
                        "Software": 1.0, "Access Management": 0.6, "Email": 0.7}[category]
    base_hours = np.random.exponential(scale=sla_target * 0.55) * slowness_factor
    resolution_hours = round(max(0.25, base_hours), 2)

    resolved = created + pd.Timedelta(hours=resolution_hours)
    breached = resolution_hours > sla_target

    csat = np.random.choice([1, 2, 3, 4, 5],
                             p=[0.03, 0.07, 0.15, 0.35, 0.40] if not breached
                             else [0.15, 0.25, 0.30, 0.20, 0.10])

    rows.append({
        "Ticket_ID": f"TCK-{10000+i}",
        "Created_Date": created.isoformat(sep=" "),
        "Resolved_Date": resolved.isoformat(sep=" "),
        "Category": category,
        "Priority": priority,
        "Channel": channel,
        "SLA_Target_Hours": sla_target,
        "Resolution_Hours": resolution_hours,
        "SLA_Breached": breached,
        "CSAT_Score": csat,
    })

df = pd.DataFrame(rows)

# realistic messiness
dupe_rows = df.sample(10, random_state=3)
df = pd.concat([df, dupe_rows], ignore_index=True)
null_idx = df.sample(12, random_state=4).index
df.loc[null_idx, "CSAT_Score"] = None

df.to_csv("data/support_tickets.csv", index=False)
print(f"Generated {len(df)} rows -> data/support_tickets.csv")
