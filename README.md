# ARES – The Agentic Earnings War Room

Manual earnings prep is often slow, fragmented, and error-prone across spreadsheets, ad hoc SQL, and disconnected narratives. ARES is an AI-first, agentic financial intelligence platform that turns repeatable finance workflows into autonomous skills to analyze revenue variance, run NRR sensitivity scenarios, and generate executive-ready outputs in minutes.

## Key Features

- **Autonomous revenue variance analysis** combining structured metric diagnostics with unstructured business-note summarization.
- **Monte Carlo sensitivity modeling** for NRR/ARR what-if scenarios with configurable assumptions.
- **Executive memo drafting** for board and leadership narratives, including risks and mitigation actions.
- **Board-ready Excel export** with multi-tab outputs: Summary Memo, Revenue Waterfall, NRR Sensitivity, Headcount, and IR Data.

## Tech Stack

- AI agents and reusable skills for finance workflows
- Semantic Views / semantic layer SQL definitions
- Dynamic Tables / incremental transformation pipelines
- Streamlit app for interactive War Room operations
- Native LLM function patterns for structured agent outputs
- `openpyxl` for professional Excel artifact generation

## Repository Layout

```text
.
├── AGENTS.md
├── README.md
├── coCo_log.md
├── reporting/
│   └── generate_earnings_excel.py
├── skills/
│   ├── earnings_memo_draft_tool.skill.md
│   ├── revenue_variance_analyzer.skill.md
│   └── sensitivity_model.skill.md
├── sql/
│   ├── dynamic_tables.sql
│   └── semantic_views.sql
└── streamlit/
    ├── app.py
    └── snowflake.yml
```

## How to Run

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies:
   ```bash
   pip install streamlit pandas numpy openpyxl
   ```
3. Launch the War Room app:
   ```bash
   streamlit run streamlit/app.py
   ```
4. In the app, submit a prompt, inspect the reasoning trace, review charts, and download the generated Excel artifact.

## How to Test

Run the reporting script directly to verify workbook generation:

```bash
python reporting/generate_earnings_excel.py
```

It writes a sample workbook to `./artifacts/ares_earnings_pack.xlsx`.

## Impact

**"Collapses multi-day earnings workflows into minutes using agentic AI"**
