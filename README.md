# Ethiopia Financial Inclusion Forecasting System

## Project Overview
This project is developed for **Selam Analytics**, a fintech consulting firm, in collaboration with the National Bank of Ethiopia and major mobile money operators (Telebirr, M-Pesa). 

Ethiopia is currently undergoing a rapid digital financial transformation. While mobile money users have surged to over 65 million, the **Global Findex 2024** report shows that account ownership has only grown by 3 percentage points (from 46% to 49%) since 2021. This project builds a forecasting system to understand the drivers behind this "Access Paradox" and predict trends for **2025-2027**.

## Objectives
- **Understand Drivers:** Identify what factors (policy, infrastructure, product launches) drive financial inclusion.
- **Impact Modeling:** Quantify how events like the entry of M-Pesa or the launch of the Fayda Digital ID affect inclusion.
- **Forecast:** Predict two core dimensions:
  1. **Access:** Account Ownership Rate
  2. **Usage:** Digital Payment Adoption Rate

## Current Status: Interim Submission (Tasks 1 & 2)
As of July 19, 2026, the following milestones have been completed:
- **Task 1: Data Exploration & Enrichment** 
  - Unified data schema implemented.
  - Enriched dataset with 2023/24 NBE administrative data and key market events.
- **Task 2: Exploratory Data Analysis (EDA)**
  - Visualized the "Access Paradox" and usage growth trends.
  - Created an interactive timeline overlaying 10+ national events onto inclusion trends.
  - Identified 5 key insights regarding Ethiopia's financial ecosystem.

## Repository Structure
```text
ethiopia-fi-forecast/
├── data/
│   ├── raw/                  # Original starter datasets
│   └── processed/            # Enriched and cleaned data for modeling
├── notebooks/
│   └── 01_Data_EDA.ipynb     # Task 1 & 2 implementation
├── reports/
│   ├── Interim_Report.md     # Summary of findings for stakeholders
│   └── figures/              # Saved visualizations
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
