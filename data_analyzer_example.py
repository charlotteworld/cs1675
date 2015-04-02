from object_saver import load

groups = ['small', 'medium', 'large']
object_groups = []

for g in groups:
	object_groups.append(load(g + '.pkl'))

for og in object_groups:
	og.printShares()

 
