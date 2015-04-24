#!/usr/bin/python
import numpy as np

from object_saver import load
from analysis import train, test
from optparse import OptionParser

group_strings = ['large', 'medium', 'small']
train_start = "2014-04-01"
train_end = "2014-09-30"
test_start = "2014-10-01"
test_end = "2015-03-31"
#alg_type = "linear"
#alg_type = "logistic"
alg_type = "svm"

def main():
	parser = OptionParser()
	parser.add_option("-o", "--output", dest="outfile",
				help="csv filename for output")

	(options, args) = parser.parse_args()
#	print "Options: " + str(options.outfile)

	writeToFile = False	
	if options.outfile != None:
		writeToFile = True
	
	filename = options.outfile
	fd = open(filename, "wb")
	fd.write("type,name,prediction\n")

	
	objects = []
	for s in group_strings:
		objects.append( load(s + ".pkl"))
	
#	groups = []
#	for o in objects:
#		groups.append(o.getShares())

	group_prediction = []
	for g in objects:
		prediction_percent = []
		for share in g.getShares():
			#if share.get_info()['symbol'] != "INTU":
			#	continue
			model = train(share, train_start, train_end,alg_type)
			predict = test(share, test_start, test_end, model,alg_type)
			if model == None or predict == None:
				continue
			prediction_percent.append(predict)
			if writeToFile:
				fd.write("share," + share.get_info()['symbol'] + \
				 "," + str(predict) + "\n")
			print "Share: " + share.get_info()['symbol'] + \
					 "\tpredict: " + str(predict)
			
		avg = np.mean(prediction_percent)
		group_prediction.append(avg)
		if writeToFile:
			fd.write("group," + g.name + "," + str(avg) + "\n")
		print "Group: " + g.name + "\tpredict: " + str(avg) + "\n"

	fd.close()

if __name__ == "__main__":
	main()
