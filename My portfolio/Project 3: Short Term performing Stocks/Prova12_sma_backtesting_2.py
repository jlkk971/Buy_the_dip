import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import pandas_datareader
import requests
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def sma_calc():
    startyear = 2019
    startmonth = 1
    startday = 1

    start = dt.datetime(startyear, startmonth, startday)

    now = dt.datetime.now()

