import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
hierarchy_file = dir_path + "/FieldOfStudyHierarchy.txt"
level_set = [set(),set(),set(),set()]

with open(hierarchy_file,"r") as fin:
	for line in fin:
		edge = line.split("\t")
		level_set[int(edge[1][1])].add(edge[0])
		level_set[int(edge[3][1])].add(edge[2])

with open(dir_path+"/fos_l0.txt","wb") as fout:
	pickle.dump(level_set[0],fout,pickle.HIGHEST_PROTOCOL)

with open(dir_path+"/fos_l1.txt","wb") as fout:
	pickle.dump(level_set[1],fout,pickle.HIGHEST_PROTOCOL)

with open(dir_path+"/fos_l2.txt","wb") as fout:
	pickle.dump(level_set[2],fout,pickle.HIGHEST_PROTOCOL)

with open(dir_path+"/fos_l3.txt","wb") as fout:
	pickle.dump(level_set[3],fout,pickle.HIGHEST_PROTOCOL)