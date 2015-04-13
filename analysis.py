import statistics as stats
from sklearn.svm import SVC
from pprint import pprint

period = 10

def getSVCArgs(share, start_date, end_date):
	
	data = share.get_historical(start_date, end_date)
#	emas = stats.ema(data, period)[1]
	try:
		features = stats.features(data)
		if len(features) == 0:
			print "analysis - getSVCArgs(): features is empty. Ticker: " + \
				share.get_info()['symbol']
			return None

		labels = stats.labels(data)
		del labels[len(features):]

		return [features, labels]
	
	except IndexError:
		print "analysis - getSVCArgs(): IndexError. Ticker: " + \
			share.get_info()['symbol']
		return None
	except KeyError:
		print "analysis - getSVCArgs(): KeyError. Ticker: " + \
			share.get_info()['symbol']
		return None
def train(share, start_date, end_date):
	
	svcargs = getSVCArgs(share, start_date, end_date)
	if svcargs == None:
		return None
	[feats, labels] = svcargs
	try:
		model =  SVC().fit(feats, labels)
	except ValueError:
		print "Value error in analysis - train() when running SVC().fit on feats: " + str(feats) + " with labels: " + str(labels)

	return model

def test(share, start_date, end_date, model):
	svcargs = getSVCArgs(share, start_date, end_date)
	if svcargs == None:
		return None
	[feats, labels] = svcargs

	return model.score(feats, labels)	
