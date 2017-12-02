from zipfile import ZipFile
import json
import time

dir_path = "/mnt/ds3lab/yanping/mag"
total = 0
withfos = 0
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
					total += 1
					a = json.loads(line.decode('utf-8'))
					if "fos" in a:
						withfos += 1
					if a_count%100000==0:
						print(a_count,withfos,total,time.time()-start_time)
			end_time = time.time()
			print(end_time-start_time)
print(withfos,total)