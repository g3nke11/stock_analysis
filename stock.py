#########
# Owner: Luke
# Editors: Andrew, Luke
#
#########
#%%
# Imports
from lets_plot import *
import pandas as pd
import plotly_express as px
import numpy as np
from lets_plot import *

LetsPlot.setup_html(isolated_frame=True)

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LinearRegression

LetsPlot.setup_html(isolated_frame=True)

# Reading the Data
stock_managing_data = pd.read_csv("Dataset/symbols_valid_meta.csv")

# Removing columns for easier organization (I may change which columns later but this should work for now)
stock_managing_data = stock_managing_data.drop(columns=['Nasdaq Traded','Listing Exchange','Market Category','Round Lot Size','Test Issue','Financial Status','CQS Symbol','Symbol','NextShares'])

# Seperates the ETF column into 2 columns. ETF_N and ETF_Y 
stock_managing_data = pd.get_dummies(stock_managing_data, columns=["ETF"])


# The data looks like this: print(stock_managing_data.head(3))
#                              Security Name NASDAQ Symbol  ETF_N  ETF_Y
# 0  Agilent Technologies, Inc. Common Stock             A   True  False
# 1          Alcoa Corporation Common Stock             AA   True  False
# 2             Perth Mint Physical Gold ETF          AAAU  False   True

# Using the list of names it reads the data on each csv file using the symbol 
for row in range(len(stock_managing_data)):
    symbol = stock_managing_data["NASDAQ Symbol"][row]

    # PRN.csv is not a valid name. We will need a better work around later. I renamed the file to include a 1. Its hardcoded...
    if symbol == "PRN":
        symbol = "PRN1"

    if stock_managing_data["ETF_N"][row] == True:
        data = pd.read_csv(f"Dataset/stocks/{symbol}.csv")
    else:
        data = pd.read_csv(f"Dataset/etfs/{symbol}.csv")


#%%
# UI
print("\nStock Analysis")
print("--------------\n")


while True:
    user_input = input("Enter a NASDAQ Symbol (type \"exit\" to close): ").upper()
    if user_input.upper() == "EXIT":
        break
    if user_input in stock_managing_data["NASDAQ Symbol"].to_numpy():

        # Read Company Data
        company_info = []
        for c in stock_managing_data.to_numpy():
            if c[1] == user_input:
                company_info = c
                break
        if company_info[3]:
            print(f"\"{user_input}\" - NASDAQ Symbol belongs to an ETF. PLease choose a different symbol")
        else:
            selected_stock = pd.read_csv(f"Dataset/stocks/{user_input}.csv")
            # Display Company Data
            print(f"\n{company_info[0]} ({company_info[1]})\n")
            print("Stock History")
            print(selected_stock)

            # Display chart
            selected_stocks = selected_stock.query('Date >= "2000-01-01" and Date <= "2020-12-31"')
            fig = px.line(
                selected_stocks,
                x='Date',
                y='Open',
                title='The Companies opening trend.'
            )
            fig.update_layout(
                xaxis_title = 'Dates between Jan 2000 & Dec 2020',
                yaxis_title = 'Opening price between Jan 2000 & Dec 2020',
                title_font_size = 25
            )
            fig.show()
            fig2 = px.line(
                selected_stocks,
                x='Date',
                y='Close',
                title='The Compnies closing trends'
            )
            fig2.update_layout(
                xaxis_title = 'Dates between Jan 2000 & Dec 2020',
                yaxis_title = 'Closing price between Jan 2000 & Dec 2020',
                title_font_size = 25
            )
            fig2.show()
            model = LinearRegression()

            # Running tests to learn the model. Will explain when I actually understand. Working with rows are weird
            test_data = pd.read_csv(f"Dataset/stocks/{user_input}.csv")
            # Not doing what I would like. With a closer look at the data its saying the next day, not past day.
            test_data['Previous_Close'] = test_data['Close'].shift(1)

            test_data = test_data.dropna()

            test_data = test_data[test_data['Date'] >= '2019-01-01']
            # test_data = test_data.drop(columns=['Date'], axis=1)

            last_day = test_data[['Previous_Close']]
            target = test_data['Close']

            # print(test_data)

            X_train, X_test, y_train, y_test = train_test_split(last_day, target, test_size=0.2, random_state=42)

            model.fit(X_train,y_train)

            y_pred = model.predict(X_test)
            # print(y_pred)

            last_close = test_data['Close'].iloc[-1]
            # tomorrow_prediction = model.predict([[last_close]])
            # print(f"Tomorrow's Predicted Closing Price: {tomorrow_prediction[0]}")

            future_predictions = []

            # Predict the next 30 days
            for _ in range(30):
                # Use the last predicted value (or initial last_close for the first prediction)
                next_close = model.predict(np.array([[last_close]]))[0]
                future_predictions.append(next_close)
                
                # Update the last_close with the predicted value for the next iteration
                last_close = next_close

            # Create a DataFrame for future predictions
            future_df = pd.DataFrame({
                'Date': range(1, 31),
                'Predicted_Close': future_predictions
            })
            future_df2 = px.histogram(
                future_df,
                x='Date',
                title='30 day prediction for the company.'
            )
            future_df2.update_layout(
                bargap=0.2
            )
            future_df2.show()

    else:
        print(f"\"{user_input}\" - NASDAQ Symbol not found")
# %%
