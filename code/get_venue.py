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
			a_count = 0
			with myzip.open(file_name) as fin:
				for line in fin:
					a_count += 1
					a = json.loads(line.decode('utf-8'))
					if "venue" in a:
						venue_set.add(a["venue"])
					if a_count%100000==0:
						print(a_count,len(venue_set),time.time()-start_time)
			end_time = time.time()
			print(end_time-start_time)

print("start writing out")
out_path = dir_path+"/data/venue.txt"
fout = open(out_path,"w")
venue_count = 0
start_time = time.time()
for v in venue_set:
	venue_count += 1
	fout.write(v+"\n")
	if venue_count%100000==0:
		end_time = time.time()
		print(venue_count,end_time-start_time)
		start_time = time.time()
fout.close()