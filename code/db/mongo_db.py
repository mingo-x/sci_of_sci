from pymongo import MongoClient, ASCENDING
from zipfile import ZipFile
import json
import time
import pickle

client = MongoClient()
db = client.mag
papers = db.papers
papers.create_index([('id', ASCENDING)], unique=True)
dir_path = "/mnt/ds3lab/yanping/mag/"
venue_fos_mapping_path = dir_path+"data/venue_fos_l1.pkl"

with open(venue_fos_mapping_path,"rb") as fin: # load in the venue-fos mapping
	venue_fos_mapping = pickle.load(fin)

bulk = []
for idx in range(1):
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
					if "venue" not in a:
						continue
					else:
						venue = a["venue"]
						a["domain"] = venue_fos_mapping[venue]
						bulk.append(a)
					
					if len(bulk) == 10:
						papers.insert_many(bulk)
						bulk = []
						
			end_time = time.time()
			print("time",end_time-start_time)

papers.insert_many(bulk)