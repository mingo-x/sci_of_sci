# cast l2/l3 fos to l1 fos
import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_fos_path = dir_path+"/venue_fos.pkl"
fos_level_path = dir_path+"/fos_level.pkl"
fos_parent_path = dir_path+"/fos_parent.pkl"
out_path = dir_path+"/venue_fos_l1.pkl"
fos_path = dir_path+"/FieldsOfStudy.txt"

def get_pa(fos,fos_pa,fos_level,l):
	pas = fos_pa[fos]
	pa_level = fos_level[pas[0]]
	if pa_level>l:
		new_pas = set()
		for pa in pas:
			ppas = fos_pa[pa]
			for ppa in ppas:
				new_pas.add(ppa)
		new_pas = list(new_pas)
		print("l2 pa",fos,pas,new_pas)
		pas = new_pas
	return pas

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
			pas = [fos]
			if fos in fos_level and fos_level[fos]>1:
				pas = get_pa(fos,fos_pa,fos_level,1)
			cast_set.update(pas)
		#old_len = len(cast_set)
		if len(cast_set) == 0:
			counter_0 += 1
		elif len(cast_set) > 1:
			counter_1 += 1

		print("Venue:",v,len(venue_fos[v]),len(cast_set))
		mapping[v] = cast_set
		#print("FOS before casting:")
		for f in venue_fos[v]:
			print("----",fos_id[f])
		#print("FOS after casting")
		for f in cast_set:
			print("````",fos_id[f])

	print("no FOS:",counter_0)
	print("more than 1 FOS:",counter_1)
	with open(out_path,"wb") as fout:
		pickle.dump(mapping,fout,pickle.HIGHEST_PROTOCOL)






