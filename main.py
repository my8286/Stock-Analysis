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
    for index, row in nifty.iterrows():
        rising_stock=get_history(row["SYMBOL"],start=datetime(2021,1,1),end=datetime(datetime.now().year,datetime.now().month,datetime.now().day))
        my_progress['value'] += 1
        root.update()
        if rising_stock.shape[0]>1 and rising_stock['Open'][-1] < rising_stock['Close'][-1]:
            SMA_window = 44
            rising_stock["44_obs_for_SMA"] = rising_stock["Close"].rolling(window=SMA_window).mean()

            if (rising_stock["High"][-1]>= rising_stock["44_obs_for_SMA"][-1] and rising_stock["Low"][-1]<= rising_stock["44_obs_for_SMA"][-1]) or abs(rising_stock["Low"][-1]-rising_stock["44_obs_for_SMA"][-1])<=2 :
                rising_stock.reset_index('Date',inplace=True)
                rising_stock['Date'] = pd.to_datetime(rising_stock.Date)
                rising_stock.set_index('Date',inplace=True)
                #print(row["SYMBOL"])
                rising_stock_list.insert(END,row["SYMBOL"])
                #mpf.plot(rising_stock,type='candle',figratio=(38,15),mav=44,style=s)
                plot_chart(rising_stock,row["SYMBOL"])
        
        
    

def plot_chart(df,symbol):
    mc = mpf.make_marketcolors(up='g',down='r',edge='black',volume='gray',ohlc='black')
    s  = mpf.make_mpf_style(marketcolors=mc)
    ourpath = pathlib.Path("img/{symbol}.png".format(symbol=symbol))
    mpf.plot(df, type='candle',figratio=(100,40), mav=44, savefig=ourpath,style=s)
        #mpf.plot(stock,type='candle',figratio=(38,15),mav=44,style=s)


def plot(event):

    n = rising_stock_list.curselection()
    filename = rising_stock_list.get(n)
    print(filename)
    image = Image.open("img/{filename}.png".format(filename=filename))
    resize_image = image.resize((1100,650))
    img = ImageTk.PhotoImage(resize_image)
    main_label.config(image=img)
    root.update()
  
   

def rising_stocks_list(value):
    rising_stock_list.insert(END,value)
    root.update()



def step():
    
    global my_progress
    my_progress= Progressbar(root, orient=HORIZONTAL, length=500, mode="determinate")
    my_progress.grid(row=3, column=3, columnspan=5, rowspan=5)
    my_progress['value'] = 1
    #my_progress.start(1)
    rising_stock_list.delete(0,END)
    scanner()
    my_progress.stop()
    my_progress.destroy()
    root.update()


def slideShow():
  #img = next(photos)
  main_label.config(image=img)
  #root.after(50, slideShow) # 0.05 seconds


def left_layout():
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

    list1.pack()
    list1.insert(END,"Nifty50")
    list1.insert(END,"Nifty100")
    list1.insert(END,"Nifty200")

    # list2 frame inside left frame
    list_frame2= Frame(left_frame)
    list_scrollbar= Scrollbar(list_frame2, orient=VERTICAL)
    list2=Listbox(list_frame2, width=30,height=15, yscrollcommand=list_scrollbar.set)
    label2=Label(list_frame2, text="Rising Stocks", width=30,  bg="#2962ff" ,fg="#FFFFFF")
    label2.pack()

    list_scrollbar.config(command=list2.yview)
    list_scrollbar.pack(side=RIGHT,fill=Y)
    list_frame2.pack(fill=X)

    list2.pack()
    list2.insert(END,"Nifty50")
    list2.insert(END,"Nifty100")
    list2.insert(END,"Nifty200")

    left_frame.pack(side=LEFT, fill=Y)

def header_layout():
    # header frame for menu
    header_frame=Frame(frame,bg="yellow")
    button1=Button(header_frame, text="Home", width=15, bg="#2962ff" ,fg="#FFFFFF", command = step)
    button1.grid(row=0,column=0,sticky="nsew")
    button2=Button(header_frame, text="Live Market", width=15, bg="#2962ff" ,fg="#FFFFFF", command = plot)
    button2.grid(row=0,column=1,sticky="nsew")
    button3=Button(header_frame, text="Scan MA stocks", width=15, bg="#2962ff" ,fg="#FFFFFF", command = step)
    button3.grid(row=0,column=3,sticky="nsew")
    header_frame.pack(fill=X)

def middle_layout():
    # middle frame layout
    chart_frame=Frame(frame,bg="orange")
    lb=Label(chart_frame,text="test",width=30)
    lb.pack()
    chart_frame.pack(side=LEFT, fill=BOTH, expand=True)


def right_layout():
    # right frame layout
    right_frame=Frame(frame,bg="yellow")
    lb=Label(frame,text="test2",width=30)
    lb.pack()
    right_frame.pack(side=RIGHT, fill=Y)
# left frame layout
# left_frame=Frame(frame,bg="blue")
# lb=Label(left_frame,text="test",width=30)
# lb.pack()
# left_frame.pack(side=LEFT, fill=Y)

# parent frame
frame=Frame(root,bg="red")
frame.pack(fill="both",expand=True)

header_layout()
left_layout()
middle_layout()
right_layout()












# list_frame2= Frame(root)
# list_scrollbar2= Scrollbar(list_frame2, orient=VERTICAL)
# rising_stock_label=Label(list_frame2, text="Rising Stocks", width=25, bg="#2962ff" ,fg="#FFFFFF")
# rising_stock_list=Listbox(list_frame2, width=25)
# rising_stock_list.insert(END,"CUB")
# rising_stock_list.bind("<<ListboxSelect>>", plot)
# list_scrollbar2.config(command=my_list.yview)

# list_scrollbar2.pack(side=RIGHT,fill=Y)
# rising_stock_label.pack()
# rising_stock_list.pack()
# list_frame2.grid(row=3, column=0)


# # images = ["TCS.png", "IGL.png"]
# # photos = cycle(ImageTk.PhotoImage(Image.open("img/{symbol}".format(symbol=image))) for image in images)
# image = Image.open("img/TCS.png")
  
# # Reszie the image using resize() method
# resize_image = image.resize((1100,650))
  
# img = ImageTk.PhotoImage(resize_image)

# main_frame=Frame(root, bg="blue",width=100,height=100)
# width = main_frame.winfo_screenwidth()
# height = main_frame.winfo_screenwidth()
# main_label=Label(main_frame)
# main_label.pack()
# main_frame.grid(row=2,column=1, columnspan=99, rowspan=20)

#root.after(10, lambda: slideShow())
root.mainloop()