"""MC2-P1: Market simulator.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Manan Mehta (replace with your name)
GT User ID: mmehta64 (replace with your User ID)
GT ID: 903390740 (replace with your GT ID)
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data

def author():
    return "mmehta64"
def compute_portvals(orders_df, start_val , commission, impact):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months


    start_date=dt.datetime(2008, 1, 1)
    end_date=dt.datetime(2009, 12, 31)
    syms = ['JPM']
    #print(start_date)
    print(orders_df)

    portvals = get_data(syms, pd.date_range(start_date, end_date))

    portvals = portvals.fillna(method='ffill')
    portvals = portvals.fillna(method='bfill')




    rows=portvals.shape[0]
    portvals['Cash']=np.ones(shape=(rows,1))
    portvals.drop('SPY',1,inplace=True)
    #print portvals
    trades = portvals.copy()
    for index,rows in trades.iterrows():
        rows['Cash']=0
        rows['JPM']=0

    #print orders_df
    for index,rows in orders_df.iterrows():
        if rows['JPM']>0:
            val = portvals.at[index, 'JPM']
            #print(portvals.at[index, s])
            trades.at[index,'JPM']+=rows['JPM']
            trades.at[index,'Cash']-=((val*rows['JPM']*1)*(1+impact))
        else:
            val = portvals.at[index, 'JPM']
            trades.at[index, 'JPM'] += 1*rows['JPM']
            trades.at[index, 'Cash'] += ((val * rows['JPM']*-1)*(1-impact))


        #print(index, trades.at[index, 'GOOG'])
        trades.at[index, 'Cash'] -= commission





    #print trades
    holdings = trades.copy()
    for index, rows in holdings.iterrows():
        rows['Cash'] = 0
        rows['JPM']=0

    start_date = trades.index[0]
    holdings.at[start_date,'Cash']=start_val
    prev_index=start_date
    for index,rows in trades.iterrows():

        if index == start_date:

            holdings.at[index, 'JPM']+=rows['JPM']

        else:
            holdings.at[index,'JPM']=holdings.at[prev_index,'JPM']+trades.at[index,'JPM']

        if index==start_date:
            holdings.at[index, 'Cash'] += rows['Cash']
        else:
            holdings.at[index,'Cash'] = rows['Cash']+holdings.at[prev_index,'Cash']
        prev_index = index

    #print holdings
    values = holdings.copy()
    values = values*portvals

    #print(values)
    final_val = values.sum(axis=1)

    #print(final_val)
    #portvals = portvals[['AAPL']]  # remove SPY
    #rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix())
    #print(rv)
    return final_val
    #return rv
    #return portvals
def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-01.csv"
    sv = 1000000

    # Process orders
    # portvals = compute_portvals(, start_val = sv)
    # if isinstance(portvals, pd.DataFrame):
    #     portvals = portvals[portvals.columns[0]] # just get the first column
    # else:
    #     "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    #print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
