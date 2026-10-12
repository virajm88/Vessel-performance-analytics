"""Synthetic educational vessel performance model, not real fleet data."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(42)
n = 90
speed = np.clip(rng.normal(13.5, 0.85, n), 10.5, 15.5)
draft = np.clip(rng.normal(15.0, 0.65, n), 13.5, 16.5)
wind = np.clip(rng.gamma(2.5, 3.0, n), 0, 25)
wave = np.clip(rng.gamma(2, 0.7, n), 0, 4.5)
day = np.arange(n)
hull_factor = 1 + 0.00075 * day
weather_factor = 1 + 0.004 * wind + 0.015 * wave
base_kw = 8000 * (speed / 14) ** 3 * (1 + 0.025 * (draft - 15))
actual_kw = base_kw * weather_factor * hull_factor * rng.normal(1, 0.012, n)
sfoc_g_kwh = 175
aux_t_day = 2.0
baseline_fuel = base_kw * sfoc_g_kwh * 24 / 1e6 + aux_t_day
actual_fuel = actual_kw * sfoc_g_kwh * 24 / 1e6 + aux_t_day

df = pd.DataFrame({
    'report_date': pd.date_range('2026-01-01', periods=n),
    'vessel_id': 'CAPESIZE_SIM_01',
    'speed_knots': np.round(speed, 2),
    'draft_m': np.round(draft, 2),
    'wind_knots': np.round(wind, 2),
    'wave_height_m': np.round(wave, 2),
    'distance_nm': np.round(speed * 24, 2),
    'shaft_power_kw': np.round(actual_kw, 1),
    'fuel_tonnes_day': np.round(actual_fuel, 3),
    'clean_calm_baseline_tonnes_day': np.round(baseline_fuel, 3),
})
df.to_csv(OUT / 'noon_reports_synthetic.csv', index=False)
# Weather-normalized expected fuel; residual drift is partly attributable to the *simulated* hull factor.
weather_expected = base_kw * weather_factor * sfoc_g_kwh * 24 / 1e6 + aux_t_day
df['weather_adjusted_expected_tonnes_day'] = np.round(weather_expected, 3)
df['fuel_deviation_pct'] = np.round((actual_fuel / weather_expected - 1) * 100, 2)
df['fuel_tonnes_per_nm'] = np.round(actual_fuel / (speed * 24), 4)
df.to_csv(OUT / 'performance_analysis.csv', index=False)

s = np.linspace(10, 16, 100)
p = 8000 * (s / 14) ** 3
plt.figure(figsize=(8, 5))
plt.plot(s, p, label='Clean calm-water baseline (15 m draft)')
plt.xlabel('Speed (knots)'); plt.ylabel('Estimated shaft power (kW)')
plt.title('Illustrative speed-power relationship'); plt.grid(alpha=.25); plt.legend()
plt.tight_layout(); plt.savefig(OUT / 'speed_power.png', dpi=170); plt.close()
plt.figure(figsize=(8, 5))
plt.scatter(df['report_date'], df['fuel_deviation_pct'], s=13, label='Daily deviation')
plt.plot(df['report_date'], df['fuel_deviation_pct'].rolling(10, min_periods=3).mean(), label='10-report rolling mean')
plt.xlabel('Report date'); plt.ylabel('Deviation from weather-adjusted baseline (%)')
plt.title('Simulated performance deterioration'); plt.grid(alpha=.25); plt.legend()
plt.xticks(rotation=25); plt.tight_layout(); plt.savefig(OUT / 'daily_deviation.png', dpi=170); plt.close()

first = df.iloc[:15]['fuel_deviation_pct'].mean()
last = df.iloc[-15:]['fuel_deviation_pct'].mean()
report = (f'SYNTHETIC EDUCATIONAL DATA - NOT REAL VESSEL MEASUREMENTS\n'
          f'Number of reports: {len(df)}\n'
          f'Average observed fuel: {df.fuel_tonnes_day.mean():.2f} t/day\n'
          f'Average deviation, first 15 days: {first:.2f}%\n'
          f'Average deviation, last 15 days: {last:.2f}%\n'
          f'Deviation change: {last-first:.2f} percentage points\n'
          'Interpretation: simulated hull deterioration drives part of the increase.\n'
          'This model is not sufficient to recommend real-world hull cleaning.\n')
(OUT / 'summary.txt').write_text(report)
print(report)


# Illustrative fuel-saving scenario

baseline_fuel = 35.0
performance_deviation = 0.056
fuel_price = 600.0
operating_days = 30
potential_fuel_savings = (
    baseline_fuel * performance_deviation
)
daily_cost_savings = (
    potential_fuel_savings * fuel_price
)
period_cost_savings = (
    daily_cost_savings * operating_days
)
print("Potential fuel savings:",
      round(potential_fuel_savings, 2), "t/day")
print("Daily gross savings: $",
      round(daily_cost_savings, 2))
print("30-day gross savings: $",
      round(period_cost_savings, 2))