import cPickle as pickle

def save(name, obj):
	with open(name, 'wb') as output:
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load(name):
	with open(name, 'rb') as input:
		return pickle.load(input)
