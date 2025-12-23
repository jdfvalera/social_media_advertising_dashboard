# Marketing Campaign Dashboard (Streamlit)

This repository contains an interactive analytics dashboard built using a **public Kaggle dataset**.
The purpose of this project is to demonstrate my general approach to **data exploration, data storytelling, and decision-oriented visualization**, rather than domain expertise in marketing.

All data used is public and synthetic.

---

## What This Project Demonstrates

- How I structure dashboards around decisions rather than metric exhaust
- How I balance analytical depth with visual clarity
- How I surface trade-offs such as scale vs. efficiency and engagement vs. conversion
- How I design dashboards intended for executive and stakeholder consumption

The dashboard is designed to be largely self-serve, with the expectation that the visuals themselves carry the primary signal.

---

## Dataset

**Source:** Kaggle  
The dataset represents synthetic social media advertising performance across companies, channels, audiences, and campaigns.

It is used purely for demonstration purposes and has been lightly cleaned and augmented with derived metrics.

---

## Dashboard Structure

### Executive Overview
A high-level view intended to support fast orientation:
- Total spend, impressions, clicks, ROI, and cost per conversion
- Ranked channel performance by ROI
- Scale vs. efficiency comparisons across channels
- Campaign goal contribution to overall volume

This view is designed to support high-level performance assessment and prioritization discussions.

---

### Audience & Engagement
Focused on audience behavior and response quality:
- Engagement vs. conversion comparisons by audience
- Conversion rate by customer segment
- CTR by language

This view supports questions around targeting, messaging alignment, and audience quality.

---

### Efficiency & Risk
Designed to surface underperformance and potential inefficiencies:
- Lowest ROI campaigns by spend
- Relationship between campaign duration and cost efficiency

This view is intended to help identify candidates for optimization or deeper review.

---

### Campaign Deep Dive
Detailed, campaign-level exploration:
- Full performance table across campaigns
- Sorted by ROI to surface top and bottom performers
- Downloadable, filtered dataset (CSV) for offline analysis

This view supports follow-up analysis and deeper inspection.

---

## Calculated Metrics

The following metrics are calculated automatically in the application:
- **CTR** = Clicks / Impressions
- **Estimated Conversions** = Clicks × Conversion Rate
- **CPC** = Acquisition Cost / Clicks
- **Cost per Conversion** = Acquisition Cost / Estimated Conversions

---

## Setup Instructions

### 1. Install Python
Download Python **3.10 or newer** from:  
https://www.python.org/downloads/

Ensure **“Add Python to PATH”** is selected during installation.

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

To update the dashboard:
- Edit `data/Social_Media_Advertising.csv`
- Append new rows or replace the file entirely
- Keep column names consistent

No code changes are required.

---