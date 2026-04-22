# Copilot Instructions for ARES Repository

## Mission
Build AI-first, agentic workflows that automate finance analytics and produce board-ready outputs.

## Repository Conventions
- Prefer deterministic, auditable logic for metric calculations.
- Keep metric definitions explicit (ARR, NRR, churn, expansion, contraction).
- Write outputs in stakeholder language, not only technical terms.
- Preserve folder boundaries:
  - `skills/` for reusable agent behavior contracts
  - `sql/` for semantic layer and incremental pipelines
  - `streamlit/` for user interaction and trace visibility
  - `reporting/` for workbook artifact generation

## Coding Guidance
- Use typed Python where practical and keep functions composable.
- Ensure any randomness in simulations supports seeded reproducibility.
- Keep Streamlit interactions responsive; cache expensive operations.
- Do not hardcode vendor-specific assumptions unless explicitly required.

## Quality Checks
- Verify generated Excel includes all required tabs.
- Confirm memo outputs include risks + mitigation actions.
- Validate SQL aligns with semantic business definitions.
