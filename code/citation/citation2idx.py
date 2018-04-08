'''
transform citation relationship into index-based form
'''

from zipfile import ZipFile
import json
import time
import pickle

dir_path = "/mnt/ds3lab/yanping/mag"
paper_id_path = dir_path+"/paper_id.pkl"
citation_idx_path = dir_path+"/citation_indexed.txt"

id_idx_dict = {}
edge_count = 0
fout = open(citation_idx_path,"wb")
for idx in range(9):
	with ZipFile(dir_path+"/data/mag_papers_"+str(idx)+".zip", "r") as myzip:
		zip_files = myzip.namelist()
		for file_name in zip_files:
			print("zip",idx,file_name)
			start_time = time.time()
			with myzip.open(file_name) as fin:
				for line in fin:
					a = json.loads(line.decode('utf-8'))
					# skip non-english papers or save english paper??? (because some papers may not have "lang" tag)
					if "lang" in a and a["lang"]!="en":
						continue
					paper_id = a["id"]
					if paper_id not in id_idx_dict:
						id_idx_dict[paper_id] = len(id_idx_dict)
					output_line = str(id_idx_dict[paper_id])
					if "references" in a:
						for r in a["references"]:
							# if a new paper is encountered, give it an index
							if r not in id_idx_dict:
								id_idx_dict[r] = len(id_idx_dict)
							output_line += ","+str(id_idx_dict[r])
						output_line += "\n"
						fout.write(output_line.encode('utf-8'))
						edge_count += len(a["references"])
						
			end_time = time.time()
			print("time",end_time-start_time,"#edges",edge_count)

fout.close()
print("start writing out")
with open(paper_id_path,"wb") as fout:
	pickle.dump(id_idx_dict,fout,pickle.HIGHEST_PROTOCOL)
