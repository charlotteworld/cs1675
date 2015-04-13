from object_saver import load
import sys
import yahoo_finance as yf

start = "2014-04-01"
end = "2015-03-31"
def main():
	group_str = ['large', 'medium', 'small']

	objects = []
	for gs in group_str:
		objects.append(load(gs + ".pkl"))
	loader = 0
	for o in objects:
		for s in o.getShares():
			try:
				data = s.get_historical(start, end)
				if data[0]['Date'] == end and  \
					data[-1]['Date'] == start:
					print "Stock valid: " + \
						s.get_info()['symbol']
				else:
					print "STOCK INVALID: " + \
						s.get_info()['symbol']
			except yf.YQLQueryError:
				print "get_hist error on: " + \
					s.get_info()['symbol']
			except KeyError:
				print "KeyError on date: " + \
					s.get_info()['symbol']
			except:
				print "Unexpecter error", sys.exc_info()[0]
				raise
if __name__ == "__main__":
	main()
