import datetime as dt
import pandas as pd
import util as ut
import numpy as np
import random
from util import get_data, plot_data
import ManualStrategy as ms
import StrategyLearner as sl
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
def stats(ans_jpm):
    daily_return = ans_jpm.copy()
    daily_return[1:] = (daily_return[1:] / daily_return[:-1].values) - 1
    daily_return = daily_return[1:]
    cr = (ans_jpm[-1] / ans_jpm[0]) - 1
    adr = daily_return.mean()
    sddr = daily_return.std()
    sr = adr / sddr
    print (cr, adr, sddr, sr)
def main():
    sd = dt.date(2008,1,1)
    ed = dt.date(2009,12,31)
    sv = 100000
    symbol = ['JPM']
    dates = dates = pd.date_range(sd, ed)
    prices_all = ut.get_data(symbol, dates)

    #--------------------------Strategy Learner------------------------------
    st_learner = sl.StrategyLearner(verbose= False, impact=0.0)
    st_learner.addEvidence('JPM', sd, ed, sv)
    df_strategy = st_learner.testPolicy('JPM', sd, ed, sv)



    #__________________________Manual Strategy-------------------------------
    df_trades,df_benchmark = ms.testPolicy('JPM', sd, ed, sv)

    port_st = compute_portvals(df_strategy,sv,0.0,0.0)
    stats(port_st)

    port_ms = compute_portvals(df_trades,sv,0.0,0.0)
    stats(port_ms)
    port_bench = compute_portvals(df_benchmark,sv,0.0,0.0)
    stats(port_bench)

    chart = pd.concat([port_st, port_ms,port_bench], axis=1)
    chart.columns = ['Portfolio Strategy Learner','Portfolio Manual Strategy', 'Portfolio Benchmark']
    chart.plot(grid=True, title='Comparison of Portfolio Values', use_index=True, color=['Red', 'Blue','Black'])
    plt.savefig("Comp")
    plt.show()



if __name__=="__main__":
    main()