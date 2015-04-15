import statistics as stats
from sklearn.svm import SVC
from pprint import pprint

period = 10

def getSVCArgs(share, start_date, end_date):
	
#	emas = stats.ema(data, period)[1]
	retry_count = 5
	while retry_count > 0:
		try:
			data = share.get_historical(start_date, end_date)
			features = stats.features(data)
			if len(features) == 0:
				print "analysis - getSVCArgs(): features is empty. Ticker: " + \
					share.get_info()['symbol']
				retry_count = retry_count - 1
				continue

			labels = stats.labels(data)
			del labels[len(features):]

			return [features, labels]
	
		except IndexError:
			print "analysis - getSVCArgs(): IndexError. Ticker: " + \
				share.get_info()['symbol']
			retry_count = retry_count - 1
			continue
		except KeyError:
			print "analysis - getSVCArgs(): KeyError. Ticker: " + \
				share.get_info()['symbol']
			retry_count = retry_count - 1
			continue

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

def trade(group, start_date, end_date, filename):
	writeToFile = False
	if filename != None:
		writeToFile = True
		fd = open(filename, "wb")
		fd.write("group," + group.name + "\n")
	else:
		fd = None
	
	trades = 0
	portfolio_value = 0.0
	start_money = 100000.00
	money = start_money
	models_with_args = []
	num_shares = len(group.models)
	
		
	for share, model in group.models.iteritems():
		args = getSVCArgs(share, start_date, end_date)
		hd = share.get_historical(start_date,end_date)
		models_with_args.append(\
			[model, args, 0, -1, share.get_info()['symbol'], hd]) \
			#model, X, shares owned,
			# buy (2) or sell (1)
	

	num_days = len(models_with_args[0][1][0])

	for i in range (num_days-1, -1, -1):
		#print "Day: " , str(num_days - i)
		#print "Money: " + str(money)
		#print models_with_args[0][5][i]
		portfolio_value = 0.00
		for ma in models_with_args:
			portfolio_value = portfolio_value + ma[2] * float(ma[5][i]['Open'])
		if writeToFile:
			fd.write("day," + str(num_days-i) + "," + \
				models_with_args[0][5][i]['Date'] + "\n")
			fd.write("value," + str(portfolio_value + money) + "\n")
				
		for ma in models_with_args:
		#	print "Share: " , str(ma[4]) , \
		#		"\tshares: " , str(ma[2])[0:6] ,\
		#		"\tprice: " , ma[5][i]['Open']
			fd.write(ma[4] + "," + str(ma[2]) + "," + ma[5][i]['Open']+ "\n")
		shares_to_buy = 0
		shares_to_sell = 0
		for ma in models_with_args:
			p = ma[0].predict(ma[1][0][i])
			#if ma[4] == 0:
			#	print ma[1][0][i]
			#	print "index: " , str(ma[4]) , "P: " , str(p)
			shares = ma[2]
			price = float(ma[5][i]['Open'])
			ma[3] = p
			if p == 2:
				shares_to_buy = shares_to_buy + 1
			else:
				ma[2] = 0
				transaction = shares*price
				money = money + transaction	
				trades = trades + 1
				#print "Selling " , str(shares) ,\
			#		" at " , price
		
#		for ma in models_with_args:
#			price = ma[1][2] #the close price
#			shares = ma[2]
#			buy_sell = ma[3]
#	
#			if buy_sell == 1: #sell
		invest_per_share = 0
		if shares_to_buy > 0:	
			invest_per_share = money / shares_to_buy
		
		for ma in models_with_args:
			price = float(ma[5][i]['Open']) #the close price
			shares = ma[2]
			buy_sell = ma[3]
	
			if buy_sell == 2: #buy
				buy_number = invest_per_share/price
				ma[2] = ma[2] + buy_number
				money = money - invest_per_share
				trades = trades + 1
				#print "Buying " , str(buy_number) ,\
			#		" at " , price
	for ma in models_with_args:
			#print ma[1]
			price = float(ma[5][0]['Close']) #the close price
			shares = ma[2]
			ma[2] = 0
			#print "Firesale"
			#print "Selling " , str(shares) ,\
			#	 " at " , price
			money = money + shares*price	
	fd.write(str(start_money) + "," + str(money) + "," + str(trades) + "\n")	
	return [start_money, money]		
