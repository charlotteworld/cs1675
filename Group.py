#import yahoo_finance

class Group:
        def __init__(self,name,low,high):
                self.name = name
                self.low = low
                self.high = high
                self.shares = []

        def addShare(self, share):
                self.shares.append(share)

	def printShares(self):
		for share in self.shares:
			print share.get_info()
