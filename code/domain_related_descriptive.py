'''
Sample codes for counting the number of papers in each domain (FOS)
'''
from zipfile import ZipFile
import json
import time
import pickle

dir_path = "/mnt/ds3lab/yanping/mag/"
venue_fos_mapping_path = dir_path+"data/venue_fos_l1.pkl"
fos_npaper_path = dir_path+"data/fos_npaper.txt"

with open(venue_fos_mapping_path,"rb") as fin: # load in the venue-fos mapping
	venue_fos_mapping = pickle.load(fin)

fos_npaper = {} # dictionary keeping the number of papers per fos
paper_en_with_venue_counter = 0

for idx in range(9): # 9 zipped packages in total
	with ZipFile(dir_path+"/data/mag_papers_"+str(idx)+".zip", "r") as myzip:
		zip_files = myzip.namelist() # get the list of file names inside one zipped package
		for file_name in zip_files:
			print("zip",idx,file_name)
			start_time = time.time()
			with myzip.open(file_name) as fin:
				for line in fin: # each line is a piece of json data
					a = json.loads(line.decode('utf-8')) # decode json
					if "lang" in a and a["lang"]!="en": # skip papers without tag "en"
						continue
					if "venue" in a:
						paper_en_with_venue_counter += 1
						venue = a["venue"]
						for fos in venue_fos_mapping[venue]: # one venue can be mapped to several FOSs
							if fos not in fos_npaper:
								fos_npaper[fos] = 0
							fos_npaper[fos] += 1
							print(fos, fos_npaper[fos])
			end_time = time.time()
			print("time",end_time-start_time,"#valid papers", paper_en_with_venue_counter)

# write out
with open(fos_npaper_path,"wb") as fout:
	for fos in fos_npaper:
		fout.write(fos+"\t"+str(fos_npaper[fos])+"\n")
