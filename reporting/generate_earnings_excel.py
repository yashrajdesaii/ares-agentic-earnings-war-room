"""Generate board-ready ARES earnings workbook artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)
TITLE_FONT = Font(size=14, bold=True)


def _write_table(sheet, start_row: int, headers: Iterable[str], rows: Iterable[Iterable[object]]) -> None:
    """Write a formatted table to the given worksheet."""
    header_list = list(headers)
    for col_idx, header in enumerate(header_list, start=1):
        cell = sheet.cell(row=start_row, column=col_idx, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center")

    for row_offset, row_values in enumerate(rows, start=1):
        for col_idx, value in enumerate(row_values, start=1):
            sheet.cell(row=start_row + row_offset, column=col_idx, value=value)

    for col_idx in range(1, len(header_list) + 1):
        sheet.column_dimensions[get_column_letter(col_idx)].width = 20


def build_workbook_bytes() -> bytes:
    """Build and return the earnings workbook as bytes."""
    wb = Workbook()

    ws_summary = wb.active
    ws_summary.title = "Summary Memo"
    ws_summary["A1"] = "ARES Quarterly Earnings Summary"
    ws_summary["A1"].font = TITLE_FONT
    ws_summary["A3"] = (
        "ARR closed at $124.5M (+6.8% QoQ). NRR held at 108.4%, below the 110.0% board target, "
        "primarily due to SMB churn pressure offset by Enterprise expansion."
    )
    ws_summary["A5"] = "Top Risks"
    ws_summary["A5"].font = Font(bold=True)
    ws_summary["A6"] = "1) SMB churn remains elevated in EMEA."
    ws_summary["A7"] = "2) Mid-market renewals concentrated in Q+1."
    ws_summary["A8"] = "3) Pricing uplift adoption variance by segment."
    ws_summary.column_dimensions["A"].width = 120

    ws_waterfall = wb.create_sheet("Revenue Waterfall")
    _write_table(
        ws_waterfall,
        start_row=2,
        headers=["Driver", "ARR Impact ($M)"],
        rows=[
            ("Starting ARR", 116.5),
            ("New Business", 9.4),
            ("Expansion", 7.8),
            ("Contraction", -4.1),
            ("Churn", -5.1),
            ("Ending ARR", 124.5),
        ],
    )

    ws_sensitivity = wb.create_sheet("NRR Sensitivity")
    _write_table(
        ws_sensitivity,
        start_row=2,
        headers=["Scenario", "P10 NRR", "P50 NRR", "P90 NRR", "Pr(NRR >= 110%)"],
        rows=[
            ("Conservative", 1.03, 1.06, 1.09, 0.21),
            ("Base", 1.05, 1.08, 1.12, 0.47),
            ("Aggressive", 1.07, 1.11, 1.15, 0.73),
        ],
    )

    ws_headcount = wb.create_sheet("Headcount")
    _write_table(
        ws_headcount,
        start_row=2,
        headers=["Function", "Current HC", "QoQ Change", "Commentary"],
        rows=[
            ("Sales", 148, 6, "Hiring focused on enterprise overlays"),
            ("Customer Success", 92, 4, "Retention pods added for SMB"),
            ("R&D", 176, 8, "Roadmap acceleration for core platform"),
        ],
    )

    ws_ir = wb.create_sheet("IR Data")
    _write_table(
        ws_ir,
        start_row=2,
        headers=["Metric", "Value", "Unit", "Period"],
        rows=[
            ("ARR", 124.5, "USD Millions", "FY26 Q1"),
            ("NRR", 1.084, "Ratio", "FY26 Q1"),
            ("Gross Churn", 0.061, "Ratio", "FY26 Q1"),
            ("Expansion Rate", 0.094, "Ratio", "FY26 Q1"),
        ],
    )

    from io import BytesIO

    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


def main() -> None:
    """Generate a local workbook artifact for quick verification."""
    output_path = Path("artifacts/ares_earnings_pack.xlsx")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(build_workbook_bytes())
    print(f"Workbook created at: {output_path.resolve()}")


if __name__ == "__main__":
    main()
