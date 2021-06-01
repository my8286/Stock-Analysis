import tkinter
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import nsepy as nse
from nsepy import get_history
import mplfinance as mpf
from tkinter.ttk import Progressbar
import pathlib
import time
from tkinter import HORIZONTAL



root = tkinter.Tk()
#window.geometry("1080x720")
root.state('zoomed')
# Icon of window
root.iconbitmap("")
# to rename the title of the window
root.title("MyStock")

# pack is used to show the object in the window
label = tkinter.Label(root, text = "Stock Analysis App for Simple Moving Average").pack()

# creating functions 

def Scanner():
    nifty=pd.read_csv('NIFTY200.csv')
    #time.sleep(60)
    # Get historical data of all Nifty50 stocks and filter out rising stocks
    # calculating the simple moving average (which is just mean calculated progressively) 
    # and add the result as a new column to dataframe
    list=[]
    updated=True
    for name, values in nifty.iteritems():
        for index in values:
            rising_stock=get_history(index,start=datetime(2021,1,1),end=datetime(datetime.now().year,datetime.now().month,datetime.now().day))
            sublist=[]
            if rising_stock.shape[0]>1 and rising_stock['Open'][-1] < rising_stock['Close'][-1]:
                short_window = 44
                rising_stock["44_obs_for_SMA"] = rising_stock["Close"].rolling(window=short_window).mean()
                
                if (rising_stock["High"][-1]>= rising_stock["44_obs_for_SMA"][-1] and rising_stock["Low"][-1]<= rising_stock["44_obs_for_SMA"][-1]):
                    sublist.append(index)
                    sublist.append(rising_stock["Open"][-1])
                    sublist.append(rising_stock["High"][-1])
                    sublist.append(rising_stock["Low"][-1])
                    sublist.append(rising_stock["Close"][-1])
                    sublist.append(rising_stock["44_obs_for_SMA"][-1])

                    list.append(sublist)
                    rising_stock.index.name = 'Date'

                    rising_stock.to_csv("stocks/{index}.csv".format(index=index))
                    print(index)
                
        #print('{name}: {value}'.format(name=name, value=values))
    data=pd.DataFrame(list,columns=["SYMBOL","Open","High","Low","Close","44_obs_for_SMA"])
    data=data[["SYMBOL","Open","High","Low","Close","44_obs_for_SMA"]]
    data.to_csv("stocks/rising_stocks.csv")
    #plot_chart()

def plot_chart():
    mc = mpf.make_marketcolors(up='g',down='r',edge='black',volume='gray',ohlc='black')
    s  = mpf.make_mpf_style(marketcolors=mc)
    rising_stocks=pd.read_csv('stocks/rising_stocks.csv',index_col=0)
    for index, row in rising_stocks.iterrows():
        stock = pd.read_csv('stocks/{symbol}.csv'.format(symbol=row["SYMBOL"]),index_col=0,parse_dates=True)
        #ourpath = pathlib.Path("img/{symbol}.png".format(symbol=row["SYMBOL"]))
        #mpf.plot(stock, type='candle',figratio=(100,40), mav=44, savefig=ourpath,style=s)
        mpf.plot(stock,type='candle',figratio=(38,15),mav=44,style=s)



def step():
    my_progress['value'] += 20

my_progress= Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
my_progress.pack(pady=20)
#tkinter.Button(root, text = "Click Me!", command = Scanner).pack(pady=20)
my_button=tkinter.Button(root, text="Progress", command = step)
my_button.pack(pady=20)

root.mainloop()