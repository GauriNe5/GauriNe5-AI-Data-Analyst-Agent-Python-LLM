# AI Data Analyst Agent (Python + LLM )

## Overview
This project implements a **tool-using AI data analyst agent** that answers natural-language questions about structured CSV datasets.

The agent uses a **Large Language Model (LLM)** for reasoning and decision-making, while delegating all data computation to **deterministic Python tools** (pandas).  
This separation ensures **accuracy, transparency, and hallucination prevention**, mirroring real-world production AI agent architectures.

## Key Features
- Natural-language data analysis on CSV files
- LLM-driven **tool selection** (no hardcoded rules)
- Deterministic Python execution for data operations
- Business-friendly explanations of analytical results
- Command-line interface (CLI)
- Easily extensible to UI or API-based systems

## High-Level Architecture

User Question
↓
LLM (Reasoning & Tool Selection)
↓
Python Tools (Data Computation with pandas)
↓
LLM (Interpretation & Explanation)

**Design Principle:**  
- LLM decides *what* to do  
- Python decides *how* to do it  

## Available Tools

| Tool | Description |
|-----|------------|
| `summarize()` | Dataset overview: rows, columns, data types, preview |
| `groupby_agg()` | Group-by aggregations (mean, sum, min, max, count) |
| `filter_rows()` | Row-level filtering with numeric or string conditions |

## Tech Stack
- Python 3.10+
- OpenAI API (LLM with tool calling)
- pandas
- python-dotenv

## Project Structure
ai-data-analyst-agent/
├── app.py # Agent logic and control loop
├── tools.py # Deterministic data analysis tools
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── data/
└── sample.csv


## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/ai-data-analyst-agent.git
cd ai-data-analyst-agent

2. Create a Virtual Environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# OR
.\.venv\Scripts\Activate.ps1   # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file:
OPENAI_API_KEY=your_openai_api_key_here

5. Run the Agent
python app.py
