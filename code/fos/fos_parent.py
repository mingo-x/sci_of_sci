import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
hierarchy_file = dir_path + "/FieldOfStudyHierarchy.txt"
fos_path = dir_path+"/FieldsOfStudy.txt"
out_file = dir_path+"/fos_parent.pkl"

def get_hierarchy(path):
	pas = {}
	with open(path,"r") as fin:
		for line in fin:
			edge = line.split("\t")
			c_level = int(edge[1][1])
			if c_level<=1:
				continue
			p_level = int(edge[3][1])
			c_id = edge[0]
			p_id = edge[2]
			weight = float(edge[4])
			if c_id in pas:
				old_p_level = pas[c_id][1]
				old_weight = pas[c_id][2]

				if (p_level<old_p_level and p_level>=1) or (p_level==old_p_level and weight>old_weight):
					# update highest and heaviest parent
					pas[c_id] = (p_id,p_level,weight)
			else:
				pas[c_id] = (p_id,p_level,weight)
	return pas

def load_fos(path):
	dic = {}
	with open(path,"r") as fin:
		for line in fin:
			parts = line[:-1].split("\t")
			dic[parts[0]] = parts[1]
	return dic

def read_hierarchy(path,fos_dic):
	hie = [{},{},{}]
	with open(path,"r") as fin:
		for line in fin:
			edge = line.split("\t")
			c_id = edge[0]
			p_id = edge[2]
			c_level = int(edge[1][1])
			p_level = int(edge[3][1])
			if c_id in hie[p_level]:
				hie[p_level][c_id].append(p_id)
			else:
				hie[p_level][c_id] = [p_id]
	pas = {}
	for fos in fos_dic:
		if fos in hie[1]:
			pas[fos] = hie[1][fos]
		elif fos in hie[0]:
			pas[fos] = hie[0][fos]
		elif fos in hie[2]:
			pas[fos] = hie[2][fos]
		else:
			pas[fos] = [fos]
	return pas



if __name__ == "__main__":
	fos_dic = load_fos(fos_path)
	pas = read_hierarchy(hierarchy_file,fos_dic)
	for fos in pas:
		print(fos,pas[fos])
	#pas = get_hierarchy(hierarchy_file)
	with open(out_file,"wb") as fout:
		pickle.dump(pas,fout,pickle.HIGHEST_PROTOCOL)

	
