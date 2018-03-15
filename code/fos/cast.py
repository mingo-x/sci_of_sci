# cast l2/l3 fos to l1 fos
import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_fos_path = dir_path+"/venue_fos.pkl"
fos_level_path = dir_path+"/fos_level.pkl"
fos_parent_path = dir_path+"/fos_parent.pkl"
out_path = dir_path+"/venue_fos_l1.pkl"
fos_path = dir_path+"/FieldsOfStudy.txt"

def get_pa(fos,fos_pa,fos_level,l):
	pa = fos
	pa_level = fos_level[fos]
	while pa_level>l:
		if pa in fos_pa:
			new_p = fos_pa[pa]
			pa = new_p[0]
			pa_level = new_p[1]
		else:
			break
	return pa

def load_fos(path):
	dic = {}
	with open(path,"r") as fin:
		for line in fin:
			parts = line[:-1].split("\t")
			dic[parts[0]] = parts[1]
	return dic


if __name__ == "__main__":
	with open(fos_level_path,"rb") as fin:
		fos_level = pickle.load(fin)

	with open(venue_fos_path,"rb") as fin:
		venue_fos = pickle.load(fin)

	with open(fos_parent_path,"rb") as fin:
		fos_pa = pickle.load(fin)

	fos_id = load_fos(fos_path)
	counter_0 = 0
	counter_1 = 1
	mapping = {}
	for v in venue_fos:
		cast_set = set()
		for fos in venue_fos[v]:
			pa = fos
			if fos in fos_level and fos_level[fos]>1:
				pa = get_pa(fos,fos_pa,fos_level,1)
			cast_set.add(pa)
		#old_len = len(cast_set)
		if len(cast_set) == 0:
			counter_0 += 1
		elif len(cast_set) > 1:
			counter_1 += 1
			# further up-casting to l0
			'''
			print("---double casting---")
			cast_set = set()
			for fos in venue_fos[v]:
				pa = fos
				if fos in fos_level and fos_level[fos]>0:
					pa = get_pa(fos,fos_pa,fos_level,0)
				cast_set.add(pa)
			if len(cast_set) > 1:
				counter_1 += 1
			'''
		print("******",v,len(venue_fos[v]),len(cast_set))
		mapping[v] = cast_set
		for f in venue_fos[v]:
			print("``````",fos_id[f])
		for f in cast_set:
			print("------",fos_id[f])

	print("no FOS:",counter_0)
	print("more than 1 FOS:",counter_1)
	with open(out_path,"wb") as fout:
		pickle.dump(mapping,fout,pickle.HIGHEST_PROTOCOL)






