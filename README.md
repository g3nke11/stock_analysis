# Stock Analysis

## Overview

What if you could correctly predict stock market trends 30 days from now? How do you predict this?

This is the question this project strives to answer. Using data from previous stock market records, we created a program that reads this data and outputs a 30 day prediction chart for a given stock based on the anylized data.

We pulled our data for our program from [Kaggle.com](https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset/data). The data we pulled is organised in the Dataset directory as follows:

* symbols_valid_meta.csv (a file containing every stock and ETF name with their assosiated symbols)
* stocks (a directory containing a csv file for each companies' stock history)
* etfs (a directory containing a csv file for each companies' ETF history)

This dataset was anylized by "market_trends.py" to create "market_trend_dataset.csv," a file containing the average of all stocks for each day. The new csv file was used by "model.py" to test code that generates a liniar regression model for our data. This code was then used by "stock.py" to predict stock market trends for a given company that is selected by typing it's NASDAQ symbol into the terminal.

## Data Analysis Results

We focused on answering the following questions:

1) How do you Train a Model using multiple files of data?

    * We solved this by writing a file that reads multiple csv files and outputs a single csv file containing averages of all the csv files put into it.

2) How does a Linear Regression Model work?

    * A linear regression model works by analysing patterns in data to make future predictions. Given a dataset, the data is split into two different sets: the training set, and the test set. The data is split based off off a factor of randomness. The training set is used to model patterns in the data so it can make future predictions. It does this by predicting outcomes and comparing its results to the test set. In other words, the test set helps the training set catch on to current patterns so it can predict patterns for the future.
    * In this program, we used the LinearRegression class and the train_test_split function from the sklearn module to train and test our data.

## Development Environment

This project was programmed in VS Code using the Python language. We used the following Python modules:

* pandas (used for processing csv files)
* numpy (used for converting and processing data)
* lets_plot (used for displaying results)
* sklearn (used for the following)
  * LinearRegression (a class that models Linear Regression)
  * train_test_split (a function that splits the data for training)

## Useful Websites

These websites wer of most help to us during our project:

* [Pandas.pydata.org](https://pandas.pydata.org/docs/user_guide/index.html)
* [Scikit-learn.org](https://scikit-learn.org/stable/user_guide.html)

## Future Work

Going forward, we could improve this project by doing the folling:

* Creating a way to display multiple stocks at once for comparison
* Find a way to test the accuracy of our prediction to improve the accuracy of our linear regression model
* Encapsulating our code into functions and classes to make it more usable in the future
