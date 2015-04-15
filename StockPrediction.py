#!/usr/bin/python

from object_saver import load
from analysis import train, test, trade
import numpy as np
from optparse import OptionParser

group_strings =  ['large', 'medium', 'small']
train_start = "2014-04-01"
train_end = "2014-09-30"
test_start = "2014-10-01"
test_end = "2015-03-21"

def main():
	parser = OptionParser()
	parser.add_option("-o", "--output", dest="outfile",
				help="csv filename for output")
	parser.add_option("-p", "--predict", action="store_true",
			dest="predict", default=False,
			help="Run prediction metrics")
	(options, args) = parser.parse_args()
#	print "Options: " + str(options.outfile)
#	print "Options:" + str(options.verbose)

	run_predict = options.predict
	writeToFile = False	
	if options.outfile != None:
		writeToFile = True
	
		filename = options.outfile
		fd = open(filename, "wb")
		fd.write("type,name,prediction\n")
	else:
		filename = None
		fd = None
	
	objects = []
	for s in group_strings:
		objects.append( load(s + ".pkl"))
	
#	groups = []
#	for o in objects:
#		groups.append(o.getShares())

	group_prediction = []
	for g in objects:
		prediction_percent = []

		retry_count = 5
		while retry_count > 0:
			try:
				for share in g.getShares():
					#if share.get_info()['symbol'] != "INTU":
					#	continue
					model = train(share, train_start, train_end)
					if model == None:
						continue
					g.addModel(share, model)
					if run_predict:
						predict = test(share, test_start, test_end, model)
						if predict == None:
							continue
					else:
						predict = 0	
					prediction_percent.append(predict)
					if writeToFile:
						fd.write("share," + share.get_info()['symbol'] + \
						 "," + str(predict) + "\n")
					try:
						print "Share: " + share.get_info()['symbol'] + \
							 "\tpredict: " + str(predict)
					except yf.YQLQueryError:
						print "StockPrediction - trying to print Share: \
						symbol prediction. Share: " + share.get_info() 
						raise
	
			except yf.YQLQueryError:
				print "StockPrediction - YQLQueryError on train and test. Share: \
						" + share.get_info()
				retry_count = retry_count - 1
				continue
			except: 
				print "StockPrediction - unexpectederror on train and test. Share: \
						" + share.get_info()
			 	retry_count = retry_count - 1
				if retry_count == 0:
					raise
				else:
					continue
			
			break
					
		avg = np.mean(prediction_percent)
		group_prediction.append(avg)
		if writeToFile:
			fd.write("group," + g.name + "," + str(avg) + "\n")
		print "Group: " + g.name + "\tpredict: " + str(avg) + "\n"

	if writeToFile:
		fd.close()

	for g in objects:
		[p1, p2] = trade(g, test_start, test_end, g.name + ".csv")
		print "Group: " , g.name + "\tstart: " , str(p1) \
				, "\tend: " , str(p2)
if __name__ == "__main__":
	main()
