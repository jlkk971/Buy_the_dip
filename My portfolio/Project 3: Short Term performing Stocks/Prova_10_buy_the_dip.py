import requests
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date, timedelta
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None, 'display.max_columns', None)



d=date(2020,1,1)

def data_mining():
    df=pd.read_csv('/Users/giuseppelecca/Desktop/Project_1 best performing stocks/stocks09-04-2021.csv', index_col=0, parse_dates=True)
    df=pd.DataFrame(df).sort_index()
    df=df[d.strftime('%Y-%m-%d'):]
    return df

def rolling_sampling():
    df=data_mining()
    #rolling sharpe ratio
    rolly_mean=df.rolling(window=180).mean()
    rolly_std=df.rolling(window=180).std()*np.sqrt(126)
    rolly_sharpe=(rolly_mean*126-0.0069)/rolly_std
    rolly_sharpe=rolly_sharpe.dropna()
    return rolly_sharpe

def find_top():
    df=rolling_sampling()
    df=df.apply(lambda s: s.nlargest(100).index.tolist(), axis=1)
    csv=df.tail().to_csv(r'/Users/giuseppelecca/Desktop/Project_1 best performing stocks/Tickers10-04-2021.csv')
    df_2=data_mining()
    backtest=pd.DataFrame()
    df=pd.DataFrame(df)
    for i, row in df.iterrows():
        for item in row:
            backtest=backtest.append(df_2.loc[i,item])

    df_lowest_ret=backtest.apply(lambda s: s.nsmallest(5).index.tolist(),axis=1)
    #csv=df_lowest_ret.to_csv(r'/Users/giuseppelecca/Desktop/Project_1 best performing stocks/Tickers_11-03-2021.csv')
    print(df_lowest_ret)
    return df_lowest_ret

def backtesting():
    backtest=pd.DataFrame()
    df=find_top()
    df=pd.DataFrame(df)
    df=df.shift(1).dropna()
    df_2=data_mining()
    for i, row in df.iterrows():
        for item in row:
            backtest=backtest.append(df_2.loc[i,item])

    #backtest=backtest.replace(0, np.nan)
    #MARKOWITZ backwards??

    mean_backtest=backtest.mean(axis=1)

    mean_backtest=mean_backtest.add(1).cumprod().mul(100)
    #df = mean_backtest.to_excel(r'/Users/giuseppelecca/Desktop/Project_1 best performing stocks/output_19_20.xlsx')
    mean_backtest.div(mean_backtest.iloc[0]).mul(100)
    return mean_backtest

def versus_sp500():
    algo=backtesting()
    price=yf.download('^GSPC', start=(d+timedelta(days=260)), end=date.today(), parse_date=['Date'], set_index=['Date'])
    price=price['Close']
    price=price.div(price.iloc[0]).mul(100)
    print(price)
    final=pd.DataFrame()
    final['Algo']=algo
    final['SP500']=price
    print(final)
    final.plot()
    plt.show()

def mixed_vix():

    algo=backtesting()
    vix=yf.download('^VIX', start=(d+timedelta(days=260)), end=date.today(), parse_date=['Date'], set_index=['Date'])
    vix=pd.DataFrame(vix['Close'])

    sp500=yf.download('^GSPC ^VIX', start=(d+timedelta(days=260)), end=date.today(), parse_date=['Date'], set_index=['Date'])
    sp500=pd.DataFrame(sp500['Close'])


    final=pd.DataFrame()
    final['algo']=algo
    final['VIX']=sp500['^VIX']
    final['SP500']=sp500['^GSPC']
    final=final.pct_change().dropna()
    #pct_csv=final.to_csv(r'/Users/giuseppelecca/Desktop/Project_1 best performing stocks/final27-9-2020.csv')

    mat=np.ones((len(final['algo']),2))


    #Weights algo
    mat[:,0]=mat[:,0]*0.7

    #Weights Vix
    mat[:,1]=mat[:,1]*0.3

    algo_1=pd.DataFrame()
    algo_1['algo']=final['algo']*mat[:,0]
    algo_1['VIX']=final['VIX']*mat[:,1]


    sp_1=pd.DataFrame()
    sp_1['SP500']=final['SP500']*mat[:,0]
    sp_1['VIX'] = final['VIX']*mat[:,1]


    final1=sp_1.sum(axis=1)
    ret1=(final1+1).cumprod()
    ret1=ret1.dropna()
    final1=ret1.div(ret1.iloc[0]).mul(100)
    final1=final1.dropna()

    final=algo_1.sum(axis=1)
    ret=(final+1).cumprod()
    ret=ret.dropna()
    final=ret.div(ret.iloc[0]).mul(100)
    final=final.dropna()

    df_last=pd.DataFrame()
    df_last['SP500']=final1
    df_last['Algo']=final
    df_last.plot()
    plt.show()

