"""Runs automatically with pytest and saves the results to CSV and Excel."""

from datetime import datetime
from pathlib import Path

import pandas as pd

_results = []


def pytest_runtest_logreport(report):
    """Called by pytest after each test. We record the outcome."""
    # "call" is the phase where the test itself runs.
    # Also record tests that failed or were skipped during setup.
    if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
        file_name, test_name = report.nodeid.split("::", 1)
        error = ""
        if report.failed:
            error = report.longreprtext.strip().splitlines()[-1]
        _results.append({
            "Test file": file_name,
            "Test name": test_name,
            "Result": report.outcome.upper(),
            "Duration (s)": round(report.duration, 4),
            "Error message": error,
        })


def pytest_sessionfinish(session, exitstatus):
    """Called once after all tests finish. We write the report files."""
    if not _results:
        return

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame(_results)
    df.insert(0, "Run time", run_time)

    # CSV report
    df.to_csv(reports_dir / "test_report.csv", index=False)

    # Excel report with two sheets: Results and Summary
    total = len(df)
    passed = int((df["Result"] == "PASSED").sum())
    failed = int((df["Result"] == "FAILED").sum())
    summary = pd.DataFrame({
        "Metric": ["Run time", "Total tests", "Passed", "Failed", "Pass rate (%)"],
        "Value": [run_time, total, passed, failed, round(100 * passed / total, 1)],
    })
    with pd.ExcelWriter(reports_dir / "test_report.xlsx") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        df.to_excel(writer, sheet_name="Results", index=False)