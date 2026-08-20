#Greencell Mobility — Data Analysis Assignment

Data visualization and interpretation assignment completed for Greencell Mobility (NueGo) as part of their Connected Vehicles & Data Analysis internship screening process.

The task: analyze a time-series voltage dataset from the electric bus fleet, identify usage patterns, and surface anomalies — first in Excel, then reproduced and extended in Python.

Overview

The dataset (Sample_Data.csv) contains 21,919 timestamped voltage readings captured over roughly one week (26 June – 3 July 2024). The readings show a repeating charge/discharge cycle consistent with EV battery behavior — a fast rise to full charge followed by a gradual discharge during operation, repeating daily.

This repo contains both the Excel exploration and the Python solution requested in the assignment brief.

Repository Structure
File	Description
python_solution.ipynb	Main Jupyter notebook — data import, charting, moving averages, peak/trough detection, threshold analysis, and the bonus slope-acceleration task
requirements.txt	Python dependencies needed to run the notebook
task1 moving averages.png	Voltage chart with 1000-value and 5000-value moving averages (Python-generated, matches the Excel chart)
task2 5day moving average (1).png	Supplementary moving average visualization
task3 peaks and lows.csv	Tabulated local peaks and troughs detected in the voltage signal
task4 below 20 voltage.csv	Every instance where voltage dropped below 20 (see Findings)
task bonus accelerating downward.csv	Bonus task — timestamps where the downward (discharge) slope accelerates within each cycle
Assignment Requirements

1. Excel — Data Visualization Plot Voltage vs. Timestamp, add a trendline, and write a short interpretation of the pattern.

2. Python — Data Manipulation

Import the data into a DataFrame and reproduce the Excel chart
Overlay 1000-value and 5000-value moving averages
Detect and tabulate local peaks and lows
Detect and tabulate every instance voltage dropped below 20

3. Bonus

Detect points where the downward slope accelerates within each discharge cycle
Host the solution (this repository serves that purpose)
Setup
bash
git clone https://github.com/Yashgupta-01/Green-cell-mobility-assignment.git
cd Green-cell-mobility-assignment
pip install -r requirements.txt
jupyter notebook python_solution.ipynb
Methodology
Moving averages: Computed as simple rolling windows over the raw reading order (1000-point and 5000-point), matching the logic used in the Excel AVERAGE() formulas so both versions are directly comparable.
Peak/trough detection: Used scipy.signal.find_peaks with a prominence threshold rather than naive local-max/min comparison, since the raw data contains many duplicate and near-duplicate consecutive readings that would otherwise register as false turning points.
Threshold check (below 20): Direct filter on the raw values, no smoothing applied — this needs to reflect true readings, not a smoothed approximation.
Slope acceleration (bonus): Within each identified discharge cycle (peak → trough), computed point-to-point slope and flagged timestamps where the slope became more negative than the preceding interval — i.e., the discharge rate increasing.
Findings
The data shows a clear repeating charge/discharge cycle, consistent with scheduled depot charging followed by daytime route operation.
The overall trendline is close to flat, indicating stable battery performance across the observation week rather than degradation.
Discharge depth varies by cycle (some cycles bottom out near 25, others only fall to ~55–60), suggesting variation in route length or duty intensity day to day.
No readings fell below 20 — the dataset's true minimum is 25, so task4 below 20 voltage.csv is intentionally empty. This is a valid result, not a bug in the detection logic.
Author

Yash Gupta Submitted as part of the Greencell Mobility (NueGo) internship screening assignment.
