# ResearchMind: Multi-Agent AI Research System

**ResearchMind** is an autonomous multi-agent AI research pipeline built using LangChain, Google's Gemini 2.5 Flash, and the Tavily Search API. It automates web retrieval, data scraping, and content synthesis by orchestrating specialized agents and chains to write and evaluate comprehensive, structured research reports.

---

## 🚀 Key Features
- **Multi-Agent Orchestration**: Sequential coordination of specialized agents and chains using LangChain.
- **Tavily Web Search**: Fast, reliable, and verified web search retrieval.
- **Deep Scraping**: Automated content extraction and cleaning from the most relevant search results using BeautifulSoup.
- **Automated Critique (LLM Judge)**: A dedicated critic evaluates drafts, provides constructive feedback, and scores them.
- **Modern UI**: A fully interactive Streamlit web dashboard.
- **CLI Mode**: Run research pipelines directly from the terminal.

---

## 🛠️ Architecture and Workflow

The system is structured as a sequential pipeline with four main phases:

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  01. Search     │      │   02. Reader    │      │   03. Writer    │      │   04. Critic    │
│     Agent       ├─────►│      Agent      ├─────►│     Chain       ├─────►│     Chain       │
│ (Tavily Search) │      │ (BeautifulSoup) │      │ (Gemini Draft)  │      │ (LLM Evaluator) │
└─────────────────┘      └─────────────────┘      └─────────────────┘      └─────────────────┘
```

1. **Search Agent (Tavily Search API)**: Gathers titles, URLs, and snippets of top 5 web results for a given query.
2. **Reader Agent (Requests & BeautifulSoup)**: Selects the most relevant URL from search results and extracts up to 3,000 characters of clean text.
3. **Writer Chain (LLM Writer)**: Synthesizes a structured markdown report including an Introduction, Key Findings (minimum of 3), a Conclusion, and a sources list.
4. **Critic Chain (LLM Judge)**: Evaluates the draft report, providing a score (out of 10), list of strengths, areas to improve, and a one-line verdict.

---

## 📂 Project Structure

```bash
multi_agent_system/
│
├── agents.py          # Sets up the Gemini LLM, Search/Reader agents, and Writer/Critic chains
├── app.py             # Streamlit web application interface
├── pipeline.py        # CLI entry point to run the research pipeline
├── tools.py           # Custom LangChain tools for Tavily Search and web scraping
├── requirements.txt   # Project dependencies
├── .env.example       # Example environment configuration file
└── .gitignore         # Prevents tracking virtual environments, caches, and secrets
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
Create a `.env` file in the root directory (you can copy `.env.example` if it exists) and add your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## 🚦 How to Run

### Command Line Interface (CLI)
Run the pipeline directly from your terminal:
```bash
python pipeline.py
```
*You will be prompted to enter a research topic, and the step-by-step progress and final report will print to the console.*

### Interactive Web UI (Streamlit)
To run the graphical user interface:
```bash
streamlit run app.py
```
*This opens a browser tab with a beautiful dark-mode interface where you can enter topics, watch agents run live, read & download reports, and view the critic's verdict.*
