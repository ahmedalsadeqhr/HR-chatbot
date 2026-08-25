# Toki — HR Assistant for 51Talk Egypt

An AI-powered HR chatbot built with Streamlit and Groq. Helps 51Talk Egypt employees with leave policies, salary calculations, payslip analysis, and iTalent system guidance.

## Features

- **Salary calculator** — Egyptian 2026 tax brackets, social insurance, Martyrs Fund
- **Payslip vision** — upload a payslip image and ask questions about it
- **HR knowledge base** — leave policies, attendance rules, conduct, resignation procedures
- **iTalent guidance** — clock-in/out, leave requests, business trips
- **Bilingual** — Arabic (RTL) and English

## Setup

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com)

### Install

```bash
pip install -r requirements.txt
```

### Configure secrets

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

Or set the environment variable:

```bash
export GROQ_API_KEY="your-groq-api-key"
```

### Run

```bash
streamlit run app.py
```

## Project Structure

```
HR-chatbot/
├── app.py                  # Streamlit UI — entry point
├── salary_calculator.py    # Egyptian tax & salary logic
├── knowledge_base.py       # Handbook text + system prompt builder
├── translations.py         # UI strings (Arabic & English)
├── groq_client.py          # Groq API wrapper with error handling
├── styles.py               # CSS theme (warm starfield design)
├── tests/
│   └── test_salary_calculator.py   # 52 unit tests
├── requirements.txt
└── toki.png                # Mascot image
```

## Running Tests

```bash
pytest tests/ -v
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Groq API key (also readable from `.streamlit/secrets.toml`) |

## Models Used

| Feature | Model |
|---------|-------|
| Text Q&A | `openai/gpt-oss-120b` |
| Payslip vision | `qwen/qwen3.6-27b` |
