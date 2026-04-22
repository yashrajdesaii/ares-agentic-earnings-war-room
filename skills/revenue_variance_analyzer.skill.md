# Skill: Revenue Variance Analyzer

## Purpose
Identify and explain ARR/revenue variance against plan and prior periods by combining structured data analysis with unstructured management-note synthesis.

## Inputs
- Period scope (quarter, fiscal year)
- Baseline (`plan`, `prior_quarter`, `prior_year`)
- Segment dimensions (geo, product, customer tier, sales motion)
- Optional note corpus (deal notes, forecast commentary, pipeline updates)

## Workflow
1. Query semantic finance views for ARR, NRR, churn, expansion, and net-new components.
2. Decompose variance into waterfall drivers:
   - Starting ARR
   - Expansion
   - Contraction
   - Churn
   - New Business
3. Rank top positive/negative contributors by absolute and percent impact.
4. Summarize unstructured notes into tagged themes (execution, macro, pricing, product).
5. Link themes to quantified drivers with confidence scores.
6. Emit a structured analysis object for memo and Excel export.

## Outputs
- Revenue variance table with driver deltas
- Root-cause summary with confidence tags
- Suggested management actions for each major negative driver

## Guardrails
- Never infer causality without supporting data or note evidence.
- Flag anomalies caused by incomplete period data.
- Preserve traceability from each conclusion to source metric(s).
