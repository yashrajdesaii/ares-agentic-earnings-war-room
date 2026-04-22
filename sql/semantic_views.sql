-- semantic_views.sql
-- Business-facing semantic layer for earnings analysis.

create or replace view FINANCE_SEMANTIC.V_EARNINGS_KPIS as
select
    n.fiscal_quarter,
    b.segment,
    b.region,
    sum(b.starting_arr) as starting_arr,
    sum(n.expansion_arr) as expansion_arr,
    sum(n.contraction_arr) as contraction_arr,
    sum(n.churn_arr) as churn_arr,
    sum(n.ending_arr) as ending_arr,
    iff(sum(b.starting_arr) = 0, null, sum(n.ending_arr) / sum(b.starting_arr)) as nrr,
    sum(n.ending_arr) - sum(b.plan_arr) as arr_gap_to_plan,
    sum(n.ending_arr) - sum(b.plan_arr) as the_gap
from FINANCE_MART.DT_ACCOUNT_NRR n
join FINANCE_RAW.ACCOUNT_QUARTERLY_BASE b
  on n.fiscal_quarter = b.fiscal_quarter
 and n.account_id = b.account_id
group by 1, 2, 3;

comment on view FINANCE_SEMANTIC.V_EARNINGS_KPIS is
'Semantic KPI view for quarterly earnings prep. Includes NRR and the gap (actual ending ARR minus plan ARR).';

create or replace view FINANCE_SEMANTIC.V_REVENUE_WATERFALL as
select
    fiscal_quarter,
    segment,
    region,
    sum(new_arr) as new_arr,
    sum(expansion_arr) as expansion_arr,
    sum(contraction_arr) as contraction_arr,
    sum(churn_arr) as churn_arr,
    sum(net_arr_delta) as net_arr_delta
from FINANCE_MART.DT_ARR_MOVEMENTS
group by 1, 2, 3;

comment on view FINANCE_SEMANTIC.V_REVENUE_WATERFALL is
'Waterfall-ready ARR movement metrics by quarter, segment, and region.';
