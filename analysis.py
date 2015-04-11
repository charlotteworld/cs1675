import statistics as stats
from sklearn.svm import SVC

period = 10

def getSVCArgs(share, start_date, end_date):
	
	data = share.get_historical(start_date, end_date)
	emas = stats.ema(data, period)[1]
	labels = stats.labels(data)
	del labels[len(emas):]

	feats = []
	for e in emas:
		feats.append([e])
	return [feats, labels]

def train(share, start_date, end_date):
	[feats, labels] = getSVCArgs(share, start_date, end_date)

	model =  SVC().fit(feats, labels)

	return model

def test(share, start_date, end_date, model):
	[feats, labels] = getSVCArgs(share, start_date, end_date)

	return model.score(feats, labels)	
