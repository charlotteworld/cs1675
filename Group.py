#import yahoo_finance

class Group:
        def __init__(self,name,low,high):
                self.name = name
                self.low = low
                self.high = high
                self.shares = {}

        def addShare(self, ticker, share):
                self.shares[ticker] = share

	def printShares(self):
		for ticker in self.shares:
			print self.shares[ticker].get_info()

	def getTickers(self):
		tickerlist = []
		for ticker in self.shares:
			tickerlist.append(ticker)

		return tickerlist
