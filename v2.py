from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
from nsepy import get_history
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pathlib
from threading import *
import matplotlib as matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def refresh():
    nifty=pd.read_csv('NIFTY500.csv')
    for index, row in nifty.iterrows():
        try:
            symbol=row["Symbol"]
            d = datetime.today() - timedelta(days=150)
            day=datetime.now().day
            month=datetime.now().month
            year=datetime.now().year
            df=get_history(symbol,start=datetime(d.year,d.month,d.day),end=datetime(year,month,day))
            data=pd.DataFrame(df)
            data.to_csv(f"stocks/{symbol}.csv")
            root.update()
        except:
            print("exception occur")
dict={}
def scanner():
    global dict
    nifty=pd.read_csv('NIFTY500.csv')

    for index, row in nifty.iterrows():
        symbol=row["Symbol"]
        rising_stock=pd.read_csv(f'stocks/{symbol}.csv',index_col=0,parse_dates=True)
        root.update()
        if rising_stock.shape[0]> 1:
            open=rising_stock['Open'][-1]
            close=rising_stock['Close'][-1]
            if open< close :
                window = 44
                rising_stock["44_obs_for_SMA"] = rising_stock["Close"].rolling(window=window).mean()

                sma_last=rising_stock["44_obs_for_SMA"][-1]
                sma_5=rising_stock["44_obs_for_SMA"][-5]
                sma_11=rising_stock["44_obs_for_SMA"][-11]
                sma_16=rising_stock["44_obs_for_SMA"][-16]
                sma_22=rising_stock["44_obs_for_SMA"][-22]
                sma_33=rising_stock["44_obs_for_SMA"][-33]
                sma_44=rising_stock["44_obs_for_SMA"][-44]
                high=rising_stock["High"][-1]
                low=rising_stock["Low"][-1]
                price=close*(2/100)
                if sma_44<sma_33 and sma_33<sma_22 and sma_22<sma_16 and sma_16<sma_11 and sma_11<sma_5 and sma_5<sma_last and sma_11<sma_last and sma_16<sma_last and sma_22<sma_last:
                    if (high>= sma_last and low<= sma_last) or (abs(low-sma_last)<=price and low>=sma_last):
                        rising_stock.reset_index('Date',inplace=True)
                        rising_stock['Date'] = pd.to_datetime(rising_stock.Date)
                        rising_stock.set_index('Date',inplace=True)
                        #print(row["SYMBOL"])
                        list.insert(END,symbol)
                        data_list=[]
                        data_list.append(row["Company Name"])
                        data_list.append(row["Industry"])
                        dict[symbol]=data_list
                        

canvas1=None
def showing(event):
    global canvas1
    canvas1.destroy()
    
    
    n = list.curselection()
    symbol = list.get(n)
    data_list=dict[symbol]
    
    name_label.config(text=f"Symbol: {data_list[0]}")
    sector_label.config(text=f"Sector: {data_list[1]}")
    canvas1=Label(chart_frame,bg="#F9FBFD")
    canvas1.pack(fill="both",expand=True)

    df=pd.read_csv(f'stocks/{symbol}.csv',index_col=0,parse_dates=True)
    mc = mpf.make_marketcolors(up='g', #Green
                               down='r', #Red
                               edge='black',
                               wick='black',
                               volume='in')
    
    s  = mpf.make_mpf_style(
                            mavcolors=["blue","orange"],
                            facecolor = "#F9FBFD",
                            gridcolor = "#F9FBFD",
                            gridstyle = "--",
                            marketcolors=mc)
    
    fig, ax = mpf.plot(df,type='candle',
                      style = s,
                      mav=44,
                      #title = f"{symbol}",
                      figratio=(60,30),
                      returnfig=True
                      )
    
    
    canvas = FigureCanvasTkAgg(fig, master=canvas1)   
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    list.bind("<Configure>", showing)

root=Tk()

#root.geometry("800x600+0+0")
root.state("zoomed")
  

header_frame=Frame(root,height=30,width=100, bg="#3700B3")
button1=Button(header_frame, text="Home" ,bg="#2962ff" ,fg="#FFFFFF", command=scanner)
button1.grid(row=0,column=0,sticky="nsew")
button2=Button(header_frame, text="Rising Stock", bg="#2962ff" ,fg="#FFFFFF", command=scanner)
button2.grid(row=0,column=1,sticky="nsew")
button3=Button(header_frame, text="Scan Stock", bg="#2962ff" ,fg="#FFFFFF" ,command=scanner)
button3.grid(row=0,column=2,sticky="nsew")
button4=Button(header_frame, text="Refresh", bg="#2962ff" ,fg="#FFFFFF" ,command=refresh)
button4.grid(row=0,column=3,sticky="nsew")
header_frame.grid_columnconfigure(0,weight=1)
header_frame.grid_columnconfigure(1,weight=1)
header_frame.grid_columnconfigure(2,weight=1)
header_frame.grid_columnconfigure(3,weight=1)
header_frame.pack(fill=X)

aside_frame=Frame(root)
# Index list
list_frame= Frame(aside_frame)
list_scrollbar= Scrollbar(list_frame, orient=VERTICAL)
list=Listbox(list_frame, width=30, height=15, yscrollcommand=list_scrollbar.set)
label=Label(list_frame, text="Index Stocks", width=30,  bg="#2962ff" ,fg="#FFFFFF")
label.pack()

list_scrollbar.config(command=list.yview)
list_scrollbar.pack(side=RIGHT,fill=Y)
list_frame.pack()

list.pack(fill=X, expand=True)
list.insert(END,"Nifty")
list.insert(END,"Nifty50")
list.insert(END,"Nifty100")
list.insert(END,"Nifty200")
list.insert(END,"Nifty100")
list.insert(END,"CNXIT")
list.insert(END,"CNXPHARMA")


# Rising stock list
list_frame= Frame(aside_frame)
list_scrollbar= Scrollbar(list_frame, orient=VERTICAL,bg="#F9FBFD")
list=Listbox(list_frame, width=30, height=23, yscrollcommand=list_scrollbar.set)
label=Label(list_frame, text="Rising Stocks", width=30,  bg="#2962ff" ,fg="#FFFFFF")
label.pack()

list_scrollbar.config(command=list.yview)
list_scrollbar.pack(side=RIGHT,fill=Y)
list_frame.pack()

list.pack(fill=X, expand=True)
list.bind("<<ListboxSelect>>", showing)
aside_frame.pack(side=LEFT, fill=Y)

chart_frame=Frame(root,padx=2,pady=5,bg="#F9FBFD")
chart_frame.pack(side=LEFT, fill=BOTH, expand=True)

horizontal_frame=Frame(chart_frame,bg="#F9FBFD")
horizontal_frame.pack(fill=X)
name_label=Label(horizontal_frame,text=f"Symbol: ",bg="#F9FBFD")
name_label.grid(row=0, column=0, padx=10,pady=10,sticky="nsew")
sector_label=Label(horizontal_frame,text="sector: IT",bg="#F9FBFD")
sector_label.grid(row=0, column=1, padx=10,pady=10,sticky="nsew")
horizontal_frame.grid_columnconfigure(0,weight=1)
horizontal_frame.grid_columnconfigure(1,weight=1)
canvas1=Label(chart_frame,bg="#F9FBFD")
canvas1.pack()


root.mainloop()