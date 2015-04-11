from object_saver import load
from analysis import train, test
import numpy as np

group_strings = ['large', 'medium']
train_start = "2014-04-01"
train_end = "2014-09-30"
test_start = "2014-10-01"
test_end = "2015-03-31"

def main():
	objects = []
	for s in group_strings:
		objects.append( load(s + ".pkl"))
	
	groups = []
	for o in objects:
		groups.append(o.getShares())

	group_prediction = []
	for g in objects:
		prediction_percent = []
		for share in g.getShares():
			model = train(share, train_start, train_end)
			predict = test(share, test_start, test_end, model)
			prediction_percent.append(predict)
			print "Share: " + share.get_info()['symbol'] + "\tpredict: " + str(predict)
		avg = np.mean(prediction_percent)
		group_prediction.append(avg)
		print "Group: " + g.name + "\tpredict: " + str(avg) + "\n"

if __name__ == "__main__":
	main()
