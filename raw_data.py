import io 
import sys
from object_saver import load
from yahoo_finance import Share

def main():
	# ewma = pandas.stats.moments.ewma
	# yahoo = Share('YHOO')
	try:
		groups = ['small', 'medium', 'large']
		object_groups = []

		for g in groups:
			object_groups.append(load(g + '.pkl'))

		file_object = open("raw_data.txt","w+" )
		for small_g in object_groups:
			for share in small_g.shares:
				data_list = share.get_historical(str(sys.argv[1]), str(sys.argv[2]))
				for index in range(len(data_list)):
					file_object.write('Symbol: '+str(data_list[index]['Symbol'])+ ' Date : '+str(data_list[index]['Date']) + ' Volume: '+str(data_list[index]['Volume']) + ' Close : '+str(data_list[index]['Close']) +"\n")
				#print(data_list[index])
	# data_list = yahoo.get_historical('2014-04-25', '2014-05-29')
	except IOError:
   		print "Error: can\'t find file or read data"
	else:
  		print "Written content in the file successfully"
  		file_object.close() 

if __name__ == "__main__": main()
