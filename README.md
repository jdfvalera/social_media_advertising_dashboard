# Marketing Campaign Dashboard (Streamlit)

This repository contains a small, self-contained analytics dashboard built using a **public Kaggle dataset**.  
The purpose of this project is to illustrate my general approach to **data storytelling, insight generation, and decision-focused visualization**.

All data is public and synthetic.

---

## What This Demonstrates

- How I structure dashboards around decision-making
- How I surface trade-offs (scale vs efficiency)
- How I reduce noise rather than maximize metrics
- How I design for executive consumption

---

## Dataset

Source: Kaggle  
The dataset represents synthetic social media advertising performance across channels, audiences, and campaigns.

It is used here purely for demonstration.

---

## Pages Included

### Executive Overview
High-level KPIs and trends intended for leadership:
- Total impressions and clicks
- Average ROI and conversion rate
- Performance trends over time
- ROI comparison by channel

### Channel Performance
Focused comparison of channels:
- CTR, CPC, ROI, and cost per conversion
- Designed to support budget allocation discussions

### Audience Insights
Segment-level analysis:
- Conversion rate by audience
- Engagement by customer segment
- Geographic performance

### Campaign Deep Dive
Campaign-level metrics and trends:
- Campaign comparison table
- Click trends over time

---

## Setup Instructions

### 1. Install Python
Download Python 3.10+ from:
https://www.python.org/downloads/

Ensure **“Add Python to PATH”** is checked during installation.

Verify:
```bash
python --version
```

---

### 2. Install Dependencies
From the project directory:
```bash
pip install -r requirements.txt
```

---

### 3. Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open automatically in your browser.

---

## Updating or Replacing the Data

To update or extend the dashboard:
- Edit `data/Social_Media_Advertising.csv`
- Append new rows or replace the file entirely
- Keep column names consistent

No code changes are required.

---

## Calculated Metrics

The following metrics are calculated automatically in the app:
- **CTR** = Clicks / Impressions
- **Estimated Conversions** = Clicks × Conversion Rate
- **CPC** = Acquisition Cost / Clicks
- **Cost per Conversion** = Acquisition Cost / Estimated Conversions

---

## Notes

This project is intentionally lightweight and opinionated.
It reflects how I typically explore data, frame insights, and communicate results to stakeholders.