#!/usr/bin/python
#This file takes a text file with a list of stocks grouped by size, and
#saves group objects for each of the groups as .pkl files. The .pkl files
#can then be used by other scripts that need access to the data
#Only run this script when the saved objects need updated

import yahoo_finance as yf
from optparse import OptionParser
import Group
import object_saver

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
			help="write report to FILE")
(options,args) = parser.parse_args()

filename = options.filename
fd = open(filename, "rb")

groups = []
current_group = None
for line in fd:
	#print line
	if line[0] == '-':
		splitline = line[1:].split(',')
		name = splitline[0]
		low = splitline[1]
		high = splitline[2]
		current_group = Group.Group(name,low,high)
		groups.append(current_group)

	else:
		splitline = line.split(',')
		print splitline
		try:
			share = yf.Share(splitline[0])
			current_group.addShare(splitline[0], share)
		except TypeError:
			print "Type error on: " , splitline[0]
		except AttributeError:
			print "Attribute error on: " , splitline[0]
fd.close()


for group in groups:
	fname = group.name + ".pkl"
	object_saver.save(fname, group)
