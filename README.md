# Grünenthal AI Agent Chatbot

A multi-agent workflow system built with `uv` package manager and `google-adk` Agent Development Kit (ADK) framework for Grünenthal's AI-powered chatbot solution.

---

## Overview

This project implements an intelligent AI agent that can answer real-world questions by leveraging multiple data sources and tools. The agent dynamically selects appropriate tools, executes queries, and provides clear, actionable answers through an intuitive chatbot interface.

---

## Key Features

- **Multi-tool Integration**: Seamlessly connects to Neo4j graph database, FDA Adverse Events API, and Grünenthal's financial reports  
- **Dynamic Tool Selection**: Intelligent agent that decides which tool to use based on query context  
- **Real-time Query Processing**: Executes dynamic queries and returns structured responses  
- **User-friendly Interface**: Clean, responsive chatbot UI for easy interaction  
- **Production Ready**: Fully deployed and accessible online  

---

## Architecture

### Data Sources & Tools

- **Neo4j Graph Database**: Complex relationship queries and graph-based data analysis  
- **FDA Adverse Events API**: Real-time access to adverse event reporting data  
- **Grünenthal Financial Reports**: Company-specific financial data and insights using `google search engine` 

### Agent Framework

Built using Agent Development Kit (ADK) for robust multi-agent orchestration with:

- Tool selection logic  
- Query routing capabilities  
- Response formatting and validation  
- Error handling and fallback mechanisms  

---

## Prerequisites

- Python 3.9+  
- `uv` package manager  
- Neo4j database instance  
- API keys for external services  

---

## Installation

### 1. Install uv Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
### 2. Clone and Setup Project
```bash
git clone <repository-url>
cd grun
```

### 3. Create Virtual Environment and Install Dependencies
```bash
# Create virtual environment with uv
uv venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Install dependencies
uv sync
```

### 4. Environment Configuration
```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
# Gemini Configuration or other
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_api_key
```

## Project Structure
```bash
grun/
├── multi_tool_agent/
│   ├── sub_agents/
│   │   ├── sub_agents/
│   │   │   ├── grunenthal_financial_report_websearch/
│   │   │   └─── healthcare_neo4j/
│   │   ├─── __init__.py
│   │   ├── .env
│   │   ├── openfda_tool.py
│   │   ├── prompt.py
│   │   ├── streamlit_agent.py
│   │   └── agent.py
├── tests/
├── docs/
├── apps/
├── uv.lock
├── config.py
├── streamlit_ui.py
├── pyproject.toml
└── README.md
```

## Local Development
```bash
# Start the Streamlit application
uv run streamlit run streamlit_ui.py

# Or run with adk interface
adk web
```

## Development
```bash

```

## QA examples
```bash
# healthcare_neo4j
├── What are the top 5 side effects reported?

├── What are the top 5 drugs reported with side effects? Get drugs along with their side effects.

├── What are the 5 most common side effects reported in the United States?
    # The 5 most common adverse drug events reported in the United States are:

    # Fatigue (303 cases)
    # Product dose omission issue (285 cases)
    # Headache (272 cases)
    # Nausea (256 cases)
    # Pain (253 cases)


# OpenFDA
├── What are the top 10 most recent adverse events registered for a drug containing TRAMADOL in its name?
    # The adverse event reports for drugs containing TRAMADOL in their name indicate the following:
    # TRAMADOL HYDROCHLORIDE: This drug has 14 application numbers and is manufactured by multiple companies.
    # Common Brand Names: TRAMADOL HYDROCHLORIDE and CONZIP.
    # Reported Adverse Events: The specific adverse events are detailed in the full reports, but some include "Hallucination, visual", "Headache", "Insomnia", "Somnolence", "Confusional state".
    # It's important to note that these are just summaries of the reports.

# grunenthal_financial_report_websearch
├── How has Grünenthal’s financial performance evolved since 2017, and what were the main drivers of its growth in 2024?
    # Grünenthal’s financial performance has significantly improved since 2017, with profitability (adjusted EBITDA) more than tripling and the company's value also increasing more than threefold. In 2024, Grünenthal sustained its record revenue level of €1.8 billion and increased its adjusted EBITDA by 9% to €412 million, driven primarily by the growth of Qutenza™ sales and the strategic acquisition of Valinor Pharma. Disciplined cost management and advancements in the R&D pipeline also contributed to this growth.

├── What are Grünenthal’s key strategies and recent investments in research and development for non-opioid pain treatments?

├── How does Grünenthal approach sustainability and corporate responsibility, and what recognitions has it received for its ESG initiatives in 2024?
```