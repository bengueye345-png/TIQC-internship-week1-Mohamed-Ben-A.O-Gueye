# csv-gpa CLI Utility

## Overview

`csv-gpa` is a simple Python command-line tool that reads a `students.csv` file, extracts valid GPA values, and prints the **average GPA rounded to two decimal places**.
The program skips malformed or invalid rows gracefully without crashing.

---

## How to Run the Program

### 1. Make sure Python is installed

```bash
python3 --version
```

### 2. Run the script

```bash
python3 csv_gpa.py
```

Or (after making it executable):

```bash
chmod +x csv_gpa.py
./csv_gpa.py
```

### 3. Run with a specific CSV file

```bash
./csv_gpa.py students_test2.csv
```

---

## Assumptions

* The CSV file contains a **header row** with a column named `gpa`.
* GPA values are **numeric** and within a reasonable range.
* Invalid entries (blank, text, malformed numbers) are **ignored**.
* If **no valid GPAs** are found, the program prints an error message instead of crashing.

---

## Sample Output

### Test 1 — Valid GPAs

Input (`students.csv`):

```
name,id,gpa
Alice,1001,3.8
Bob,1002,3.2
Evan,1005,4.0
```

Command:

```bash
./csv_gpa.py students.csv
```

Output:

```
3.67
```

---

### Test 2 — Mixed Valid and Invalid Rows

Input (`students_test2.csv`):

```
name,id,gpa
Alice,1001,3.8
Bob,1002,not_a_number
Charlie,1003,
Dina,1004,4.0
```

Output:

```
3.90
```

---

### Test 3 — No Valid GPA Values

Input (`students_test3.csv`):

```
name,id,gpa
Alice,1001,abc
Bob,1002,
Charlie,1003,?
```

Output:

```
No valid GPA values found.
```

---

## Source Code (CLI Utility)

```python
#!/usr/bin/env python3
import csv
import sys

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "students.csv"

    try:
        total = 0
        count = 0

        with open(filename, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    gpa = float(row["gpa"])
                    total += gpa
                    count += 1
                except:
                    continue

        if count == 0:
    
```
