# -*- coding: utf-8 -*-
"""
@author: rwang
"""
import os
import numpy as np
import datetime as dt
from numpy import genfromtxt
import matplotlib.pyplot as plt
from assignment_1_wang_wmt_q1_q2 import average_profit_per_trade
from collections import deque

ticker='WMT'

def main():
    try:
        # Create ticker data   
        ticker_data = genfromtxt('./{}.csv'.format(ticker), delimiter=',', dtype=str)
        # Question 3
        x_data = np.arange(0, 10.01, 0.1)
        y_data = deque()
        print('Plotting over 100 points for threshold, please hold as this takes a few seconds')
        for threshold in x_data:
            y_data.append(average_profit_per_trade(ticker_data, threshold=threshold))
        y_data = np.array(y_data)
        plt.plot(x_data, y_data, label='P/L vs. Threshold to trade')
        plt.legend()
        plt.xlabel('Threshold for Trading (%)')
        plt.ylabel('Average Profit per day ($)')
        plt.savefig('Threshold Trading Question 3_{}'.format(ticker))
        plt.show()

    except Exception as e:
        print('Failed to read stock data for ticker: {} with exception: {}'.format(ticker, e))


if __name__ == "__main__":
    main()
