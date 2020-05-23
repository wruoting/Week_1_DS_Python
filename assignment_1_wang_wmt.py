# -*- coding: utf-8 -*-
"""
@author: rwang
"""
import os
import numpy as np
import datetime as dt
from numpy import genfromtxt

ticker='WMT'

def process_adj_open(row, previous_row):
    # Subtract next open from adj_close
    open_current_day = row[7].astype(np.float32)
    adj_close = previous_row[12].astype(np.float32)
    return np.subtract(open_current_day, adj_close)

def open_to_close(open, adj_close, strat='long', money=100):
    # Round number of shares to two decimal places
    number_of_shares = np.around(np.divide(money, open), 2)
    # Round profit and loss to two places
    pnl = np.around(np.multiply(number_of_shares, adj_close), 2)
    # Round to two places for our total
    if strat == 'long':
        # Spend money at the beginning, make it back in number of shares x adj_close
        return np.round(np.add(np.negative(money), pnl), 2), number_of_shares
    if strat == 'short':
        # Receive money at the beginning from selling short, spend it to buy shares at end of day shares x adj_close
        return np.round(np.add(money, np.negative(pnl)), 2), number_of_shares
    else:
        raise "Strat not defined"

def pnl_per_share(profit, shares):
    # Round pnl per share to 2 places
    return np.round(np.divide(profit, shares), 2)

# Returns profit from close to open given a row
def open_to_close_rows(row, strat='long', money=100):
    # Subtract adj_close from open (not adj close)
    adj_close = row[12].astype(np.float32)
    open_current_day = row[7].astype(np.float32)
    return open_to_close(open_current_day, adj_close, strat=strat, money=money)

def main():
    # try:
    # Create ticker data   
    ticker_data = genfromtxt('./{}.csv'.format(ticker), delimiter=',', dtype=str)
    trading_strategy_1 = np.array([])
    trading_strategy_1_per_share = np.array([])
    trading_strategy_2 = np.array([])
    trading_strategy_2_per_share = np.array([])

    for index, row in enumerate(ticker_data):
        if (index > 1 and index != np.size(ticker_data, axis=0)-1):
            # Trading Strategy Long
            if(process_adj_open(row, ticker_data[index-1]) > 0):
                profit, number_of_shares = open_to_close_rows(ticker_data[index], strat='long')
                pnl_share = pnl_per_share(profit, number_of_shares)
                trading_strategy_1 = np.append(trading_strategy_1, profit)
                trading_strategy_1_per_share = np.append(trading_strategy_1_per_share, pnl_share)
            # Trading Strategy Short
            if(process_adj_open(row, ticker_data[index-1]) < 0):
                profit, number_of_shares = open_to_close_rows(ticker_data[index], strat='short')
                pnl_share = pnl_per_share(profit, number_of_shares)
                trading_strategy_2 = np.append(trading_strategy_2, profit)
                trading_strategy_2_per_share = np.append(trading_strategy_2_per_share, pnl_share)
    # Question 1
    # Sum all the pnls and divide by number of days
    sum_pnl = np.add(np.sum(trading_strategy_1), np.sum(trading_strategy_2))
    sum_pnl_per_share = np.add(np.sum(trading_strategy_1_per_share), np.sum(trading_strategy_2_per_share))
    num_days = np.add(np.size(trading_strategy_1), np.size(trading_strategy_2))
    # Round to two decimal places
    average_pnl = np.round(np.divide(sum_pnl, num_days), 2)
    average_pnl_per_share = np.round(np.divide(sum_pnl_per_share, num_days), 2)

    # Question 2
    sum_pnl_long = np.sum(trading_strategy_1)
    sum_pnl_short = np.sum(trading_strategy_2)
    print('Daily Profit:')
    print('Longs: {}'.format(trading_strategy_1))
    print('Shorts: {}'.format(trading_strategy_2))
    print('Longs per share: {}'.format(trading_strategy_1_per_share))
    print('Shorts per share: {}'.format(trading_strategy_2_per_share))
    print('Question 1:')
    print('Average daily profit per share: {}'.format(average_pnl_per_share))
    print('Average daily profit: {}'.format(average_pnl))
    print('Question 2:')
    print('Long position profit: {}'.format(sum_pnl_long))
    print('Short position profit: {}'.format(sum_pnl_short))
    print('The short position profits are higher than the long position profits')
    print('Question 3:')
    


    # except Exception as e:
    #     print('Failed to read stock data for ticker: {} with exception: {}'.format(ticker, e))




if __name__ == "__main__":
    main()




