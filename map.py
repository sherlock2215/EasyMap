import pandas as pd

# Read first CSV
df1 = pd.read_csv("stations1.csv")
# Read second CSV
df2 = pd.read_csv("stations2.csv")

# Combine them into one DataFrame
data = pd.concat([df1, df2], ignore_index=True)

# Clean column names
data.columns = [col.strip() for col in data.columns]

# Convert timestamp to datetime
data['date'] = data['MESS_DATUM'].astype(str).str[:8]
data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')

# Compute daily average temperature per station
daily_avg = data.groupby(['STATIONS_ID', 'date'])['TT_TER'].mean().reset_index()

print(daily_avg.head())
