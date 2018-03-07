import time
from zipfile import ZipFile
import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# build content
dir_path = "/mnt/ds3lab/yanping/mag"

content = []
for idx in range(2):
	with ZipFile(dir_path+"/data/mag_papers_"+str(idx)+".zip", "r") as myzip:
		zip_files = myzip.namelist()
		for file_name in zip_files:
			print("zip",idx,file_name)
			start_time = time.time()
			with myzip.open(file_name) as fin:
				for line in fin:
					a = json.loads(line.decode('utf-8'))
					if "abstract" in a:
						content.append(a["abstract"])
			end_time = time.time()
			print(end_time-start_time, len(content))