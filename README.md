# ResearchMind: Multi-Agent AI Research System

**ResearchMind** is an autonomous multi-agent AI research pipeline built using LangChain, Google Gemini 2.5 Flash, and the Tavily Search API. It automates web retrieval, multi-source data scraping, report drafting, and iterative reflection loops to produce comprehensive, verified research reports.

---

## 🚀 Key Features

- **Multi-Agent & Chain Orchestration**: Sequential coordination of specialized search agents, deterministic scrapers, writer chains, and critic/revision reflection loops.
- **Tavily Web Search**: Fast, reliable, and verified web search retrieval with lossless URL extraction from raw tool messages.
- **Multi-Source Scraping**: Deterministic content extraction and cleaning from multiple top search URLs using BeautifulSoup with structured source labeling (`SOURCE 1`, `SOURCE 2`, etc.).
- **Iterative Reflection & Revision Loop**: An automated LLM Judge (Critic Chain) scores reports and triggers a Revision Chain if the quality score is below threshold (`SCORE_THRESHOLD = 8`), addressing specific critique points over multiple attempts (`MAX_RETRIES = 2`).
- **Strict Anti-Hallucination Prompting**: Enforced constraints ensuring URLs and facts are strictly derived from gathered research without fabrication.
- **Interactive UI & CLI Modes**: Run pipelines via a modern Streamlit web dashboard or directly from the terminal with optional CLI arguments.

---

## 🛠️ Architecture and Workflow

```
┌─────────────────┐      ┌─────────────────────────┐      ┌─────────────────┐      ┌─────────────────────────┐
│  01. Search     │      │  02. Multi-Source       │      │   03. Writer    │      │  04. Critic & Revision  │
│     Agent       ├─────►│      Scraper            ├─────►│     Chain       ├─────►│     Reflection Loop     │
│ (Tavily Search) │      │ (Deterministic Scraping)│      │ (Gemini Draft)  │      │ (Score & Self-Correction)│
└─────────────────┘      └─────────────────────────┘      └─────────────────┘      └────────────┬────────────┘
                                                                                                │ (Score < 8)
                                                                                                ▼
                                                                                   ┌─────────────────────────┐
                                                                                   │     Revision Chain      │
                                                                                   │ (Addresses Critique)    │
                                                                                   └─────────────────────────┘
```

1. **Search Agent (Tavily Search API)**: Gathers titles, URLs, and snippets of top web results. Raw `ToolMessage` outputs are extracted directly to prevent losing authentic URLs.
2. **Deterministic Multi-Source Scraper (Requests & BeautifulSoup)**: Parses the top search URLs (up to 3) and deterministically scrapes and cleans full-text content into labeled source sections.
3. **Writer Chain (LLM Writer)**: Synthesizes a structured report containing an Introduction, Key Findings (with source attribution), a Conclusion, and a Sources section matching the retrieved URLs.
4. **Critic & Reflection Loop (LLM Evaluator & Reviser)**: 
   - Evaluates the report and assigns a score (`Score: X/10`), strengths, areas to improve, and a verdict.
   - If the score is below `SCORE_THRESHOLD` (8/10), it invokes the **Revision Chain** with the critique and research to produce a revised draft (up to `MAX_RETRIES` iterations).

---

## 📂 Project Structure

```bash
multi_agent_system/
│
├── agents.py          # LLM setup, Search/Reader agents, Writer, Critic, and Revision chains
├── app.py             # Streamlit interactive web dashboard
├── pipeline.py        # CLI orchestration pipeline with reflection loop and argument support
├── tools.py           # Custom LangChain tools for Tavily Search and web scraping
├── utils.py           # Helper utilities for tool message extraction, URL parsing, multi-scraping, and score parsing
├── requirements.txt   # Project dependencies
├── .env.example       # Example environment configuration file
└── .gitignore         # Ignores virtual environments, cache files, and secrets
```

---

## ⚙️ Prerequisites and Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/Gayatri-N-Gaikwad/Multi-Agent-AI-Research-System.git
cd Multi-Agent-AI-Research-System
```

### 2. Set Up Virtual Environment
Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and configure your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## 🚦 How to Run

### Command Line Interface (CLI)
Run the research pipeline directly from your terminal:

**With argument:**
```bash
python pipeline.py "Quantum computing breakthroughs"
```

**Interactive mode:**
```bash
python pipeline.py
```

### Interactive Web UI (Streamlit)
To launch the graphical dashboard:
```bash
streamlit run app.py
```

### Running Utility Tests
To verify URL extraction logic:
```bash
python -c "from utils import extract_urls_from_search; print(extract_urls_from_search('URL: https://example.com\nURL: https://test.com'))"
```
