-- dynamic_tables.sql
-- Incremental finance pipelines for ARR/NRR/churn tracking.

-- Source assumptions:
-- 1) FINANCE_RAW.SUBSCRIPTION_EVENTS captures account-level ARR movements.
-- 2) EVENT_TYPE in ('new', 'expansion', 'contraction', 'churn').
-- 3) EVENT_DATE is normalized to UTC date.

create or replace dynamic table FINANCE_MART.DT_ARR_MOVEMENTS
target_lag = '5 minutes'
warehouse = ANALYTICS_WH
as
select
    date_trunc('quarter', event_date) as fiscal_quarter,
    account_id,
    segment,
    region,
    sum(case when event_type = 'new' then arr_delta else 0 end) as new_arr,
    sum(case when event_type = 'expansion' then arr_delta else 0 end) as expansion_arr,
    sum(case when event_type = 'contraction' then abs(arr_delta) else 0 end) as contraction_arr,
    sum(case when event_type = 'churn' then abs(arr_delta) else 0 end) as churn_arr,
    sum(arr_delta) as net_arr_delta
from FINANCE_RAW.SUBSCRIPTION_EVENTS
group by 1, 2, 3, 4;

create or replace dynamic table FINANCE_MART.DT_ACCOUNT_NRR
target_lag = '5 minutes'
warehouse = ANALYTICS_WH
as
with start_arr as (
    select
        fiscal_quarter,
        account_id,
        sum(starting_arr) as starting_arr
    from FINANCE_RAW.ACCOUNT_QUARTERLY_BASE
    group by 1, 2
),
movements as (
    select
        fiscal_quarter,
        account_id,
        sum(expansion_arr) as expansion_arr,
        sum(contraction_arr) as contraction_arr,
        sum(churn_arr) as churn_arr
    from FINANCE_MART.DT_ARR_MOVEMENTS
    group by 1, 2
)
select
    s.fiscal_quarter,
    s.account_id,
    s.starting_arr,
    coalesce(m.expansion_arr, 0) as expansion_arr,
    coalesce(m.contraction_arr, 0) as contraction_arr,
    coalesce(m.churn_arr, 0) as churn_arr,
    (s.starting_arr + coalesce(m.expansion_arr, 0) - coalesce(m.contraction_arr, 0) - coalesce(m.churn_arr, 0)) as ending_arr,
    iff(
        s.starting_arr = 0,
        null,
        (s.starting_arr + coalesce(m.expansion_arr, 0) - coalesce(m.contraction_arr, 0) - coalesce(m.churn_arr, 0)) / s.starting_arr
    ) as nrr
from start_arr s
left join movements m
    on s.fiscal_quarter = m.fiscal_quarter
   and s.account_id = m.account_id;
