
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
    soup=BeautifulSoup(url,'lxml')
    table=soup.find('table',{'class':'wikitable sortable'})
    tick=table.findAll('td')
    tick=table.findAll('a')
    links=[]
    links2=[]
    tickers=[]
    for i in tick:
        links.append(i.get('href'))

    for i in links:
        if 'http' in i:

            if ':' in i[-1]:
                links2.append(i[0])
            elif ':' in i[-2]:
                links2.append(i[-1:])
            elif ':' in i[-3]:
                links2.append(i[-2:])

            elif ':' in i[-4:]:
                links2.append(i[-3:])
            elif 'pany' in i:
                pass
            elif ':' in i[-5:]:
                links2.append(i[-4:])
            elif '/' in i[-1]:
                links2.append(i[0])
            elif '/' in i[-2]:
                links2.append(i[-2:])
            elif '/' in i[-4]:
                links2.append(i[-3:])
            elif '/' in i[-5]:
                links2.append(i[-4:])
            elif '/' in i[-4]:
                links2.append(i[-3:])
            elif '/' in i[-3]:
                links2.append(i[-2:])
            elif '/' in i[-2]:
                links2.append(i[-1:])
            elif '/' in i[-1]:
                links2.append(i[0])
            elif 'pany' in i:
                pass
            else:
                links2.append(i[-5:])

    for i in links2:
        tickers.append(i.upper())

    tickers=sorted(tickers)
    tickers.remove('BF.B')
    tickers.remove('BRK.B')

    tickers=list(dict.fromkeys(tickers))
    tickers=sorted(tickers)
    tickers2=[]

    for i in tickers:
        try:
            prices=yf.download(i, start='2018-01-01', end=date.today(), header=[0,1], parse_date=['Date'], index_col=['Date'] )
            prices2={'Close':get_live_price(i)}
            closing=pd.DataFrame(prices['Close'])
            last_date=date.today()
            #closing3=closing.append(pd.DataFrame(index=[last_date]))
            closing3=closing.append(pd.DataFrame(prices2, index=[last_date]))
            norm = closing3.div(closing3.iloc[0]).mul(100)
            df=df.append((closing3['Close']))
            tickers2.append(i)

        except:
            pass

    df=df.set_index([tickers2])
    df=df.T
    df=df.pct_change()
    df=df.replace(np.nan,0)
    df.index=pd.to_datetime(df.index, format='%Y-%m-%d')
    print(df)

    df = df.to_csv(r'/Users/giuseppelecca/Desktop/Project_1 best performing stocks/stocks07-05-2021.csv')

    return df

data_mining()



