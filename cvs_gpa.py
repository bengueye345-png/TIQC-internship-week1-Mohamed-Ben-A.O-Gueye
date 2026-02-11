#!/usr/bin/env python3
"""
csv-gpa: Reads a students.csv file and prints the average GPA (rounded to two decimals).

Expected input: a CSV with a header row that includes a GPA column (e.g., "gpa").
Skips invalid/malformed rows gracefully.
"""

from __future__ import annotations

import argparse
import csv
import sys
from typing import Optional


POSSIBLE_GPA_HEADERS = {
    "gpa",
    "grade_point_average",
    "gradepointaverage",
    "grade point average",
    "grade-point-average",
}


def normalize_header(s: str) -> str:
    return " ".join(s.strip().lower().replace("-", " ").replace("_", " ").split())


def find_gpa_column(fieldnames: list[str]) -> Optional[str]:
    """
    Returns the actual column name that corresponds to GPA (as it appears in the CSV),
    or None if not found.
    """
    # direct match after normalization
    for name in fieldnames:
        if normalize_header(name) in POSSIBLE_GPA_HEADERS:
            return name

    # fallback: any header containing 'gpa' after normalization
    for name in fieldnames:
        if "gpa" in normalize_header(name):
            return name

    return None


def parse_gpa(value: str) -> Optional[float]:
    """
    Parse GPA from string. Returns float if valid, otherwise None.
    Allows values like '3.5' or ' 3.50 '.
    Rejects negatives and absurdly high values (basic sanity check).
    """
    if value is None:
        return None

    raw = value.strip()
    if raw == "":
        return None

    try:
        gpa = float(raw)
    except ValueError:
        return None

    # Basic sanity bounds (adjust if your program uses different scale)
    if gpa < 0.0 or gpa > 5.0:
        return None

    return gpa


def compute_average_gpa(csv_path: str) -> float:
    total = 0.0
    count = 0

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV appears to have no header row.")

        gpa_col = find_gpa_column(reader.fieldnames)
        if gpa_col is None:
            raise ValueError(
                f"Could not find a GPA column. Found headers: {reader.fieldnames}"
            )

        for row_num, row in enumerate(reader, start=2):  # header is line 1
            try:
                gpa = parse_gpa(row.get(gpa_col, ""))
                if gpa is None:
                    # skip invalid/malformed row
                    continue
                total += gpa
                count += 1
            except Exception:
                # Any unexpected row-level issue: skip gracefully
                continue

    if count == 0:
        raise ValueError("No valid GPA values found in the CSV.")

    return total / count


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="csv-gpa",
        description="Read a students.csv file and print the average GPA (rounded to two decimals).",
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default="students.csv",
        help="Path to CSV file (default: students.csv)",
    )
    args = parser.parse_args()

    try:
        avg = compute_average_gpa(args.csv_file)
        print(f"{avg:.2f}")
        return 0
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv_file}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
