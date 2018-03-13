# cast l2/l3 fos to l1 fos
# suppose no l0 for now
import pickle
import json

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_fos_path = dir_path+"/venue_fos.json"

if __name__ == "__main__":
	# load fos by level
	with open(dir_path+"/fos_l0.pkl","rb") as fin:
		fos_l0 = pickle.load(fin)
	with open(dir_path+"/fos_l1.pkl","rb") as fin:
		fos_l1 = pickle.load(fin)
	with open(dir_path+"/fos_l2.pkl","rb") as fin:
		fos_l2 = pickle.load(fin)
	with open(dir_path+"/fos_l3.pkl","rb") as fin:
		fos_l3 = pickle.load(fin)

	with open(venue_fos_path,"r") as fin:
		for line in fin:
			mapping = json.loads(line)
			new_fos = []
			for fos in mapping["fos"]:
				if fos in fos_l2 or fos in fos_l3:

				else:
					new_fos.append(fos)




