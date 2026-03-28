import numpy as np
import pandas as pd
from datetime import timedelta, datetime

# Set random seed for reproducibility
np.random.seed(42)

# Constants
days = 365
start_date = datetime(2025, 1, 1)
date_list = [start_date + timedelta(days=i) for i in range(days)]

# Generate dates
dates = pd.date_range(start='2025-01-01', periods=365)

# Generate data based on requirements
steps = np.random.normal(loc=8500, scale=2500, size=365).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1, size=365).clip(4.5, 9.5)
heart_rate = np.random.normal(loc=68, scale=10, size=365).clip(48, 110)
calories_burned = np.random.uniform(low=1800, high=4200, size=365)
active_minutes = np.random.uniform(low=20, high=180, size=365)

# Create DataFrame
data = pd.DataFrame({
    'Date': dates,
    'Steps': steps,
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_bpm': heart_rate,
    'Calories_Burned': calories_burned,
    'Active_Minutes': active_minutes
})

# Introduce 5% missing values (NaN)
for column in data.columns[1:]:  # Skip the 'Date' column
    data.loc[data.sample(frac=0.05).index, column] = np.nan

# Save to CSV
data.to_csv('data/health_data.csv', index=False)