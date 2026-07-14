from __future__ import annotations

import os
import json
import sys

# Ensure the Test directory is in the sys.path so modules can be imported
test_dir = os.path.dirname(os.path.abspath(__file__))
if test_dir not in sys.path:
    sys.path.insert(0, test_dir)

def pytest_sessionfinish(session, exitstatus):
    """
    Hook executed after all tests are finished.
    Saves the execution stats to a JSON file and runs the chart/HTML generation.
    """
    try:
        from algorithm_config import EXECUTION_RESULTS
    except ImportError:
        print("Could not import EXECUTION_RESULTS from algorithm_config.")
        return

    # Put the reports folder at the workspace root
    workspace_dir = os.path.dirname(test_dir)
    reports_dir = os.path.join(workspace_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    results_path = os.path.join(reports_dir, "test_results.json")

    # Save to JSON
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(EXECUTION_RESULTS, f, indent=4, ensure_ascii=False)

    print(f"\n[Pytest Hook] Saved {len(EXECUTION_RESULTS)} executions to {results_path}")

    # Generate charts and HTML
    try:
        from generate_charts import generate_reports_and_charts
        generate_reports_and_charts(results_path=results_path, output_dir=reports_dir)
    except Exception as e:
        print(f"[Pytest Hook] Error generating charts and dashboard: {e}")
