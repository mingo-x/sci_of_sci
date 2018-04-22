from pymongo import MongoClient
from zipfile import ZipFile
import json
import time
import pickle

client = MongoClient()
db = client.mag
papers = db.papers
dir_path = "/mnt/ds3lab/yanping/mag/"

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
					_id = papers.insert_one(a)
					print(_id)
						
			end_time = time.time()
			print("time",end_time-start_time)