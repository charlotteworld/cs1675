#This file can be used to save and load python objects
import cPickle as pickle

#Save - saves a python object to a pickle file
#params
#	name - the file name to save the object to
#	obj - the python object to be saved
#returns
#	no return
def save(name, obj):
	with open(name, 'wb') as output:
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

#load - loads a python object from a pickle file
#params
#	name - the file to load the object from
#returns
#	a python object
def load(name):
	with open(name, 'rb') as input:
		return pickle.load(input)
