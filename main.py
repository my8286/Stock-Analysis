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
from tkinter import HORIZONTAL, END


root = tkinter.Tk()
#window.geometry("1080x720")
root.state('zoomed')
# Icon of window
root.iconbitmap("logo.png")
# to rename the title of the window
root.title("MyStock")

# pack is used to show the object in the window
#label = tkinter.Label(root, text = "Stock Analysis App for Simple Moving Average").pack()

# creating functions 

def scanner():
    nifty=pd.read_csv('NIFTY200.csv')
    #time.sleep(60)
    # Get historical data of all Nifty50 stocks and filter out rising stocks
    # calculating the simple moving average (which is just mean calculated progressively) 
    # and add the result as a new column to dataframe
    list=[]
    
    for name, values in nifty.iteritems():
        for index in values:
            rising_stock=get_history(index,start=datetime(2021,1,1),end=datetime(datetime.now().year,datetime.now().month,datetime.now().day))
            sublist=[]
            root.update()
            if rising_stock.shape[0]>1 and rising_stock['Open'][-1] < rising_stock['Close'][-1]:
                short_window = 44
                rising_stock["44_obs_for_SMA"] = rising_stock["Close"].rolling(window=short_window).mean()
                root.update()
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
                    root.update()
                
        #print('{name}: {value}'.format(name=name, value=values))
    data=pd.DataFrame(list,columns=["SYMBOL","Open","High","Low","Close","44_obs_for_SMA"])
    data=data[["SYMBOL","Open","High","Low","Close","44_obs_for_SMA"]]
    data.to_csv("stocks/rising_stocks.csv")
    plot_chart()
    

def plot_chart():
    mc = mpf.make_marketcolors(up='g',down='r',edge='black',volume='gray',ohlc='black')
    s  = mpf.make_mpf_style(marketcolors=mc)
    rising_stocks=pd.read_csv('stocks/rising_stocks.csv',index_col=0)
    for index, row in rising_stocks.iterrows():
        root.update()
        stock = pd.read_csv('stocks/{symbol}.csv'.format(symbol=row["SYMBOL"]),index_col=0,parse_dates=True)
        ourpath = pathlib.Path("img/{symbol}.png".format(symbol=row["SYMBOL"]))
        mpf.plot(stock, type='candle',figratio=(100,40), mav=44, savefig=ourpath,style=s)
        #mpf.plot(stock,type='candle',figratio=(38,15),mav=44,style=s)


def rising_stocks_list(value):
    rising_stock_list.insert(END,value)
    root.update()



def step():
    #my_progress['value'] += 20
    my_progress= Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
    my_progress.grid(row=3, column=3, columnspan=5, rowspan=5)
    my_progress.start(1)
    scanner()
    my_progress.stop()
    my_progress.destroy()



#tkinter.Button(root, text = "Click Me!", command = scanner).pack(pady=20)
home_button=tkinter.Button(root, text="Home", width=15, bg="#2962ff" ,fg="#FFFFFF", command = step)
home_button.grid(row=0, column=0)

market_button=tkinter.Button(root, text="Live Market", width=15, bg="#2962ff" ,fg="#FFFFFF", command = step)
market_button.grid(row=0, column=1)

scan_stock_button=tkinter.Button(root, text="Scan MA stocks", width=15, bg="#2962ff" ,fg="#FFFFFF", command = step)
scan_stock_button.grid(row=0, column=2)



my_label=tkinter.Label(root, text="NSE Indices", width=15,  bg="#2962ff" ,fg="#FFFFFF")
my_label.grid(row=1, column=0)

my_list=tkinter.Listbox(root, width=15)
my_list.grid(row=2, column=0)
my_list.insert(END,"Nifty50")
my_list.insert(END,"Nifty100")
my_list.insert(END,"Nifty200")

rising_stock_label=tkinter.Label(root, text="Rising Stocks", width=15, bg="#2962ff" ,fg="#FFFFFF")
rising_stock_label.grid(row=3, column=0)

rising_stock_list=tkinter.Listbox(root, width=15)
rising_stock_list.grid(row=4, column=0)


root.mainloop()