# 🤖 Agentic QA Organization

An autonomous, multi-agent AI system designed to orchestrate, execute, and analyze end-to-end software quality assurance missions. Built on **LangGraph**, **FastAPI**, and **React**.

![Mission Dashboard](/Users/danielannankra/.gemini/antigravity/brain/cce460a7-c053-4b48-a1bc-3bce0885cfa4/mission_execution_dashboard_1770051339469.png)

## 🌟 Overview

The Agentic QA Organization transforms high-level testing requirements into executable missions. A **Lead Orchestrator** analyzes the mission, coordinates with **Specialist Agents** (Functional, E2E, Security, Performance), and generates a comprehensive Quality Gate report.

### Key Capabilities:
- **Autonomous Planning**: LangGraph-driven workflows that adapt based on agent findings.
- **Real Tool Execution**: Generates and runs real **Playwright** (E2E) and **k6** (Load Testing) scripts.
- **Advanced RAG**: Grounded in project context via **Jira Integration** and local knowledge bases.
- **TestRail Synchronization**: Automated result reporting via **Model Context Protocol (MCP)**.
- **Real-time Visualization**: A sleek web dashboard to monitor agent transitions and live log streams.

---

## 🏗️ Architecture

The system follows a decentralized multi-agent architecture:
- **Lead Planner**: Decomposes requests into specific agent tasks.
- **Specialist Agents**: 
  - `E2E Specialist`: Playwright automation generation and execution.
  - `Performance Expert`: Load testing with k6 metrics analysis.
  - `Security Specialist`: Vulnerability scanning and threat modeling.
  - `Functional/Unit Specialists`: Static analysis and logic verification.
- **Execution Engine**: A dedicated layer for safely running generated code in subprocesses.
- **Knowledge Base**: FAISS-powered vector store for retrieving Jira issues and past mission results.
- **MCP Server**: A sidecar service for integrating external tools like TestRail with standard protocols.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- [k6](https://k6.io/docs/getting-started/installation/) (for performance testing)
- Playwright browsers: `playwright install chromium`

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Annankra/qaorganization.git
cd qaorganization

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3. Configuration
Create a `.env` file in the root directory (see `.env.example` for details):
```env
OPENAI_API_KEY=your_key_here
JIRA_URL=https://your-domain.atlassian.net
JIRA_USER_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-token

# TestRail Configuration (MCP)
TESTRAIL_URL=https://your-domain.testrail.io
TESTRAIL_USER=your-email@example.com
TESTRAIL_API_KEY=your-api-key
```

---

## 🛠️ Running the System

### Full-Stack Dashboard (Recommended)
Launch both services to use the glassmorphic mission control:

**Backend (API & Agents):**
```bash
export PYTHONPATH=$PYTHONPATH:.
./venv/bin/python3 src/server.py
```

**Frontend (Visualization):**
```bash
cd frontend
npm run dev
```
Navigate to `http://localhost:5173` to start a mission.

### CLI Mode (Standalone)
Run a specific mission directly from the terminal:
```bash
./venv/bin/python3 main.py --mission "Test the checkout flow for performance regressions"
```

---

## 📈 Dashboard Preview

The dashboard provides real-time visibility into the "Brain" of the QA organization:
- **Node Graph**: Status indicators for all specialist agents.
- **Activity Stream**: SSE-powered live terminal logs.
- **Report Terminal**: Markdown-rendered mission summaries.

---

## 📜 License
MIT License - See the [LICENSE](LICENSE) file for details.
