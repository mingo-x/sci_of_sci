dir_path = "../MAG/"
hierarchy_file = dir_path + "FieldOfStudyHierarchy.txt"
fos_set = set()
level_count = [0,0,0,0]

with open(hierarchy_file,"r") as fin:
	for line in fin:
		edge = line.split("\t")
		if edge[0] not in fos_set:
			fos_set.add(edge[0])
			level_count[int(edge[1][1])] += 1
		if edge[2] not in fos_set:
			fos_set.add(edge[2])
			level_count[int(edge[3][1])] += 1

for c in level_count:
	print(c)

