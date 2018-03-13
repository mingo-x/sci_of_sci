from zipfile import ZipFile
import json
import time

dir_path = "/mnt/ds3lab/yanping/mag"

no_venue = 0
no_fos = 0
no_venue_and_fos = 0

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
					if "venue" not in a:
						no_venue += 1
						if "fos" not in a:
							no_fos += 1
							no_venue_and_fos += 1
					elif "fos" not in a:
						no_fos += 1
					if a_count%100000==0:
						print(a_count,time.time()-start_time, no_venue, no_fos, no_venue_and_fos)
			end_time = time.time()
			print(end_time-start_time)

print("no_venue", no_venue)
print("no_fos", no_fos)
print("no_venue_and_fos", no_venue_and_fos)