def get_sharpe(r):
    summary=r.agg(['mean','std']).T
    summary=summary.rename(columns={'mean':'Return','std':'Risk'})
    summary['Return']=summary['Return']*252
    summary['Risk']=summary['Risk']*np.sqrt(12)
    summary['Sharpe']=(summary['Return']-0.0069)/summary['Risk']
    return summary


def Markowitz():
    df=find_top()
    df=df.iloc[-1]
    separator=' '
    lst=separator.join(df)
    prices=yf.download(str(lst), start=(date.today()-timedelta(days=300)), end=date.today(), parse_date='Date', set_index='Date')
    close=(prices['Close'])
    close=close.pct_change().dropna()
    summary=close.agg(['mean','std']).T
    summary=summary.rename(columns={'mean':'Return','std':'Risk'})
    summary['Return']=summary['Return']*252
    summary['Risk']=summary['Risk']*np.sqrt(252)
    summary['Sharpe']=(summary['Return']-0.0069)/summary['Risk']
    noa=len(close.columns)
    nop=100
    matrix=np.random.random(nop*noa).reshape(nop,noa)
    matrixsum=matrix.sum(axis=1,keepdims=True)
    weights=matrix/matrixsum
    port_ret=close.dot(weights.T)
    port_rand=get_sharpe(port_ret)

    mrsp=port_rand['Sharpe'].idxmax()
    mrsp_p=port_rand.iloc[mrsp]
    mrsp_w=weights[mrsp,:]
    weighted_av=summary.loc[:,['Return','Risk','Sharpe']].T.dot(mrsp_w)

    print(mrsp_w)
    print(weighted_av)
    print(summary)

def mixed_vix_sp():

    algo=backtesting()
    vix=yf.download('^VIX', start=(d+timedelta(days=260)), end=date.today(), parse_date=['Date'], set_index=['Date'])
    vix=pd.DataFrame(vix['Close'])

    sp500=yf.download('^GSPC ^VIX', start=(d+timedelta(days=260)), end=date.today(), parse_date=['Date'], set_index=['Date'])
    sp500=pd.DataFrame(sp500['Close'])


    final=pd.DataFrame()
    final['algo']=algo
    final['VIX']=sp500['^VIX']
    final['SP500']=sp500['^GSPC'].mul(5)
    final=final.pct_change().dropna()
    print(final)

    #pct_csv=final.to_csv(r'/Users/giuseppelecca/Desktop/Project_1 best performing stocks/final27-9-2020.csv')

    mat=np.ones((len(final['algo']),3))


    #Weights algo
    mat[:,0]=mat[:,0]*0.4

    #Weights Vix
    mat[:,1]=mat[:,1]*0.20

    #Weights SP
    mat[:, 2] = mat[:, 2] * 0.4

    algo_1=pd.DataFrame()
    algo_1['algo']=final['algo']*mat[:,0]
    algo_1['VIX']=final['VIX']*mat[:,1]
    algo_1['SP'] = final['SP500'] * mat[:, 2]

    sp_1=pd.DataFrame()
    sp_1['SP500']=final['SP500']#*mat[:,0]
    #sp_1['VIX'] = final['VIX']*mat[:,1]


    final1=sp_1.sum(axis=1)
    ret1=(final1+1).cumprod()
    ret1=ret1.dropna()
    final1=ret1.div(ret1.iloc[0]).mul(100)
    final1=final1.dropna()

    print("Hello World")

    final=algo_1.sum(axis=1)
    ret=(final+1).cumprod()
    ret=ret.dropna()
    final=ret.div(ret.iloc[0]).mul(100)
    final=final.dropna()


    df_last=pd.DataFrame()
    df_last['SP500']=final1
    df_last['Combination']=final
    df_last.plot()
    plt.show()


find_top()
