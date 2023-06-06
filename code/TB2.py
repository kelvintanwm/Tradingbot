import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

stock = input("Enter a stock symbol ticker:")
print(stock)

start_year = 2020
start_month = 1
start_day = 1

start = dt.datetime(start_year,start_month,start_day)

now = dt.datetime.now()

df = pdr.get_data_yahoo(stock,start,now)

print(df)

# ma = 50

# sma_string = "Sma_{}".format(str(ma))


# # Creating moving average using dataframe
# df[sma_string] = df.iloc[:,4].rolling(window = ma).mean()

# print(df)

# df = df.iloc[ma:]

# print(df)

emas_used = [8,19,21,39]

for x in emas_used:
	ema = x
	df["Ema_{}".format(ema)] = round(df.iloc[:,4].ewm(span = ema, adjust = False).mean(),2)


df["MACD"] = df["Ema_8"] - df["Ema_21"]
df["SMACD"] = df["Ema_19"] - df["Ema_39"]
df["signal1"] = round(df.iloc[:,10].ewm(span = 9, adjust = False).mean(),2)
df["signal2"] = round(df.iloc[:,11].ewm(span = 9, adjust = False).mean(),2)
print(df.head(13))


pos = 0 # 0 will signal no position while 1 will signal position
num = 0
percent_change = []

for i in df.index:

	#cmin = min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i])
	#cmax = max(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i])
	
	close = df["Adj Close"][i]
	# opens = df["Open"][i]

	if(df["signal1"][i] > df["MACD"][i]):
		print("Signal line above MACD")
		if pos == 0:
			bp = close
			pos = 1
			print("Buying now at "+str(bp))

	elif(df["signal2"][i] < df["SMACD"][i]):
		print("Signal line below SMACD")
		if pos == 1:
			pos = 0
			sp = close
			print("Selling now at "+str(sp))
			pc = (sp/bp -1)*100
			percent_change.append(pc)

	if (num == df["Adj Close"].count()-1 and pos ==1 ):
		pos = 0
		sp = close
		print("Selling now at "+str(sp))
		pc = (sp/bp -1)*100
		percent_change.append(pc)

	num +=1

print(percent_change)


# Effectiveness of the trading strategy

gains = 0
gain_count = 0
losses = 0
loss_count = 0
no_round = 1

for i in percent_change:
	if (i>0):
		gains += i
		gain_count +=1
	else:
		losses += i
		loss_count +=1
	no_round = no_round*((i/100)+1)

no_round = round((no_round-1)*100,2)

if (gain_count>0):
	avg_gain = gains/gain_count
	max_gain = str(max(percent_change))
else:
	avg_gain = 0
	max_gain = "undefined"

if (loss_count>0):
	avg_loss = losses/loss_count
	max_loss = str(min(percent_change))
	ratio = str(-avg_gain/avg_loss)
else:
	avg_loss = 0
	max_loss = "undefined"
	ratio = "infinite"

if (gain_count > 0 or loss_count>0):
	batting_avg = gain_count/(gain_count+loss_count)
else:
	batting_avg = 0

print()
print("Results for "+ stock +" going back to "+str(df.index[0])+", Sample size: "+str(gain_count+loss_count)+" trades")
print("EMAs used: "+str(emas_used))
print("Batting Avg: "+ str(batting_avg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avg_gain))
print("Average Loss: "+ str(avg_loss))
print("Max Return: "+ max_gain)
print("Max Loss: "+ max_loss)
print("Total return over "+str(gain_count+loss_count)+ " trades: "+ str(no_round)+"%" )
#print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()