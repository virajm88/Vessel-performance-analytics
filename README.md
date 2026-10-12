# Capesize Vessel Performance & Fuel Consumption Analysis

Independent learning project | October 2026

**Data disclaimer:** All vessel characteristics, daily observations, weather effects, and hull degradation are synthetic. This is not a validated naval-architecture model or actual fleet performance data.

## Run

```bash
python -m pip install -r requirements.txt
python analyze.py
```

This creates `noon_reports_synthetic.csv`, `performance_analysis.csv`, `speed_power.png`, `daily_deviation.png`, and `summary.txt`.

For SQL practice, load `noon_reports_synthetic.csv` into a SQLite table named `noon_reports`, then run `queries.sql`. You can also use the included `load_sqlite.py` to generate the database automatically.

## Model

- Illustrative reference: 14 knots, 8,000 kW shaft power.
- Calm-water power approximation: P = 8000*(V/14)^3, with a draft adjustment.
- Fuel use: main-engine power (kW) * specific fuel oil consumption (g/kWh) * 24 / 1,000,000 = tonnes/day.
- Synthetic weather and hull degradation add multipliers to shaft power; auxiliary consumption is a fixed 2 tonnes/day.
- Simplified example assumptions are not calibrated to any real vessel.

## Interpretation caveats

Fuel deviations cannot alone prove hull fouling. Real-world analysis should account for weather, currents, draft/displacement, trim, sensor calibration, engine condition, sea margins and reporting errors. Hull cleaning decisions require technical and economic validation.
