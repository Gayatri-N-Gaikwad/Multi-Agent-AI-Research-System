# ResearchMind: Autonomous Multi-Agent AI Research System

**ResearchMind** is an enterprise-grade autonomous multi-agent research and synthesis engine built with **LangChain**, **Google Gemini 2.5 Flash**, and the **Tavily Search API**. 

Instead of relying on a single one-shot LLM prompt (which often suffers from hallucinations, dropped source links, and shallow analysis), ResearchMind decomposes research into specialized agents and chains orchestrated with an **automated Critic-in-the-loop reflection architecture**.

---

## 🚀 Key Architectural Highlights

- **Dynamic Agentic Search**: Autonomous Search Agent leveraging Google Gemini 2.5 Flash and Tavily Search API to find live, verified web sources.
- **Lossless Citation Extraction**: Extracts raw `ToolMessage` payloads directly from agent execution history, preventing URLs and citations from getting silently lost in LLM summaries.
- **Deterministic Multi-Source Scraper**: High-performance BeautifulSoup scraper that extracts and cleans body text from top search results while stripping boilerplate (`<script>`, `<style>`, `<nav>`, `<footer>`).
- **Strict Anti-Fabrication Prompting**: Enforced prompt constraints ensuring all factual claims and URLs are derived exclusively from verified research without hallucinations.
- **Automated LLM Judge (Critic Chain)**: Evaluates research drafts against a 4-pillar rubric (*Citation Grounding*, *Analytical Rigor*, *Temporal Grounding*, and *Structure*), returning a numerical score (`Score: X/10`).
- **Iterative Reflection & Self-Correction**: When a draft scores below the threshold (`SCORE_THRESHOLD = 8`), an automated revision chain refines the draft based on editorial critique (capped at `MAX_RETRIES = 2`).
- **Multi-Interface Deployment**: Supports interactive **Streamlit UI**, command-line **CLI**, headless **Flask/Gunicorn REST API**, and **Docker** containerization.

---

## 🛠️ Architecture & Workflow

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 RESEARCHMIND PIPELINE                                  │
└────────────────────────────────────────────────────────────────────────────────────────┘

 1. USER INPUT           2. DYNAMIC RETRIEVAL               3. DEEP EXTRACTION
 ┌─────────────┐        ┌────────────────────────┐         ┌────────────────────────┐
 │ Topic Query │───────►│  Search Agent (Tavily) │────────►│ Multi-Source Scraper   │
 └─────────────┘        │  Raw ToolMessage Parse │         │ (BeautifulSoup Clean)  │
                        └────────────────────────┘         └───────────┬────────────┘
                                                                       │
 6. PRODUCTION-READY REPORT         5. REFLECTION LOOP                 │ 4. SYNTHESIS
 ┌──────────────────────┐        ┌─────────────────────────┐           ▼
 │ Final Verified Report│◄───────┤ Critic: Automated Judge │◄──────────────────────┐
 │ (Scored ≥ 8 / Max)   │ (Pass) │ Evaluates 4 Rubrics     │   Writer Chain        │
 └──────────────────────┘        └───────────┬─────────────┘   (Drafts Synthesis)  │
                                             │ (Score < 8)             ▲
                                             ▼                         │
                                 ┌─────────────────────────┐           │
                                 │ Revision Chain          ├───────────┘
                                 │ (Applies Critique Diff) │
                                 └─────────────────────────┘
```

---

## 📂 Project Structure

```bash
multi_agent_system/
│
├── agents.py          # LLM initialization, Search Agent, Reader, Writer & Critic chains
├── app.py             # Streamlit interactive dashboard with live step progress cards
├── flask_app.py       # Headless REST API (/health, /api/research)
├── pipeline.py        # Core orchestration engine (run_research_pipeline & CLI main)
├── tools.py           # Custom LangChain tools (Tavily search & BeautifulSoup scraper)
├── utils.py           # Extractors for tool outputs, URL parsers, and score extractors
├── Dockerfile         # Production multi-stage container setup with healthcheck
├── .dockerignore      # Docker build context optimizations
├── requirements.txt   # Python dependencies (LangChain, Flask, Gunicorn, Streamlit)
├── .env.example       # Template for environment configuration
└── .gitignore         # Ignores virtual environments, cache files, and secrets
```

---

## ⚙️ Prerequisites & Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/Gayatri-N-Gaikwad/Multi-Agent-AI-Research-System.git
cd Multi-Agent-AI-Research-System
```

### 2. Set Up Python Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=5000
```

---

## 🚦 Execution Modes

### 1. Command Line Interface (CLI)
Run the pipeline directly from your terminal:

```bash
# Direct topic argument
python pipeline.py "Quantum computing breakthroughs"

# Interactive prompt mode
python pipeline.py
```

---

### 2. Headless REST API (Flask / Gunicorn)
Run as a standalone microservice:

```bash
python flask_app.py
```

#### Health Check
```bash
curl http://localhost:5000/health
# Response: {"status": "ok"}
```

#### Submit Research Request
```bash
curl -X POST http://localhost:5000/api/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "Quantum computing breakthroughs"}'
```

---

### 3. Interactive Web Dashboard (Streamlit)
Launch the rich visual UI with real-time pipeline monitoring and markdown export:

```bash
streamlit run app.py
```

---

### 4. Docker Containerization
Build and deploy the isolated service container:

```bash
# Build image
docker build -t researchmind-ai .

# Run container with environment variables
docker run -d -p 5000:5000 --env-file .env --name researchmind researchmind-ai
```

---

## 🌐 Enterprise Multi-Service Architecture

ResearchMind is designed to run behind a **Spring Boot 3.x Reactive Gateway (WebFlux Netty)** inside a shared Docker network (`research-network`):

- **API Gateway (`:8080`)**: Non-blocking public endpoint with a 200s timeout handling client traffic.
- **AI Engine (`:5000`)**: Containerized Python service executing LLM agent chains and deterministic web scrapers.
- **Memory Optimized**: JVM configured with `-Xmx256m -Xss256k` and Python slim image, enabling deployment on a single \$0 AWS free-tier `t2.micro` or `t3.micro` EC2 instance.

---

## 📜 License & Author

- **Author**: Gayatri Gaikwad
- **Repository**: [Multi-Agent-AI-Research-System](https://github.com/Gayatri-N-Gaikwad/Multi-Agent-AI-Research-System)
- **License**: MIT License
