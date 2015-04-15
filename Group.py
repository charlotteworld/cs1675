#import yahoo_finance

class Group:
        def __init__(self,name,low,high):
                self.name = name
                self.low = low
                self.high = high
                self.shares = {}
		self.models = {}
     
	def addModel(self, share, model):
		self.models[share] = model

  	def addShare(self, ticker, share):
                self.shares[ticker] = share

	def getShares(self):
		sharelist = []
		for ticker in self.shares:
			sharelist.append(self.shares[ticker])

		return sharelist

	def getTickers(self):
		tickerlist = []
		for ticker in self.shares:
			tickerlist.append(ticker)

		return tickerlist

	def printShares(self):
		for ticker in self.shares:
			print self.shares[ticker].get_info()


