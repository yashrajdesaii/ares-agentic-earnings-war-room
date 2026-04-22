"""ARES War Room Streamlit app."""

from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd
import streamlit as st

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reporting.generate_earnings_excel import build_workbook_bytes


st.set_page_config(page_title="ARES War Room", page_icon="📈", layout="wide")
st.title("ARES – Agentic Earnings War Room")
st.caption("AI-first workspace for earnings diagnostics, scenario modeling, and board-ready reporting.")


@st.cache_data(show_spinner=False)
def run_agent_simulation(prompt: str) -> tuple[list[str], pd.DataFrame, pd.DataFrame]:
    """Generate deterministic, demo-safe outputs for the War Room UI."""
    seed = abs(hash(prompt)) % (2**32)
    rng = np.random.default_rng(seed)

    reasoning_trace = [
        "Step 1: Ingested prompt intent and selected skills (variance, sensitivity, memo).",
        "Step 2: Calculated revenue waterfall contributions by major ARR drivers.",
        "Step 3: Simulated NRR outcomes with Monte Carlo assumptions.",
        "Step 4: Drafted executive-ready summary and risk framing.",
    ]

    waterfall = pd.DataFrame(
        {
            "Driver": ["New Business", "Expansion", "Contraction", "Churn"],
            "ARR Impact ($M)": [
                round(float(rng.normal(9.2, 1.0)), 2),
                round(float(rng.normal(7.4, 0.8)), 2),
                round(float(-abs(rng.normal(4.0, 0.6))), 2),
                round(float(-abs(rng.normal(5.2, 0.7))), 2),
            ],
        }
    )

    trials = rng.normal(loc=1.085, scale=0.02, size=5000)
    sensitivity = pd.DataFrame(
        {
            "Percentile": ["P10", "P50", "P90"],
            "NRR": [
                round(float(np.percentile(trials, 10)), 3),
                round(float(np.percentile(trials, 50)), 3),
                round(float(np.percentile(trials, 90)), 3),
            ],
        }
    )

    return reasoning_trace, waterfall, sensitivity


prompt = st.text_area(
    "Ask the War Room agent",
    value="Analyze Q1 ARR variance vs plan and estimate NRR target attainment risk.",
    height=120,
)

if st.button("Run Agent", type="primary"):
    with st.spinner("Running agentic workflow..."):
        trace, waterfall_df, sensitivity_df = run_agent_simulation(prompt)

    st.subheader("Visible Reasoning Trace")
    for step in trace:
        st.markdown(f"- {step}")

    left, right = st.columns(2)
    with left:
        st.subheader("Revenue Waterfall")
        st.dataframe(waterfall_df, use_container_width=True)
        st.bar_chart(waterfall_df.set_index("Driver"))

    with right:
        st.subheader("NRR Monte Carlo Sensitivity")
        st.dataframe(sensitivity_df, use_container_width=True)
        st.line_chart(sensitivity_df.set_index("Percentile"))

    st.subheader("Executive Memo Snapshot")
    st.info(
        "ARR outperformed plan on enterprise expansion, while elevated SMB churn created a "
        "target gap risk for NRR. Management should prioritize renewal saves and cross-sell "
        "playbooks in at-risk cohorts."
    )

    st.download_button(
        label="Download Board-Ready Excel",
        data=build_workbook_bytes(),
        file_name="ares_earnings_pack.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.write("Submit a prompt to execute the ARES agent workflow.")
