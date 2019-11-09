import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
import util as ut
import marketsimcode as ms
import indicators as ind

def testPolicy(symbol, sd, ed, sv):


    symbols = [symbol]
    dates = pd.date_range(sd, ed)
    benchmark = ut.get_data(symbols, dates, addSPY=False).dropna()
    #print benchmark
    prices = benchmark['JPM'].values

    trades = pd.DataFrame(data=np.zeros(len(prices)), index=benchmark.index, columns=['JPM'])

    '''
    vals=np.zeros(len(prices))
    helper(0,len(prices)-1,prices,vals)
    print 'A'
    print vals

    if vals[0]==1:
        trades.at[trades.iloc[0].name, 'JPM'] = 1000
    else:
        trades.at[trades.iloc[0].name, 'JPM'] = -1000


    for i in range(1,len(vals)-1):
        if vals[i] == -1 and vals[i+1]!=-1:
            trades.at[trades.iloc[i].name,'JPM'] = -2000
        elif vals[i] == -1 and vals[i+1]==-1:
            if prices[i]>prices[i+1]:
                trades.at[trades.iloc[i].name, 'JPM'] = -2000
                vals[i+1]=0
            else:
                continue
        if vals[i] == 1 and vals[i+1]!=1:
            trades.at[trades.iloc[i].name,'JPM'] = 2000
        elif vals[i] == 1 and vals[i+1]==1:
            if prices[i]<prices[i+1]:
                trades.at[trades.iloc[i].name, 'JPM'] = 2000
                vals[i+1]=0
            else:
                continue


    '''
    benchmark_trades = pd.DataFrame({'Date': dt.datetime(2008,1,2), 'JPM': [1000]})
    benchmark_trades.set_index("Date", inplace=True)

    sma = ind.sma(benchmark,14)
    #sma2 = ind.sma(benchmark,10)

    mom = ind.momentum(benchmark)
    print mom
    upper,lower,vals,rm,rstd = ind.bollinger(benchmark)


    current =0
    for i in range(14, len(prices)):
        # Smaller than threshold -> buy
        # Bigger than threshold -> sell
        if sma[i] < 0.95 and vals[i]<0:
            trades['JPM'].iloc[i] = 1000 - current
            current = 1000
        elif sma[i] > 1.05 and vals[i]>1:
            trades['JPM'].iloc[i] = - current - 1000
            current = -1000



    return trades,benchmark_trades

if __name__ == "__main__":
    insample_start = dt.datetime(2008, 1, 1)
    insample_end = dt.datetime(2009, 12, 31)
    symbol = ['JPM']
    dates = pd.date_range(insample_start,insample_end)
    benchmark = ut.get_data(symbol,dates,addSPY=False).dropna()
    print benchmark
    insample_start = benchmark.index[0]
    benchmark_trades = pd.DataFrame({'Date':[insample_start],'JPM':[1000]})
    benchmark_trades.set_index("Date", inplace=True)

    #print benchmark_trades

    trades = testPolicy('JPM',insample_start,insample_end,1000000)

    print trades
    ans_jpm = ms.compute_portvals(trades,100000,9.95,0.005)
    daily_return = ans_jpm.copy()
    daily_return[1:] = (daily_return[1:] / daily_return[:-1].values) - 1
    daily_return = daily_return[1:]
    cr = (ans_jpm[-1] / ans_jpm[0]) - 1
    adr = daily_return.mean()
    sddr = daily_return.std()
    sr = adr / sddr
    print (cr, adr, sddr)
    ans_benchmark = ms.compute_portvals(benchmark_trades,100000,9.95,0.005)
    daily_return = ans_benchmark.copy()
    daily_return[1:] = (daily_return[1:] / daily_return[:-1].values) - 1
    daily_return = daily_return[1:]
    cr = (ans_benchmark[-1] / ans_benchmark[0]) - 1
    adr = daily_return.mean()
    sddr = daily_return.std()
    sr = adr / sddr
    print (cr, adr, sddr)
    ans_jpm = ans_jpm/ans_jpm[0]
    ans_benchmark = ans_benchmark/ans_benchmark[0]

    #print ans_jpm
    plt.plot(ans_jpm)
    plt.plot(ans_benchmark)


    chart = pd.concat([ans_jpm, ans_benchmark], axis=1)
    chart.columns = ['Portfolio', 'Benchmark']
    chart.plot(grid=True, title='Strategy vs Benchmark index', use_index=True, color=['Black', 'Blue'])
    plt.savefig("Manual2")
    plt.show()





