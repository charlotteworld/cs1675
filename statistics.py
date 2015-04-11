#This file contains functions for calculating the simple moving average
#and the exponential moving average over a period of time for one share

from object_saver import load
from pprint import pprint
import sys


#This function calculates the simple moving average for a single date
#params
#	hist_data - the yahoo_finance historical data for a single stock
#	period - an int for the number of days to calculate the moving average
#	start - an index into the hist_data array for the date to calculate on
#returns
#	float - the simple moving average
def sma_from_start(hist_data, period, start):
	running_sum = 0.0
	for i in range(0, period):
		running_sum = running_sum + float(hist_data[start + i]['Close'])
	sma = running_sum / period	
	return sma

#This function calculates the simple moving averages for each day in a set of historical data for a given stock
#params
#	hist_data - the yahoo_finance historical data for a single stock
#	period - an into for the number of days to calculate the moving average
#returns
#	dictionary(date, sma) - the simple moving average for each date in hist_data	
def sma(hist_data, period):
	smas = {}
	start = len(hist_data) - period
	while start >= 0:
		smas[hist_data[start]['Date']] = sma_from_start(hist_data, period, start)
		start = start - 1
	return smas

#This function calculates the exponential moving average for each day in a set of historical data for a given stock
#params
#	hist_data - the yahoo_fiance historical data for a single stock
#	period - an int for the number of days for the average
#	date - optional string argument to specify a single date desired. Format as YYYY-MM-DD
#returns
#	[dictionary(date, ema), array(ema)] - the exponential moving average for each
#					 date in hist_data. The array is in order from
#					most recent to oldest date
#def ema(hist_data, period, date = None):
def ema(*arg):
	hist_data = arg[0]
	period = arg[1]
	emas_dict = {}
	emas_array = []
	if len(arg) == 2:
		start = len(hist_data) - period
		loop_end = 0
	else:
		date = arg[2]
		start = 0
		for s in hist_data:
			if s['Date'] == date:
				break;
			start = start + 1 
		if start == len(hist_data):
			print("Error: That date does not exist in the historical data provided. Function terminating.")
			sys.exit()
		loop_end = start
		print "start: " + str(start)
	multiplier = 2.0 / (period + 1)
#	print "Multiplier: " + str(multiplier)
	previous_day_ema = sma_from_start(hist_data, period, start)
#	print "First ema: " + str(previous_day_ema) + " at start: " + str(start)
	while start >= loop_end:
		new_ema = (float(hist_data[start]['Close']) - previous_day_ema) * multiplier + previous_day_ema
		emas_dict[hist_data[start]['Date']]  = new_ema
		emas_array.append(new_ema)
		previous_day_ema = new_ema
		start = start - 1

	emas_array.reverse()
	return [emas_dict, emas_array]

def labels(hist_data):
	y = [0]*(len(hist_data)-1)
	
	for i in range(0, len(y)):
		if hist_data[i]['Close'] >= hist_data[i+1]['Close']:
			y[i] = 1
		else:
			y[i] = -1

	return y

def main():
	largegroup = load('large.pkl')

	tickers = largegroup.getTickers()

	first_share = largegroup.shares[tickers[0]]

	hist_data = first_share.get_historical('2014-04-01', '2014-04-29')
	smas = sma(hist_data, 10)
	[emas, emas_array] = ema(hist_data, 10)
	print "Simple Moving Averages"
	for date in smas:
		print date + ": " + str(smas[date])
	
	print "\nExponential Moving Averages"
	for date in emas:
		print date + ": " + str(emas[date])
	#pprint(hist_data)

	for v in emas_array:
		print str(v)

if __name__ == "__main__":
	main()
