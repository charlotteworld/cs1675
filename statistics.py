from object_saver import load
from pprint import pprint


def sma_from_start(hist_data, period, start):
	running_sum = 0.0
	for i in range(0, period):
		running_sum = running_sum + float(hist_data[start + i]['Close'])
	sma = running_sum / period	
	return sma
	
def sma(hist_data, period):
	smas = {}
	start = len(hist_data) - period
	while start >= 0:
		smas[hist_data[start]['Date']] = sma_from_start(hist_data, period, start)
		start = start - 1
	return smas
def ema(hist_data, period):
	emas = {}
	start = len(hist_data) - period
	multiplier = 2.0 / (period + 1)
#	print "Multiplier: " + str(multiplier)
	previous_day_ema = sma_from_start(hist_data, period, start)
#	print "First ema: " + str(previous_day_ema) + " at start: " + str(start)
	while start >= 0:
		new_ema = (float(hist_data[start]['Close']) - previous_day_ema) * multiplier + previous_day_ema
		emas[hist_data[start]['Date']]  = new_ema
		previous_day_ema = new_ema
		start = start - 1

	return emas

def main():
	largegroup = load('large.pkl')

	tickers = largegroup.getTickers()

	first_share = largegroup.shares[tickers[0]]

	hist_data = first_share.get_historical('2014-04-01', '2014-04-29')
	smas = sma(hist_data, 10)
	emas = ema(hist_data, 10)
	print "Simple Moving Averages"
	for date in smas:
		print date + ": " + str(smas[date])
	
	print "\nExponential Moving Averages"
	for date in emas:
		print date + ": " + str(emas[date])
	#pprint(hist_data)

if __name__ == "__main__":
	main()
