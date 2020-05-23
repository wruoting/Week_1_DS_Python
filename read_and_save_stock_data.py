# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:37:29 2018

@author: epinsky
Changelog:
    Updated by rwang on 5/21/2020
"""
# run this  !pip install pandas_datareader
import pandas_datareader.data as web
import os
import pandas as pd


def get_stock(ticker, start_date, end_date, s_window, l_window):
    try:
        df = web.DataReader(ticker, start=start_date, end=end_date, data_source='yahoo')
        df['Return'] = df['Adj Close'].pct_change()
        df['Return'].fillna(0, inplace = True)
        df['Date'] = df.index
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year 
        df['Day'] = df['Date'].dt.day
        for col in ['Open', 'High', 'Low', 'Close', 'Adj Close']:
            df[col] = df[col].round(2)
        df['Weekday'] = df['Date'].dt.day_name()
        df['Week_Number'] = df['Date'].dt.strftime('%U')
        df['Year_Week'] = df['Date'].dt.strftime('%Y-%U')
        df['Short_MA'] = df['Adj Close'].rolling(window=s_window, min_periods=1).mean()
        df['Long_MA'] = df['Adj Close'].rolling(window=l_window, min_periods=1).mean()        
        col_list = ['Date', 'Year', 'Month', 'Day', 'Weekday', 
                    'Week_Number', 'Year_Week', 'Open', 
                    'High', 'Low', 'Close', 'Volume', 'Adj Close',
                    'Return', 'Short_MA', 'Long_MA']
        num_lines = len(df)
        df = df[col_list]
        print('read ', num_lines, ' lines of data for ticker: ' , ticker)
        return df
    except Exception as error:
        print(error)
        return None

try:
    ticker = 'WMT'
    df = get_stock(ticker, start_date='2014-01-01', end_date='2019-12-31', s_window=14, l_window=50)
    df.to_csv('./{}.csv'.format(ticker), index=False)
    print('wrote ' + str(len(df)) + ' lines to file: ./{}.csv'.format(ticker))
except Exception as e:
    print(e)
    print('failed to get Yahoo stock data for ticker: ', ticker)

