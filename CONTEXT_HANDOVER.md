# Agentic QA Organization - Context Handover

This document summarizes the current state of the project to enable a seamless transition to a new chat session.

## Project Overview
A modular, testable, and self-improving Agentic QA system built using **LangGraph** and **LangChain**. The system can analyze requirements, plan missions, execute specialized tests (Functional, E2E, Security, Performance, etc.), and generate executive reports with Go/No-Go recommendations.

## Current Status: PRODUCTION READY
*   **Codebase**: Refactored, linted, and verified on Python 3.14.
*   **Configuration**: Externalized to `.env`.
*   **RAG**: Fully operational with FAISS indexing for mission outcomes.
*   **Orchestration**: Completed LangGraph workflow with Review and Eval loops.
*   **CI/CD**: Implementation includes a bridge for PR comments and quality gates.

## Key Components
### Core Infrastructure (`src/core/`)
*   `BaseAgent`: Foundational logic for LLM interaction, memory, and tools.
*   `Orchestrator`: LangGraph definition with dynamic routing nodes.
*   `KnowledgeBase`: Local FAISS vector store for RAG.
*   `ToolRegistry`: Management of specialist skills.
*   `MemoryManager`: Short-term and long-term agent persistence.

### Specialist Agents (`src/agents/`)
*   `QALead`: Planner and strategist.
*   `Functional`: Scenario generation and regression analysis.
*   `E2E`: User journey mapping and Playwright automation.
*   `Security`: Threat modeling and simulated scans.
*   `Performance`: Load test planning and metric analysis.
*   `Review`: Audit and critique of specialist reports.
*   `Eval`: Scoring and feedback on mission outcomes.
*   `Reporting`: Executive summary synthesis.

### Unified Entry Point
*   `main.py`: CLI for running missions and managing dependencies.

## Setup & Execution
### 1. Environment
*   **Python**: `python3` (3.14+ supported).
*   **Venv**: Active virtual environment in `./venv`.
*   **Env Variables**: Configured in `.env` (requires `OPENAI_API_KEY`).

### 2. How to Run
```bash
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:.
python main.py "Describe your QA mission here"
```

## Handover Details
*   **Recent Fixes**: Resolved strict type annotation errors and LangChain `ModuleNotFoundError` issues specific to Python 3.14.
*   **Latest Commit**: `bdb3cd2` (Refactor for production readiness).
*   **Data Persistence**: Agent memories are in `data/memory/`, and the Knowledge Base index is in `data/faiss_index/` (both ignored by git).

## Suggested Next Steps
1.  **UI Integration**: Build a frontend to visualize the LangGraph execution.
2.  **Real Tool Integration**: Replace simulated shell tools with actual Playwright, k6, or OWASP ZAP runners.
3.  **Advanced RAG**: Expand the Knowledge Base to ingest company-wide documentation or Jira tickets for even better grounding.
