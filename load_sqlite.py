import sqlite3
from pathlib import Path
import pandas as pd
p = Path(__file__).resolve().parent
with sqlite3.connect(p / 'fleet_performance.db') as conn:
    pd.read_csv(p / 'noon_reports_synthetic.csv').to_sql('noon_reports', conn, if_exists='replace', index=False)
print('Created fleet_performance.db')
