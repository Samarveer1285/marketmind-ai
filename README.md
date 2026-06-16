# 🚀 MarketMind AI

### AI-Powered Executive Market Intelligence Platform for E-Commerce Decision Making

MarketMind AI is an end-to-end executive intelligence platform designed to transform raw e-commerce product data into actionable business insights.

The platform combines automated data ingestion, advanced analytics, anomaly detection, forecasting, generative AI, and executive dashboards to help decision-makers identify opportunities, monitor risks, and optimize strategy.

---

## 🎯 Project Objective

Traditional analytics dashboards focus on reporting historical metrics.

MarketMind AI goes beyond reporting by enabling users to:

- Predict future trends
- Detect anomalies automatically
- Identify hidden opportunities
- Benchmark competitors
- Segment customers and products
- Simulate strategic scenarios
- Generate AI-powered executive briefings

---

# ✨ Key Features

## 📈 Executive Intelligence Modules

### Market Analytics

- Pricing Analytics
- Growth Analytics
- Brand Analytics
- Market Intelligence
- Executive Summary

### Predictive Intelligence

- Forecasting
- Forecasting V2
- Portfolio Optimizer
- Scenario Simulator

### Opportunity Discovery

- Opportunity Scoring
- Product Segmentation
- Hidden Gems Detection

### Risk & Monitoring

- Anomaly Detection
- ML Anomaly Detection
- Market Alerts

### Strategic Intelligence

- Competitor Benchmarking
- Executive Scorecard
- Category Intelligence

### Customer Intelligence

- Customer Segmentation

### Generative AI

- AI Analyst Copilot
- Executive Briefings
- Natural Language Market Queries

---

# 🧠 AI Analyst Copilot

MarketMind AI integrates Gemini and LangChain to enable conversational market intelligence.

Users can ask questions such as:

- Which products have the highest risk and why?
- What categories show the strongest growth momentum?
- Which hidden gems should executives prioritize?
- Summarize this week's market intelligence.
- What products represent the biggest opportunities?

The Copilot converts analytics outputs into executive-ready insights.

---

# 🔄 Automated Data Pipeline

MarketMind AI continuously refreshes market snapshots using automated ingestion workflows.

## Data Sources

- Flipkart Product Listings
- Apify Scraping Actor

## Pipeline Flow

Flipkart Listings

↓

Apify Actor

↓

daily_ingestion.py

↓

Historical CSV Snapshots

↓

Analytics Engine

↓

AI Layer

↓

Executive Dashboards

---

# ⏰ Automation

## Windows Task Scheduler (Implemented)

Development automation is executed using Windows Task Scheduler.

Configured schedule:

- Every Monday at 10:00 AM
- Every Thursday at 10:00 AM

Responsibilities:

- Execute snapshot refresh
- Generate category snapshots
- Update historical repository
- Refresh MarketMind analytics

---

## n8n Workflow (Documented)

A conceptual n8n production workflow was designed to illustrate enterprise deployment architecture.

Workflow:

Schedule Trigger

↓

Invoke daily_ingestion.py

↓

Generate Category Snapshots

↓

Refresh MarketMind Analytics

---

# 🏗️ System Architecture

![MarketMind Architecture](architecture/MarketMind_Architecture.png)

The architecture integrates:

- Automated ingestion pipelines
- Historical snapshot storage
- Executive analytics modules
- Gemini-powered AI layer
- Streamlit dashboards
- Business decision support workflows

---

# 📸 Screenshots

## Dashboard

![Dashboard](docs/screenshots/dashboard.png)

---

## Market Intelligence

![Market Intelligence](docs/screenshots/market_intelligence.png)

---

## AI Analyst Copilot

![AI Copilot](docs/screenshots/ai_copilot.png)

---

## Windows Task Scheduler Automation

![Task Scheduler](docs/screenshots/task_scheduler.png)

---

## n8n Workflow Documentation

![n8n Workflow](docs/screenshots/n8n_workflow.png)

---

# 📂 Project Structure

```
MarketMind AI
│
├── analytics/
│   ├── charts/
│   └── reports/
│
├── architecture/
│   ├── MarketMind_Architecture.drawio
│   └── MarketMind_Architecture.png
│
├── backend/
│   ├── dashboard.py
│   ├── analytics_engine.py
│   ├── ai_copilot.py
│   ├── daily_ingestion.py
│   └── pages/
│
├── docs/
│   └── screenshots/
│
├── pipelines/
│   ├── ingestion_pipeline.py
│   ├── flipkart_pipeline.py
│   └── snapshots/
│
├── providers/
│
├── refresh_snapshots.bat
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Samarveer1285/marketmind-ai.git
cd marketmind-ai
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
APIFY_TOKEN=your_apify_token
ACTOR_ID=your_apify_actor_id
GEMINI_API_KEY=your_gemini_api_key
```

---

# ▶️ Running MarketMind AI

Launch Streamlit:

```bash
streamlit run backend/dashboard.py
```

Open:

```
http://localhost:8501
```

---

# 🔄 Refreshing Market Snapshots

Manual refresh:

```bash
python backend/daily_ingestion.py
```

OR

Execute:

```bash
refresh_snapshots.bat
```

Automation is handled by Windows Task Scheduler.

---

# 📊 Historical Snapshot Repository

MarketMind maintains historical category snapshots for trend analysis.

Categories include:

- Smartphones
- Gaming Laptops
- Tablets
- Bluetooth Speakers
- Computer Monitors
- Headphones
- Smartwatches
- Televisions
- Cameras
- Power Banks

Snapshots enable:

- Trend tracking
- Growth analysis
- Forecasting
- Opportunity detection
- Risk monitoring

---

# 🛠️ Technology Stack

## Frontend

- Streamlit

## Backend

- Python

## Data Processing

- Pandas
- NumPy

## Visualization

- Plotly
- Matplotlib

## Machine Learning

- Scikit-learn

## Forecasting

- Statistical Forecasting Models

## Generative AI

- Gemini
- LangChain

## Automation

- Windows Task Scheduler
- n8n (Conceptual Workflow)

## Data Acquisition

- Apify
- Flipkart

## Version Control

- Git
- GitHub

---

# 🚀 Future Enhancements

Potential future improvements include:

- Cloud deployment
- Docker containerization
- CI/CD pipelines
- Production n8n execution
- Multi-marketplace intelligence
- Real-time streaming ingestion
- Role-based access control

---

# 👨‍💻 Author

**Samarveer Thakur**

Built as an executive intelligence platform demonstrating the integration of analytics, machine learning, automation, and generative AI for strategic decision-making.

---

## ⭐ If you found this project interesting, consider starring the repository.
