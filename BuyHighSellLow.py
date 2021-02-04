import pandas as pd
import pandas as pd
import numpy as np
import yfinance as yf  
from datetime import date
import pandas as pd
import math
import seaborn as sns

import matplotlib.pyplot as plt



filename = input('filenavn (transactions_export_2021-02-04T21_39_17.csv) :')
df = pd.read_csv(filename, engine='c', encoding ='utf_16',delimiter='\t')

print('Værdipapirer som du har handlet:')
print(list(df['Værdipapirer'].unique()))

buys = df[df['Transaktionstype']=='KØBT']
sells = df[df['Transaktionstype']=='SOLGT']
sells = sells.drop(1)
buys.head()


data = yf.download('SPY',df.tail(1)['Handelsdag'].values[0],date.today())
data['Date'] = data.index
data = data[['Date','Adj Close']]
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

fig = plt.figure(figsize=(14,7))
dates, prices = [], []
for i in buys['Valørdag']:
    dates.append(i)
    prices.append(data[data['Date']==i]['Adj Close'].values[0])

buyss = pd.DataFrame([dates,prices], index=['Date', 'price']).T
buyss['Date'] = pd.to_datetime(buyss['Date'], format='%Y-%m-%d')
plt.scatter(buyss['Date'], buyss['price'], c='g', label ='Buy')

dates, prices = [], []
for i in sells['Valørdag']:
    dates.append(i)
    prices.append(data[data['Date']==i]['Adj Close'].values[0])

sellss = pd.DataFrame([dates,prices], index=['Date', 'price']).T
sellss['Date'] = pd.to_datetime(sellss['Date'], format='%Y-%m-%d')

plt.scatter(sellss['Date'], sellss['price'], c='r', label='Sell')

first_day = df.tail(1)['Handelsdag'].values[0].split('-')
first_day = date(int(first_day[0]), int(first_day[1]), int(first_day[2]))



plt.plot(data['Date'],data['Adj Close'])
fig.autofmt_xdate()
plt.title('Timing of investments shown against SPY')
plt.ylabel('SPY price USD')
plt.legend()
plt.savefig('BuyHighSellLow.png', dpi=420)
