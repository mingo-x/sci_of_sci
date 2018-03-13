# cast l2/l3 fos to l1 fos
# suppose no l0 for now
import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_fos_path = dir_path+"/venue_fos.pkl"
fos_level_path = dir_path+"/fos_level.pkl"
fos_parent_path = dir_path+"/fos_parent.pkl"
out_path = dir_path+"/venue_fos_l1.pkl"

def get_l1_pa(fos,fos_pa,fos_level):
	pa = fos
	pa_level = fos_level[fos]
	while pa_level>1:
		if pa in fos_pa:
			new_p = fos_pa[fos]
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

	for v in venue_fos:
		# assume one fos per venue
		fos = venue_fos[v]
		if fos_level[fos]>1:
			l1_pa = get_l1_pa(fos,fos_pa,fos_level)
			if l1_pa == fos:
				print("WARNING: No L1 Parent",fos_level[fos])
			venue_fos[v] = l1_pa

	with open(out_path,"wb") as fout:
		pickle.dump(venue_fos,fout,pickle.HIGHEST_PROTOCOL)






