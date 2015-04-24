import statistics as stats
import numpy as np
from pprint import pprint
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

period = 10

def getSVCArgs(share, start_date, end_date, alg_type):
	
	data = share.get_historical(start_date, end_date)
#	emas = stats.ema(data, period)[1]
	try:
	
		features = stats.features(data)
		if len(features) == 0:
			print "analysis - getSVCArgs(): features is empty. Ticker: " + \
				share.get_info()['symbol']
			return None
		
		labels = stats.labels(data, alg_type)		
		del labels[len(features):]

		features = np.array(features)
		labels = np.array(labels)
		return [features, labels]
	
	except IndexError:
		print "analysis - getSVCArgs(): IndexError. Ticker: " + \
			share.get_info()['symbol']
		return None
	except KeyError:
		print "analysis - getSVCArgs(): KeyError. Ticker: " + \
			share.get_info()['symbol']
		return None


def train(share, start_date, end_date, alg_type):
	
	svcargs = getSVCArgs(share, start_date, end_date, alg_type)
	if svcargs == None:
		print("None is returned in train")
		return None
	[feats, labels] = svcargs
	try:
		if(alg_type =="svm"):
			model =  SVC().fit(feats, labels)
		elif(alg_type =="linear"):
			model = LinearRegression().fit(feats,labels)
		elif(alg_type =="logistic"):
			model = LogisticRegression().fit(feats,labels)

	except ValueError:
		print "Value error in analysis - train() when running SVC().fit on feats: " + str(feats) + " with labels: " + str(labels)

	return model

def test(share, start_date, end_date, model,alg_type):
	svcargs = getSVCArgs(share, start_date, end_date,alg_type)
	if svcargs == None:
		print("None is returned in test")
		return None
	[feats, labels] = svcargs

	return model.score(feats, labels)	
