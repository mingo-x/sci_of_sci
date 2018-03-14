# cast l2/l3 fos to l1 fos
import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_fos_path = dir_path+"/venue_fos.pkl"
fos_level_path = dir_path+"/fos_level.pkl"
fos_parent_path = dir_path+"/fos_parent.pkl"
out_path = dir_path+"/venue_fos_l1.pkl"

def get_pa(fos,fos_pa,fos_level):
	pa = fos
	pa_level = fos_level[fos]
	while pa_level>1:
		if pa in fos_pa:
			new_p = fos_pa[pa]
			pa = new_p[0]
			pa_level = new_p[1]
		else:
			break
	return pa

if __name__ == "__main__":
	with open(fos_level_path,"rb") as fin:
		fos_level = pickle.load(fin)

	with open(venue_fos_path,"rb") as fin:
		venue_fos = pickle.load(fin)

	with open(fos_parent_path,"rb") as fin:
		fos_pa = pickle.load(fin)

	counter_0 = 0
	counter_1 = 1
	mapping = {}
	for v in venue_fos:
		cast_set = set()
		for fos in venue_fos[v]:
			pa = fos
			if fos_level[fos]>1:
				pa = get_pa(fos,fos_pa,fos_level)
			cast_set.add(pa)
		if len(cast_set) == 0:
			counter_0 += 1
		elif len(cast_set) > 1:
			counter_1 += 1
			#print("WARNING: more than 1 FOS")
		print("******",v,len(cast_set))
		mapping[v] = cast_set

	with open(out_path,"wb") as fout:
		pickle.dump(mapping,fout,pickle.HIGHEST_PROTOCOL)






