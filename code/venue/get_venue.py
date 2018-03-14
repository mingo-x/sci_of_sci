from zipfile import ZipFile
import json
import time
import pickle

dir_path = "/mnt/ds3lab/yanping/mag"

venue_set = set()
non_en_count = 0

for idx in range(9):
	with ZipFile(dir_path+"/data/mag_papers_"+str(idx)+".zip", "r") as myzip:
		zip_files = myzip.namelist()
		for file_name in zip_files:
			print("zip",idx,file_name)
			start_time = time.time()
			with myzip.open(file_name) as fin:
				for line in fin:
					a = json.loads(line.decode('utf-8'))
					if "venue" in a:
						if "lang" in a and a["lang"]!="en":
							non_en_count += 1
							continue
						venue_set.add(a["venue"])
			print(len(venue_set))
			end_time = time.time()
			print(end_time-start_time)

print("start writing out")
out_path = dir_path+"/data/venue.pkl"
with open(out_path,"wb") as fout:
	start_time = time.time()
	pickle.dump(venue_set,fout,pickle.HIGHEST_PROTOCOL)
	print(time.time()-start_time)
print("non english papers:",non_en_count)
