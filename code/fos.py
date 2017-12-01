from zipfile import ZipFile
import json
import time

dir_path = "/mnt/ds3lab/yanping/mag"

fos_set = set()

for idx in range(9):
	with ZipFile(dir_path+"/data/mag_papers_"+str(idx)+".zip", "r") as myzip:
		zip_files = myzip.namelist()
		for file_name in zip_files:
			print("zip",idx,file_name)
			start_time = time.time()
			a_count = 0
			with myzip.open(file_name) as fin:
				for line in myzip:
					a_count += 1
					a = json.loads(line)
					if "fos" in a:
						fos = a["fos"]
						for f in fos:
							fos_set.add(f)
					if a_count%1000000==0:
						print(a_count)
			end_time = time.time()
			print(end_time-start_time)

print("start writing out")
out_path = dir_path+"/data/fos.txt"
fout = open(out_path,"w")
fos_count = 0
start_time = time.time()
for f in fos_set:
	fos_count += 1
	fout.write(f+"\n")
	if fos_count%100000==0:
		end_time = time.time()
		print(fos_count,end_time-start_time)
		start_time = time.time()
fout.close()