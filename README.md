<div align="center">

# 🌊 **Flood Risk Assistant — Bangladesh**

## A Gen AI-powered agent that answers "is my district at flood risk?" in Bengali, grounded in real river-discharge data

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white)
![Status](https://img.shields.io/badge/Status-Phase_1_Data_Layer-orange?style=for-the-badge)

</div>

---

## 🎓 Project Info

###**Submission for:** Google Cloud Gen AI Academy APAC Edition (Cohort 3) — Meet the Builders

**Built by:** **Farjana Ferdausi**

---

## 🌍 Overview

Bangladesh is one of the most flood-exposed countries in the world, and flood-risk
information often doesn't reach rural communities in a language or format they can
act on. This project pulls real river-discharge data for flood-prone Bangladeshi
districts and — in the next phase — wraps it in a conversational Gemini agent that
answers flood-risk questions in plain Bengali.

**Data source:** [Open-Meteo Flood API](https://open-meteo.com/en/docs/flood-api) —
free, no API key required, powered by the Global Flood Awareness System (GloFAS).
Provides simulated river discharge (m³/s) at ~5 km resolution from 1984 to a
7-month forecast.

## 🚧 Project Status

- ✅ **Phase 1 — Data layer:** fetch + load river discharge data into
  BigQuery for 10 flood-prone districts
- ✅ **Phase 2 — Agent layer:** ADK + Gemini agent that queries BigQuery,
  applies a district-relative flood-risk classification, and answers in
  conversational Bengali
- ⬜ **Phase 3 — Deployment:** Cloud Run
- ⬜ **Phase 4 — Documentation:** Medium blog + LinkedIn post + demo video

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Flood data | Open-Meteo Flood API (GloFAS) | Daily river discharge per district |
| Processing | Pandas | Reshape API response into tabular rows |
| Storage | Google BigQuery | Partitioned, queryable flood-risk dataset, window-function risk scoring |
| Agent | Google ADK + Gemini 3.5 Flash | Bengali-language conversational flood-risk assistant |

## 📁 Project Structure

```
flood-risk-assistant/
├── data_ingestion/
│   ├── districts.py         # 10 flood-prone Bangladeshi districts (lat/lon)
│   ├── fetch_flood_data.py  # Pulls river discharge from Open-Meteo
│   └── load_to_bigquery.py  # Loads fetched data into BigQuery
├── app/
│   ├── tools.py             # BigQuery-backed tools (district-relative risk logic)
│   ├── agent.py             # ADK + Gemini agent definition
│   └── demo.py              # Local test harness (InMemoryRunner)
├── schema.sql               # BigQuery table DDL
├── requirements.txt
└── README.md
```

## 🧠 How Risk Is Judged

Flood risk is scored **relative to each district's own history**, not one
fixed number for the whole country — a river like the Jamuna naturally
carries far more water than a smaller one, so a single flat threshold would
misjudge both. A BigQuery window query computes each district's own trailing
365-day 75th/90th percentile discharge, and today's reading is compared
against *that same district's* baseline:

| Latest discharge vs. district's own baseline | Risk level |
|---|---|
| ≥ 90th percentile | High |
| ≥ 75th percentile | Elevated |
| below 75th percentile | Normal |

## 🤖 Trying the Agent

```bash
cd app
python demo.py YOUR_GCP_PROJECT_ID
```

Asks the agent a few sample Bengali questions and prints its answers,
including tool calls to BigQuery, using ADK's `InMemoryRunner`.

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Try the fetch step on its own (no GCP needed yet)

```bash
cd data_ingestion
python fetch_flood_data.py
```

This prints a preview and saves `flood_discharge_raw.csv` — a good sanity check
before touching BigQuery.

### 3. Set up BigQuery

```bash
gcloud auth application-default login
bq mk --dataset YOUR_PROJECT_ID:flood_risk
bq query --use_legacy_sql=false < ../schema.sql
```

### 4. Fetch + load in one step

```bash
python load_to_bigquery.py --project YOUR_PROJECT_ID
```

## 🗺️ Districts Covered

Dhaka, Sirajganj, Bogura, Kurigram, Gaibandha, Rangpur, Jamalpur, Faridpur,
Sylhet, Chattogram — selected for known exposure along the Jamuna/Brahmaputra,
Padma, and Surma river systems. Add more in `data_ingestion/districts.py`.

## ⚠️ Scope Note

This tool surfaces river-discharge data from a public, non-commercial hydrological
model (GloFAS) — it is a decision-support aid, not an official flood warning. For
official alerts, always defer to Bangladesh's Flood Forecasting and Warning Centre
(FFWC) and local authorities.

## 🖊️ Author

**Farjana Ferdausi**

AI/ML Engineering & Data Science, Fellow — Google Cloud Gen AI Academy APAC Edition (Cohort 3) | Agentic AI · RAG · Gemini · ADK · BigQuery MCP · Cloud Run | Former HR Professional (14+ years) at Radisson Blu Dhaka Water Garden, Bangladesh

LinkedIn Profile: https://www.linkedin.com/in/farjana-ferdausi/

Medium Blog Link:

Medium Profile: https://medium.com/@farjana.rafi1983

---
<div align="center">Built with Open-Meteo · BigQuery · Gemini · Google ADK</div>
