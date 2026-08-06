import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

def data_pull():
  ticker = input("What ticker would you like to see?: ")
  start_date = input("What is your desired start date (YYYY-MM-DD)?: ")
  end_date = input("What is your desired end date (YYYY-MM-DD)?: ")
  data = yf.download(ticker, start=start_date, end=end_date, progress = False, auto_adjust = True)
  close = data["Close"].squeeze()
  start_price = close.iloc[0]
  end_price = close.iloc[-1] 
  growth_rate = end_price/start_price
  day_number = len(close)
  years = day_number/252
  data_returns = close.pct_change()
  data_mean = np.mean(data_returns)
  data_sd = np.std(data_returns)
  running_peak = close.cummax()
  drawdown = (close/running_peak)-1
  max_drawdown = drawdown.min()*100
  downwards_returns = data_returns[data_returns<0]  
  data_downwards_sd = np.std(downwards_returns)
  data_riskfree = yf.download("^IRX", start=start_date, end=end_date, progress = False, auto_adjust = True)
  closing = data_riskfree["Close"].squeeze()
  data_riskfree_mean = (np.mean(closing)/100)/252
  close.plot()
  plt.title(ticker+" Closing Price ("+start_date[:4]+"-"+end_date[:4]+")")
  plt.ylabel("Stock Value (USD)")
  plt.xlabel("Dates")
  plt.show()
  sharpe_ratio = ((data_mean - data_riskfree_mean)/data_sd)*np.sqrt(252)
  sortino_ratio = ((data_mean - data_riskfree_mean)/data_downwards_sd)*np.sqrt(252)
  cagr = (((growth_rate**(1/years))-1)*100)
  print("Sharpe Ratio: "+str(round(sharpe_ratio,2)))
  print("Sortino Ratio: "+str(round(sortino_ratio,2)))
  print("CAGR: "+str(round(cagr,2))+"%")
  print("Max Drawdown: "+str(round(max_drawdown,2))+"%")
                                                                     
data_pull()
  

           


