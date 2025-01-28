#########
# Owner: Glen Kelley
# Editors: Kelson Gneiting
#
#########

import pandas as pd 
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

# Initializing the model 
model = LinearRegression()

# Running tests to learn the model. Will explain when I actually understand. Working with rows are weird
test_data = pd.read_csv("market_trend_dataset.csv")
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
    'Day': range(1, 31),
    'Predicted_Close': future_predictions
})

# print(future_df)
(
ggplot(future_df, aes(x='Day', y='Predicted_Close'))
+ geom_line()
)