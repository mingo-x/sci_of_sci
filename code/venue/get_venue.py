from zipfile import ZipFile
import json
import time

dir_path = "/mnt/ds3lab/yanping/mag"

venue_set = set()

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
						venue_set.add(a["venue"])
			print(len(venue_set))
			end_time = time.time()
			print(end_time-start_time)

print("start writing out")
out_path = dir_path+"/data/venue.txt"
fout = open(out_path,"w")
start_time = time.time()
for v in venue_set:
	fout.write(v+"\n")
print(time.time()-start_time)
fout.close()