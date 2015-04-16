#starting date, ending date

import io 
import sys

from object_saver import load
from statistics import ema
from yahoo_finance import Share


def main(start_date, end_date, printValue):
	# ewma = pandas.stats.moments.ewma
	# yahoo = Share('YHOO')
	try:
		#groups = ['small', 'medium', 'large']
		groups = [ 'large']
		object_groups = []

		#yahoo = Share('YHOO')
		#print yahoo.get_historical('2014-04-25', '2014-04-29')
		#print sys.argv[1], sys.argv[2]
		for g in groups:
			object_groups.append(load(g + '.pkl'))

		file_object = open("raw_data.txt","w+" )

		X_label = [None]*10
		Y_label = [None]*10
		i = 0
		for small_g in object_groups:
			for share in small_g.shares:
				# print share
				X_label[i] = []
				Y_label[i] = []
				data_list = small_g.shares[share].get_historical(start_date, end_date)
				for index in range(len(data_list)):
					file_object.write('Symbol: '+str(data_list[index]['Symbol'])+ ' Date : '+str(data_list[index]['Date']) + ' Volume: '+str(data_list[index]['Volume']) + ' Open : '+str(data_list[index]['Open']) + ' Close : '+str(data_list[index]['Close']) + ' High : '+str(data_list[index]['High']) + ' Low : '+str(data_list[index]['Low'])+ ' Adj_Close : '+str(data_list[index]['Adj_Close']) + "\n")
					if( index < (len(data_list)-9) ):
						X_label[i].append([ data_list[index]['Volume'],data_list[index]['Open'],data_list[index]['Close'],data_list[index]['High'],data_list[index]['Low'],data_list[index]['Adj_Close'], ema(data_list, 10, data_list[index]['Date'])[1][0]])					
						j = index - 1
						if data_list[index]['Close'] <= data_list[j]['Close']:
							Y_label[i].append(1)
						if data_list[index]['Close'] > data_list[j]['Close']:
							Y_label[i].append(2)
				i=+1
		if(printValue):
			print X_label[0]
			print Y_label[0]
		else:
			return [X_label, Y_label]
				#print(data_list[index])
	# data_list = yahoo.get_historical('2014-04-25', '2014-05-29')
	except IOError:
   		print "Error: can\'t find file or read data"
	else:
  		print "Written content in the file successfully"
  		file_object.close() 
		
#def getData():
	

if __name__ == "__main__": main( str(sys.argv[1]), str(sys.argv[2]),True) 
