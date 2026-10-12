-- SQLite queries; run after load_sqlite.py
-- 1. Overall daily fuel performance
SELECT vessel_id, COUNT(*) AS reports,
       ROUND(AVG(fuel_tonnes_day),2) AS avg_fuel_t_day,
       ROUND(SUM(fuel_tonnes_day),2) AS total_fuel_t
FROM noon_reports GROUP BY vessel_id;

-- 2. Highest fuel-consumption days (not necessarily inefficiency)
SELECT report_date, speed_knots, wind_knots, wave_height_m, fuel_tonnes_day
FROM noon_reports ORDER BY fuel_tonnes_day DESC LIMIT 10;

-- 3. Compare performance at similar speeds and moderate weather
SELECT CASE WHEN speed_knots < 12 THEN 'below 12'
            WHEN speed_knots < 14 THEN '12-14'
            ELSE '14+' END AS speed_band,
       COUNT(*) AS reports,
       ROUND(AVG(fuel_tonnes_day),2) AS avg_fuel_t_day
FROM noon_reports WHERE wind_knots < 12 AND wave_height_m < 2
GROUP BY speed_band ORDER BY speed_band;

-- 4. Rolling 7-report fuel average (not necessarily seven calendar days)
SELECT report_date, fuel_tonnes_day,
       ROUND(AVG(fuel_tonnes_day) OVER (
         PARTITION BY vessel_id ORDER BY report_date
         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW),2) AS moving_avg_t_day
FROM noon_reports ORDER BY report_date;

-- 5. Normalized consumption per nautical mile
SELECT report_date, ROUND(fuel_tonnes_day / NULLIF(distance_nm,0),4) AS tonnes_per_nm
FROM noon_reports ORDER BY tonnes_per_nm DESC LIMIT 10;


-- 6. Fuel consumption deviation from clean/calm baseline
SELECT
    report_date,
    vessel_id,
    ROUND(speed_knots, 2) AS speed_knots,
    ROUND(fuel_tonnes_day, 2) AS observed_fuel,
    ROUND(clean_calm_baseline_tonnes_day, 2)
        AS expected_fuel,
    ROUND(
        (
            fuel_tonnes_day -
            clean_calm_baseline_tonnes_day
        ) * 100.0 /
        NULLIF(clean_calm_baseline_tonnes_day, 0),
        2
    ) AS deviation_pct
FROM noon_reports
ORDER BY deviation_pct DESC
LIMIT 10;

-- 7. Aggregate excess fuel above clean/calm baseline
SELECT
    vessel_id,
    COUNT(*) AS total_reports,
    ROUND(
        SUM(fuel_tonnes_day), 2
    ) AS observed_fuel_sum,
    ROUND(
        SUM(clean_calm_baseline_tonnes_day), 2
    ) AS baseline_fuel_sum,
    ROUND(
        SUM(
            fuel_tonnes_day -
            clean_calm_baseline_tonnes_day
        ), 2
    ) AS net_difference_tonnes,
    ROUND(
        100.0 *
        SUM(
            fuel_tonnes_day -
            clean_calm_baseline_tonnes_day
        ) /
        NULLIF(
            SUM(clean_calm_baseline_tonnes_day), 0
        ),
        2
    ) AS overall_deviation_pct
FROM noon_reports
GROUP BY vessel_id;