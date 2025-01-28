#########
# Owner: Kelson
# Editors: Glen
#
#########

# Imports
import pandas as pd
# import datetime as dt

stock_managing_data = pd.read_csv("Dataset/symbols_valid_meta.csv")

# Removing columns for easier organization (I may change which columns later but this should work for now)
stock_managing_data = stock_managing_data.drop(columns=['Nasdaq Traded','Listing Exchange','Market Category','Round Lot Size','Test Issue','Financial Status','CQS Symbol','Symbol','NextShares'])

aggregated_data = {}

class RunningStats:
    def __init__(self):
        self.n = 0          # Count of numbers
        self.mean = 0.0     # Current mean
        self.M2 = 0.0       # Sum of squares of differences from the mean

    def update(self, x):
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        delta2 = x - self.mean
        self.M2 += delta * delta2

    def variance(self):
        if self.n < 2:
            return float('nan')  # Variance is undefined for n < 2
        return self.M2 / (self.n - 1)

    def std_dev(self):
        return self.variance() ** 0.5


for row in range(len(stock_managing_data)):
    symbol = stock_managing_data["NASDAQ Symbol"][row]
    print(symbol)

    # PRN.csv is not a valid name. We will need a better work around later. I renamed the file to include a 1. Its hardcoded...
    if symbol == "PRN":
        symbol = "PRN1"

    if stock_managing_data["ETF"][row] == 'N':
        data = pd.read_csv(f"Dataset/stocks/{symbol}.csv")

        data['Date'] = pd.to_datetime(data['Date'])
        data = data[data['Date'] >= '2000-01-01']

        for row_index in range(len(data)):
            date = data.iloc[row_index]['Date']

            open_value = float(data.iloc[row_index]['Open'])
            high_value = float(data.iloc[row_index]['High'])
            low_value = float(data.iloc[row_index]['Low'])
            close_value = float(data.iloc[row_index]['Close'])
            adj_close_value = float(data.iloc[row_index]['Adj Close'])
            volume_value = float(data.iloc[row_index]['Volume'])

            if date in aggregated_data:

                aggregated_data[date]['Std_Open'].update(open_value)
                aggregated_data[date]['Std_High'].update(high_value)
                aggregated_data[date]['Std_Low'].update(low_value)
                aggregated_data[date]['Std_Close'].update(close_value)
                aggregated_data[date]['Std_Adj Close'].update(adj_close_value)
                aggregated_data[date]['Std_Volume'].update(volume_value)
                aggregated_data[date]['Deviations'] += 1

                num_std_dev = 2 

                if (abs(open_value - aggregated_data[date]['Std_Open'].mean) <= num_std_dev * aggregated_data[date]['Std_Open'].std_dev() and
        abs(high_value - aggregated_data[date]['Std_High'].mean) <= num_std_dev * aggregated_data[date]['Std_High'].std_dev() and
        abs(low_value - aggregated_data[date]['Std_Low'].mean) <= num_std_dev * aggregated_data[date]['Std_Low'].std_dev() and
        abs(close_value - aggregated_data[date]['Std_Close'].mean) <= num_std_dev * aggregated_data[date]['Std_Close'].std_dev() and
        abs(adj_close_value - aggregated_data[date]['Std_Adj Close'].mean) <= num_std_dev * aggregated_data[date]['Std_Adj Close'].std_dev() and
        abs(volume_value - aggregated_data[date]['Std_Volume'].mean) <= num_std_dev * aggregated_data[date]['Std_Volume'].std_dev()):


                    aggregated_data[date]['Open'] += open_value
                    aggregated_data[date]['High'] += high_value
                    aggregated_data[date]['Low'] += low_value
                    aggregated_data[date]['Close'] += close_value
                    aggregated_data[date]['Adj Close'] += adj_close_value
                    aggregated_data[date]['Volume'] += volume_value
                    aggregated_data[date]['Count'] += 1.0


            else:
                aggregated_data[date] = {
                    'Open' : open_value,
                    'High' : high_value,
                    'Low' : low_value,
                    'Close' : close_value,
                    'Adj Close' : adj_close_value,
                    'Volume' : volume_value,
                    'Count' : 1.0,
                    "Deviations" : 0,
                    'Std_Open' : RunningStats(),
                    'Std_High' : RunningStats(),
                    'Std_Low' : RunningStats(),
                    'Std_Close' : RunningStats(),
                    'Std_Adj Close' : RunningStats(),
                    'Std_Volume' : RunningStats(),
                }
    else:
        data = pd.read_csv(f"Dataset/etfs/{symbol}.csv")

        data['Date'] = pd.to_datetime(data['Date'])
        data = data[data['Date'] >= '2000-01-01']

        for row_index in range(len(data)):
            date = data.iloc[row_index]['Date']

            open_value = float(data.iloc[row_index]['Open'])
            high_value = float(data.iloc[row_index]['High'])
            low_value = float(data.iloc[row_index]['Low'])
            close_value = float(data.iloc[row_index]['Close'])
            adj_close_value = float(data.iloc[row_index]['Adj Close'])
            volume_value = float(data.iloc[row_index]['Volume'])

            if date in aggregated_data:

                aggregated_data[date]['Std_Open'].update(open_value)
                aggregated_data[date]['Std_High'].update(high_value)
                aggregated_data[date]['Std_Low'].update(low_value)
                aggregated_data[date]['Std_Close'].update(close_value)
                aggregated_data[date]['Std_Adj Close'].update(adj_close_value)
                aggregated_data[date]['Std_Volume'].update(volume_value)
                aggregated_data[date]['Deviations'] += 1

                num_std_dev = 2 

                if (abs(open_value - aggregated_data[date]['Std_Open'].mean) <= num_std_dev * aggregated_data[date]['Std_Open'].std_dev() and
        abs(high_value - aggregated_data[date]['Std_High'].mean) <= num_std_dev * aggregated_data[date]['Std_High'].std_dev() and
        abs(low_value - aggregated_data[date]['Std_Low'].mean) <= num_std_dev * aggregated_data[date]['Std_Low'].std_dev() and
        abs(close_value - aggregated_data[date]['Std_Close'].mean) <= num_std_dev * aggregated_data[date]['Std_Close'].std_dev() and
        abs(adj_close_value - aggregated_data[date]['Std_Adj Close'].mean) <= num_std_dev * aggregated_data[date]['Std_Adj Close'].std_dev() and
        abs(volume_value - aggregated_data[date]['Std_Volume'].mean) <= num_std_dev * aggregated_data[date]['Std_Volume'].std_dev()):


                    aggregated_data[date]['Open'] += open_value
                    aggregated_data[date]['High'] += high_value
                    aggregated_data[date]['Low'] += low_value
                    aggregated_data[date]['Close'] += close_value
                    aggregated_data[date]['Adj Close'] += adj_close_value
                    aggregated_data[date]['Volume'] += volume_value
                    aggregated_data[date]['Count'] += 1.0


            else:
                aggregated_data[date] = {
                    'Open' : open_value,
                    'High' : high_value,
                    'Low' : low_value,
                    'Close' : close_value,
                    'Adj Close' : adj_close_value,
                    'Volume' : volume_value,
                    'Count' : 1.0,
                    "Deviations" : 0,
                    'Std_Open' : RunningStats(),
                    'Std_High' : RunningStats(),
                    'Std_Low' : RunningStats(),
                    'Std_Close' : RunningStats(),
                    'Std_Adj Close' : RunningStats(),
                    'Std_Volume' : RunningStats(),
                }


rows = []

for date, values in aggregated_data.items():
    row = {
        'Date': date,
        'Open': values['Open'] / values['Count'],
        'High': values['High'] / values['Count'],
        'Low': values['Low'] / values['Count'],
        'Close': values['Close'] / values['Count'],
        'Adj Close': values['Adj Close'] / values['Count'],
        'Volume': values['Volume'] / values['Count']
    }
    rows.append(row)

market_trend_dataset = pd.DataFrame(rows)

market_trend_dataset['Date'] = pd.to_datetime(market_trend_dataset['Date'])
market_trend_dataset = market_trend_dataset.sort_values(by='Date').reset_index(drop=True)

market_trend_dataset.dropna(inplace=True)


market_trend_dataset.to_csv('market_trend_dataset.csv', index=False, header=True)

print("It is Finished")
