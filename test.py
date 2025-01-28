import pandas as pd

# Example DataFrame
data1 = pd.DataFrame({
    'Date': ['1999-12-31', '2000-01-01', '2000-01-01'],
    'Open': [10, 20, 30],
    'High': [10, 20, 30],
    'Low': [10, 20, 30],
    'Close': [10, 20, 30],
    'Adj Close': [10, 20, 30],
    'Volume': [10, 20, 30]
})

# Ensure 'Date' column is in datetime format
data1['Date'] = pd.to_datetime(data1['Date'])

# Filter rows where the year is 2000 or later
data = data1[data1['Date'].dt.year >= 2000]

aggregated_data = {}

for row_index in range(len(data)):
    date = data.at[row_index,'Date']
    if date in aggregated_data:
        aggregated_data[date]['Open'] += data.at[row_index,'Open'],
        aggregated_data[date]['High'] += data.at[row_index,'High'],
        aggregated_data[date]['Low'] += data.at[row_index,'Low'],
        aggregated_data[date]['Close'] += data.at[row_index,'Close'],
        aggregated_data[date]['Adj Close'] += data.at[row_index,'Adj Close'],
        aggregated_data[date]['Volume'] += data.at[row_index,'Volume'],
        aggregated_data[date]['Count'] += 1
    else:
        aggregated_data[date] = {
            'Open' : data.at[row_index,'Open'],
            'High' : data.at[row_index,'High'],
            'Low' : data.at[row_index,'Low'],
            'Close' : data.at[row_index,'Close'],
            'Adj Close' : data.at[row_index,'Adj Close'],
            'Volume' : data.at[row_index,'Volume'],
            'Count' : 1
        }

print(data)
