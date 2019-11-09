import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
import util as ut

def bollinger(price):

    cols = price.columns.tolist()
    #print cols
    price_df = price[cols[0]]
    #print price_df
    price_df = price_df/price_df[0]
    #print price_df
    rolling_mean = price_df.rolling(20,center = False).mean()
    rolling_stdev = price_df.rolling(20, center = False).std()

    upper = rolling_mean+2*rolling_stdev
    lower = rolling_mean-2*rolling_stdev
    bb_val = (price_df - lower) / (upper-lower)
    # plt.xlabel("Date")
    # plt.ylabel("Price(Normalized)")
    #
    # plt.plot(price_df)
    # plt.plot(rolling_mean)
    # plt.plot(rolling_mean+2*rolling_stdev)
    # plt.plot(rolling_mean-2*rolling_stdev)
    # plt.legend(["Price", "Rolling Mean", "Upper Band", "Lower Band"])
    # plt.savefig("2")
    #
    # plt.show()
    return upper,lower,bb_val,rolling_mean,rolling_stdev

def sma(prices,window):
    cols = prices.columns.tolist()
    #print cols
    price_df = prices[cols[0]]
    price_df = price_df/price_df[0]
    rolling_mean = price_df.rolling(window,center=False).mean()
    final = price_df.divide(rolling_mean,axis='index')
    final = final

    # plt.clf()
    # plt.xlabel("Date")
    # plt.ylabel("Price(Normalized)")
    #
    # plt.plot(price_df)
    # plt.plot(rolling_mean)
    # plt.legend(["Prices","Rolling Mean"])
    # plt.savefig("1")
    # plt.show()
    return final

def momentum(prices):
    cols = prices.columns.tolist()
    #print cols
    price_df = prices[cols[0]]
    price_df = price_df / price_df[0]
    final = price_df/price_df.shift(19)-1

    # plt.clf()
    # plt.xlabel("Date")
    # plt.ylabel("Price(Normalized)")
    #
    # plt.plot(final)
    # plt.plot(price_df)
    # plt.legend(["Momentum", "Rolling Mean"])
    # plt.savefig("3")
    # plt.show()
    return final


def calc_indicators():

    insample_start = dt.datetime(2008, 1, 1)
    insample_end = dt.datetime(2009, 12, 31)
    symbol = 'JPM'
    dates = pd.date_range(insample_start,insample_end)
    prices = ut.get_data([symbol],dates)
    bollinger(prices)
    sma(prices,20)
    momentum(prices)



if __name__ == "__main__":
    calc_indicators()