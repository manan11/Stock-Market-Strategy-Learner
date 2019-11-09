"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch

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

import datetime as dt
import pandas as pd
import util as ut
import BagLearner as bl
import RTLearner as rt
from indicators import sma, bollinger, momentum
import numpy as np
import random

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.Days = 10
        self.learner = bl.BagLearner(rt.RTLearner,kwargs = {"leaf_size":5},bags = 20,boost=False,verbose=False)

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        # add your code to do learning here

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        #if self.verbose: print prices
        #print prices

        # example use with new colname
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        if self.verbose: print volume
        #print volume

        S = sma(prices,20)
        upper, lower ,bb, r_m,r_std= bollinger(prices)
        M = momentum(prices)

        SMA = pd.DataFrame({'SMA':S})
        bb_val = pd.DataFrame({'Bollinger': bb})
        Upper = pd.DataFrame({'Upper':upper})
        Lower = pd.DataFrame({'Lower':lower})
        Momentum = pd.DataFrame({'Momentum': M})
        R_M =  pd.DataFrame({'Rolling Mean': r_m})
        R_STD = pd.DataFrame({"Rolling STD": r_std})
        ind = pd.concat((SMA,bb_val,Upper,Lower,R_M,R_STD,Momentum), axis=1)
        ind.fillna(0,inplace=True)
        ind = ind[:-self.Days]

        x_train = ind.values
        '''
        for i in range(0,len(prices)-self.Days):
            if i<20:
                x_train[i][0] = 0
                x_train[i][1] = 0
                x_train[i][2] = 0
                x_train[i][3] = prices.iloc[i]
                x_train[i][4] = prices.iloc[i + self.Days]
            else:
                x_train[i][0] = SMA.iloc[i]
                x_train[i][1] = bb_val.iloc[i]
                x_train[i][2] = Momentum.iloc[i]
                x_train[i][3]=prices.iloc[i]
                x_train[i][4]=prices.iloc[i+self.Days]
        '''

        #print x_train

        y_temp = []

        for i in range(0,len(prices)-self.Days):
            if prices.ix[i+self.Days,symbol]/prices.ix[i,symbol]> 1.008+self.impact:
                y_temp.append(1)
            elif prices.ix[i+self.Days,symbol]/prices.ix[i,symbol] < 0.992-self.impact:
                y_temp.append(-1)
            else:
                y_temp.append(0)




        y_train = np.array(y_temp)

        self.learner.addEvidence(x_train,y_train)


    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later

        #print prices

        S = sma(prices, 20)
        upper, lower, bb, r_m, r_std = bollinger(prices)
        M = momentum(prices)

        SMA = pd.DataFrame({'SMA': S})
        bb_val = pd.DataFrame({'Bollinger': bb})
        Upper = pd.DataFrame({'Upper': upper})
        Lower = pd.DataFrame({'Lower': lower})
        Momentum = pd.DataFrame({'Momentum': M})
        R_M = pd.DataFrame({'Rolling Mean': r_m})
        R_STD = pd.DataFrame({"Rolling STD": r_std})

        ind = pd.concat((SMA, bb_val,Upper,Lower,R_M,R_STD, Momentum), axis=1)
        ind.fillna(0, inplace=True)
        ind = ind[:-self.Days]

        x_test = ind.values
        '''
        x_test = np.zeros(shape=(len(prices) - self.Days, 3))
        for i in range(0, len(prices) - self.Days):
            if i<20:
                x_test[i][0] = 0
                x_test[i][1] = 0
                x_test[i][2] = 0
            else:
                x_test[i][0] = SMA.iloc[i]
                x_test[i][1] = bb_val.iloc[i]
                x_test[i][2] = Momentum.iloc[i]

        '''
        #print x_test
        y_ans = self.learner.query(x_test)
        #print(y_ans)
        trades = pd.DataFrame(0, columns=prices.columns, index=prices.index)
        shares=0
        for i in range(0,len(prices)-self.Days):
            if y_ans[i] == 1:
                trades[symbol].iloc[i] = 1000 - shares
                shares = 1000
            elif y_ans[i] ==-1:
                trades[symbol].iloc[i] = - shares - 1000
                shares = -1000

        #print trades

        '''
        trades.values[:,:] = 0 # set them all to nothing  		   	  			    		  		  		    	 		 		   		 		  
        trades.values[0,:] = 1000 # add a BUY at the start  		   	  			    		  		  		    	 		 		   		 		  
        trades.values[40,:] = -1000 # add a SELL  		   	  			    		  		  		    	 		 		   		 		  
        trades.values[41,:] = 1000 # add a BUY  		   	  			    		  		  		    	 		 		   		 		  
        trades.values[60,:] = -2000 # go short from long  		   	  			    		  		  		    	 		 		   		 		  
        trades.values[61,:] = 2000 # go long from short  		   	  			    		  		  		    	 		 		   		 		  
        trades.values[-1,:] = -1000 #exit on the last day  		   	  			    		  		  		    	 		 		   		 		  
        if self.verbose: print type(trades) # it better be a DataFrame!  		   	  			    		  		  		    	 		 		   		 		  
        if self.verbose: print trades  		   	  			    		  		  		    	 		 		   		 		  
        if self.verbose: print prices_all  		
        '''

        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
    learner = StrategyLearner()
    learner.addEvidence(symbol = "IBM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,1,1),sv = 10000)
    learner.testPolicy(symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=10000)