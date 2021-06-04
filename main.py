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
from tkinter import HORIZONTAL, END, Frame, LEFT
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from itertools import cycle
from PIL import ImageTk, Image
import glob,os, shutil


root = tkinter.Tk()

root.geometry("600x400")
#root.state('zoomed')
# Icon of window
root.iconbitmap("logo.png")
# to rename the title of the window
root.title("MyStock")

# pack is used to show the object in the window
#label = tkinter.Label(root, text = "Stock Analysis App for Simple Moving Average").pack()
my_progress=None
new_window=None
# creating functions 
 
def scanner():
    nifty=pd.read_csv('NIFTY200.csv')

    for index, row in nifty.iterrows():
        symbol=row["SYMBOL"]
        rising_stock=get_history(symbol,start=datetime(2021,1,1),end=datetime(datetime.now().year,datetime.now().month,datetime.now().day))
        my_progress['value'] += 1
        root.update()
        if rising_stock.shape[0]>1 and rising_stock['Open'][-1] < rising_stock['Close'][-1]:
            SMA_window = 44
            rising_stock["44_obs_for_SMA"] = rising_stock["Close"].rolling(window=SMA_window).mean()

            if (rising_stock["High"][-1]>= rising_stock["44_obs_for_SMA"][-1] and rising_stock["Low"][-1]<= rising_stock["44_obs_for_SMA"][-1]):
                rising_stock.reset_index('Date',inplace=True)
                rising_stock['Date'] = pd.to_datetime(rising_stock.Date)
                rising_stock.set_index('Date',inplace=True)
                #print(row["SYMBOL"])
                list2.insert(END,symbol)
                #new_window.title(symbol)
                #mpf.plot(rising_stock,type='candle',figratio=(38,15),mav=44,style=s)
                plot_chart(rising_stock,symbol)
        
        
    

def plot_chart(df,symbol):
    mc = mpf.make_marketcolors(up='g',down='r',edge='black',volume='gray',ohlc='black')
    s  = mpf.make_mpf_style(marketcolors=mc)
    ourpath = pathlib.Path("img/{symbol}.png".format(symbol=symbol))
    mpf.plot(df, type='candle',figratio=(100,40), mav=44, savefig=ourpath,style=s)
        #mpf.plot(stock,type='candle',figratio=(38,15),mav=44,style=s)


   

def step():
    
    global my_progress
    global new_window
    # window_width = 500
    # window_height = 100

    # get the screen dimension
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()

    # # find the center point
    # center_x = int(screen_width/2 - window_width / 2)
    # center_y = int(screen_height/2 - window_height / 2)

    # # set the position of the window to the center of the screen
    # new_window=Toplevel(root)
    # new_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # new_window.title("Scanning stocks")
    # new_window.resizable(False,False)
    my_progress= Progressbar(chart_frame, orient=HORIZONTAL, length=500, mode="determinate")
    my_progress.pack(padx=20,pady=20)
    my_progress['value'] = 1
    #my_progress.start(1)
    list2.delete(0,END)
    scanner()
    my_progress.stop()
    my_progress.destroy()
    #new_window.destroy()



def get_window_size():
    if chart_frame.winfo_width() > 200 and chart_frame.winfo_height() >30:
        w = chart_frame.winfo_width() - 200
        h = chart_frame.winfo_height() - 30
    else:
        w = 200
        h = 30
    return w, h


def showing(event):
    n = list2.curselection()
    filename = list2.get(n)
    im = Image.open("img/{filename}.png".format(filename=filename))
    im = im.resize((get_window_size()), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)
    w, h = img.width(), img.height()
    canvas.image = img
    canvas.config(width=w, height=h)
    canvas.create_image(0, 0, image=img, anchor=NW)
    chart_frame.bind("<Configure>", lambda x: showing(x))


# parent frame
frame=Frame(root,bg="red")
frame.pack(fill="both",expand=True)   


# header frame for menu
header_frame=Frame(frame,bg="yellow")
button1=Button(header_frame, text="Home", width=15, bg="#2962ff" ,fg="#FFFFFF", command = step)
button1.grid(row=0,column=0,sticky="nsew")
button2=Button(header_frame, text="Live Market", width=15, bg="#2962ff" ,fg="#FFFFFF", command = step)
button2.grid(row=0,column=1,sticky="nsew")
button3=Button(header_frame, text="Scan MA stocks", width=15, bg="#2962ff" ,fg="#FFFFFF", command = step)
button3.grid(row=0,column=3,sticky="nsew")
header_frame.pack(fill=X)

# left frame
left_frame=Frame(frame,bg="blue")

# list1 frame inside left frame
list_frame= Frame(left_frame)
list_scrollbar= Scrollbar(list_frame, orient=VERTICAL)
list1=Listbox(list_frame, width=30,height=15, yscrollcommand=list_scrollbar.set)
label1=Label(list_frame, text="NSE Indices", width=30,  bg="#2962ff" ,fg="#FFFFFF")
label1.pack()

list_scrollbar.config(command=list1.yview)
list_scrollbar.pack(side=RIGHT,fill=Y)
list_frame.pack(fill=X)

list1.pack(fill=X, expand=True)
list1.insert(END,"Nifty50")
list1.insert(END,"Nifty100")
list1.insert(END,"Nifty200")

# list2 frame inside left frame
list_frame2= Frame(left_frame)
list_scrollbar= Scrollbar(list_frame2, orient=VERTICAL)
list2=Listbox(list_frame2, width=30,height=25, yscrollcommand=list_scrollbar.set)
label2=Label(list_frame2, text="Rising Stocks", width=30,  bg="#2962ff" ,fg="#FFFFFF")
label2.pack()

list_scrollbar.config(command=list2.yview)
list_scrollbar.pack(side=RIGHT,fill=Y)
list_frame2.pack(fill=X)

list2.pack(fill=X, expand=True)
list2.bind("<<ListboxSelect>>", showing)



left_frame.pack(side=LEFT, fill=Y)



# middle frame layout
chart_frame=Frame(frame)
canvas = Canvas(chart_frame)
canvas.pack()
chart_frame.pack(side=LEFT, fill=BOTH, expand=True)


root.mainloop()