import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
hierarchy_file = dir_path + "/FieldOfStudyHierarchy.txt"
level = {}

with open(hierarchy_file,"r") as fin:
	for line in fin:
		edge = line.split("\t")
		level[edge[0]] = int(edge[1][1])
		level[edge[2]] = int(edge[3][1])

with open(dir_path+"/fos_level.pkl","wb") as fout:
	pickle.dump(level,fout,pickle.HIGHEST_PROTOCOL)

