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

root = tkinter.Tk()
#window.geometry("1080x720")
root.state('zoomed')
#window.attributes("-fullscreen", True)
# to rename the title of the window
root.title("MyStock")
# pack is used to show the object in the window
#label = tkinter.Label(window, text = "Stock Analysis App for Simple Moving Average").pack()
# creating a function called DataCamp_Tutorial()
def DataCamp_Tutorial():
    tkinter.Label(root, text = "GUI with Tkinter!").pack()
    progress = Progressbar(root, orient=HORIZONTAL,length=100,  mode='indeterminate')
    nifty=pd.read_csv('NIFTY200.csv')
    # Get historical data of all Nifty50 stocks and filter out rising stocks
    # calculating the simple moving average (which is just mean calculated progressively) 
    # and add the result as a new column to dataframe
    list=[]
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

tkinter.Button(root, text = "Click Me!", command = DataCamp_Tutorial).pack()

root.mainloop()