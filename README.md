# 🛡️ Intel Reader

> **AI-powered Cyber-Geopolitical Intelligence Dashboard** — automatically ingests RSS feeds from top cybersecurity and world news sources, analyzes them with Google Gemini, and presents a filterable, threat-classified dashboard built with Streamlit.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

Intel Reader continuously monitors curated RSS feeds — CISA advisories, BleepingComputer, Reuters World News, and more — and uses **Google Gemini 2.5 Flash** to produce:

- **Concise AI summaries** of each article
- **Threat level classification** (High / Medium / Low / Info)
- **Named entity extraction** (countries, threat actors, organizations)
- **Geopolitical impact assessment**

All results are persisted in a local SQLite database and surfaced through an interactive Streamlit dashboard with real-time filtering.

---

## Features

| Feature | Description |
|---|---|
| 📡 RSS Ingestion | Polls multiple curated security & geopolitical feeds |
| 🤖 AI Analysis | Gemini 2.5 Flash generates summaries, threat ratings, and entity lists |
| 🗄️ SQLite Storage | Deduplicates articles and persists processed intel across runs |
| 🎨 Streamlit Dashboard | Color-coded threat cards with source & level filters |
| 🔄 Manual Refresh | One-click "Fetch & Analyze" button in the sidebar |
| 🐳 Docker Support | Fully containerized via Docker + Docker Compose |

---

## Project Structure

```
intel-reader/
├── agent.py            # RSS ingestion + Gemini AI analysis pipeline
├── app.py              # Streamlit dashboard UI
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container definition (Python 3.12-slim)
├── docker-compose.yml  # Multi-service orchestration
├── data/               # SQLite database (auto-created at runtime)
└── .github/workflows/  # CI/CD workflows
```

---

## Prerequisites

- **Python 3.12+** (for local setup)
- **Docker & Docker Compose** (for containerized setup)
- A **Google Gemini API key** — get one free at [Google AI Studio](https://aistudio.google.com/)

---

## Quickstart

### Option 1 — Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/FsocietyVoid/intel-reader.git
cd intel-reader

# 2. Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"

# 3. Build and run
docker compose up --build
```

The dashboard will be available at **http://localhost:8501**.

---

### Option 2 — Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/FsocietyVoid/intel-reader.git
cd intel-reader

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"

# 5. Run the ingestion agent (first-time data load)
python agent.py

# 6. Launch the dashboard
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Google Gemini API key |

### Adding RSS Feeds

Edit the `FEEDS` list in `agent.py` to add or remove sources. Any valid RSS or Atom feed URL is supported:

```python
FEEDS = [
    "https://www.cisa.gov/cybersecurity-advisories/feed",
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.reuters.com/reuters/worldNews",
    # Add your feeds here
]
```

---

## How It Works

```
RSS Feeds → feedparser → agent.py → Gemini 2.5 Flash
                                         │
                              ┌──────────▼──────────┐
                              │  AI-generated JSON:  │
                              │  • summary           │
                              │  • threat_level      │
                              │  • entities          │
                              │  • geopolitical_     │
                              │    impact            │
                              └──────────┬──────────┘
                                         │
                                   SQLite (data/)
                                         │
                              Streamlit Dashboard (app.py)
```

1. `agent.py` fetches each configured feed with `feedparser`.
2. New articles (identified by MD5 hash of URL) are passed to **Gemini 2.5 Flash** for analysis.
3. The structured JSON response is stored in a local SQLite database.
4. `app.py` renders the data as color-coded cards, filterable by **threat level** and **source**.
5. The sidebar "Fetch & Analyze" button lets users trigger an on-demand refresh.

---

## Dashboard

The dashboard displays articles as cards with threat-level color coding:

| Threat Level | Color | Meaning |
|---|---|---|
| 🔴 High | Red | Active exploits, critical vulnerabilities, major incidents |
| 🟠 Medium | Orange | Notable threats, significant geopolitical events |
| 🔵 Low | Blue | General advisories, minor incidents |
| ⚫ Info | Grey | Informational updates, background context |

Each card shows the **source**, **threat level**, **published date**, **AI summary**, **extracted entities**, and a **link to the original article**.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | ≥ 1.28 | Web dashboard UI |
| `feedparser` | ≥ 6.0 | RSS/Atom feed parsing |
| `google-generativeai` | ≥ 0.7 | Gemini AI integration |
| `pandas` | ≥ 2.2 | Data handling and display |

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your fork: `git push origin feature/your-feature`
5. Open a Pull Request.

Please keep commits focused and include a clear description of what changed and why.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Author

Built by **[Yash Bhujbal](https://github.com/FsocietyVoid)** · 2026
