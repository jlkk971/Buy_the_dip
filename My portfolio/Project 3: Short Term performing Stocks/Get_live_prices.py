
from yahoo_fin.stock_info import *
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None, 'display.max_columns', None)

def data_mining():

    url=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').text
    soup=BeautifulSoup(url,'html.parser')
    table=soup.find('table',{'class':'wikitable sortable'})
    table=pd.read_html(str(table))
    table1=pd.DataFrame(table[0])
    tickers=table1['Symbol'].tolist()
    headers=[]

    tickers=['AAPL','AMZN']

    df=pd.DataFrame()

    for i in tickers:
        try:
            prices=yf.download(i, start='2010-01-01', end=date.today(), header=[0,1], parse_date=['Date'], index_col=['Date'] )
            prices2={'Close':get_live_price(i)}
            closing=pd.DataFrame(prices['Close'])
            last_date=date.today()
            #closing3=closing.append(pd.DataFrame(index=[last_date]))
            closing3=closing.append(pd.DataFrame(prices2, index=[last_date]))
            norm = closing3.div(closing3.iloc[0]).mul(100)
            df=df.append((closing3['Close']))
            headers.append(i)

        except:
            pass

    df=df.set_index([headers])
    df=df.T
    df=df.pct_change()
    df=df.replace(np.nan,0)
    df.index=pd.to_datetime(df.index, format='%Y-%m-%d')
    #df = df.to_csv(r'/Users/giuseppelecca/Desktop/Project_1 best performing stocks/stocks22-05-2021.csv')
    #TESTING ENVIRONMENT
    df=pd.read_csv(r'/Users/giuseppelecca/Desktop/Project_1 best performing stocks/stocks20-05-2021.csv')

    return df

print(data_mining())


