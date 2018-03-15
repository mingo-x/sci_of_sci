import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
hierarchy_file = dir_path + "/FieldOfStudyHierarchy.txt"
out_file = dir_path+"/fos_parent.pkl"

def get_hierarchy(path):
	pas = {}
	with open(path,"r") as fin:
		for line in fin:
			edge = line.split("\t")
			c_level = int(edge[1][1])
			#if c_level<=1:
			#	continue
			p_level = int(edge[3][1])
			c_id = edge[0]
			p_id = edge[2]
			weight = float(edge[4])
			if c_id in pas:
				old_p_level = pas[c_id][1]
				old_weight = pas[c_id][2]

				# if fos has an l1 parent, don't go further to l0
				if (p_level<old_p_level and old_p_level!=1) or (p_level==old_p_level and weight>old_weight):
					# update highest and heaviest parent
					pas[c_id] = (p_id,p_level,weight)
			else:
				pas[c_id] = (p_id,p_level,weight)
	return pas

if __name__ == "__main__":
	pas = get_hierarchy(hierarchy_file)
	with open(out_file,"wb") as fout:
		pickle.dump(pas,fout,pickle.HIGHEST_PROTOCOL)

	
