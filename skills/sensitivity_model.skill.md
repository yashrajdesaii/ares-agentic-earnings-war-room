# Skill: Sensitivity Model

## Purpose
Run Monte Carlo simulations for NRR/ARR scenarios to estimate downside/upside ranges under uncertainty.

## Inputs
- Current ARR base
- Distribution assumptions for:
  - Gross churn
  - Expansion rate
  - New logo ARR
  - Contraction pressure
- Number of trials (default: 5,000)
- Scenario metadata (base, conservative, aggressive)

## Workflow
1. Validate parameter ranges and reject invalid inputs.
2. Sample distributions for each trial.
3. Compute projected ARR and NRR outcome for each draw.
4. Aggregate outcomes into percentile bands (P10/P50/P90).
5. Estimate probability of meeting board target threshold.
6. Return simulation summary for charts + workbook tab.

## Outputs
- Scenario table by percentile
- Probability of achieving target NRR
- Driver sensitivity ranking

## Guardrails
- Use reproducible random seeds when requested.
- Cap impossible values (e.g., negative ARR).
- Include assumptions alongside outputs for auditability.
