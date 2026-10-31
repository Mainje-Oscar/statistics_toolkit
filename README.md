# Statistical Analysis Monitoring Toolkit

A statistical analysis monitoring toolkit engineered using Python's standard library. This toolkit is tailored for the Wakala Plus risk management team to clean messy mobile transaction logs submitted by agents and isolate outliers (potential fraud or input errors).

## Summary of findings

* **Data quality:** Out of **40 raw records**, the system successfully validated **34 rows** and indentified **6 rows** containing structural anomalies, missing spaces, or non-numeric typos.
* **Outliers isolated:** The IQR algorithm determined a valid operating ceiling of **KES 31,185.63**. Two transaction rows were way beyond this ceiling:
  * `KES 96,500.00` on 2026-09-18 by Agent `AG-104` in Nakuru.
  * `KES 88,400.00` on 2026-10-06 by Agent `AG-104` in Nakuru.
* Removing these two anomalous rows caused the sample standard deviation to drop from **KES 18,464.80** down to **KES 4,241.65**. This represents a huge reduction in statistical misinformation, defining a fairly accurate operating baseline for future risk alerts.

---

## Architectural choices and method justification.

### 1. Sample vs. Population Variance
The toolkit defaults to **Sample Variance (n - 1)** rather than Population Variance (n). Because this dataset captures a short-term temporal snapshot of agent deposits across only four regions, it represents a sample of ongoing behavior. Using an n - 1 denominator provides an unbiased estimate of deposit amount flactuations.

### 2. Quartile and interpolation selection
To ensure synchronization with standard data frameworks, the `quartiles()` function uses the **Linear interpolation method**. This method avoids step functions by interpolating indexes when calculating Q₁, Q₂, and Q₃.

### 3. Data cleaning and refusal logic
The system enforces data validation. It documents and drops values that cannot be trusted to avoid corrupting aggregate averages:
* **Missing/Blank values** (e.g., row 7 and row 29) are dropped as unsubmitted records.
* **Null placeholders** (such as `-` or `n/a` in rows 10 and 14) are intercepted.
* **Alphabetical typos** (such as `"abc"` or the character substitute `"12,40O"`) are tagged for validation instead of being guessed or coerced blindly.

---

## Workspace setup and execution

This workspace is managed using **uv** for fast and reproducible dependency.

### Prerequisites
Ensure you have `uv` installed on your laptop. If not, install it via the package manager:
```bash
pip install uv
```

### Run the main analysis pipeline
Execute the processing python script to calculate metrics, verify figures against NumPy, and compile the text report:
```bash
uv run stats_toolkit.py
```
This generates your final summary file inside `output/stats_report.txt`.

### Run the unit tests
To run the tests under `unittest`:
```bash
uv run python -m unittest -v test_stats_toolkit.py
```

---

## Project workspace structure
```text
stats-toolkit/                
├── stats_toolkit.py         
├── test_stats_toolkit.py    
├── data/
│   └── agent_deposits.csv  
├── output/
│    └── stats_report.txt
├── requirements.txt 
└── README.md   
```
