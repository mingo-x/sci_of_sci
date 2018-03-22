'''
build citation graph
id to index mapping
collect n_citation statistics
skip non-english papers
'''

from zipfile import ZipFile
import json
import time
import pickle

dir_path = "/mnt/ds3lab/yanping/mag"
paper_id_path = dir_path+"/paper_id.pkl"
citation_graph_path = dir_path+"/citation_graph.pkl"
n_citation_path = dir_path+"/n_citation.txt"
#paper_author_path = dir_path+"/paper_author.pkl" #[[]]

paper_id_dict = {}
citation_graph = []
n_citation = []
for idx in range(9):
	with ZipFile(dir_path+"/data/mag_papers_"+str(idx)+".zip", "r") as myzip:
		zip_files = myzip.namelist()
		for file_name in zip_files:
			print("zip",idx,file_name)
			start_time = time.time()
			with myzip.open(file_name) as fin:
				for line in fin:
					a = json.loads(line.decode('utf-8'))
					# skip non-english papers
					if "lang" in a and a["lang"]!="en":
						continue
					paper_id = a["id"]
					if paper_id not in paper_id_dict:
						paper_id_dict[paper_id] = len(paper_id_dict)
						citation_graph.append([])
						n_citation.append(-1)
					paper_idx = paper_id_dict[paper_id]
					#print("paper:",paper_id,paper_idx)
					if "references" in a:
						for r in a["references"]:
							# if a new paper is encountered, give it an index
							if r not in paper_id_dict:
								paper_id_dict[r] = len(paper_id_dict)
								citation_graph.append([])
								n_citation.append(-1)
								#print("ref:",r,paper_id_dict[r])
							citation_graph[paper_id_dict[r]].append(paper_idx)
					if "n_citation" in a:
						n_citation[paper_idx] = a["n_citation"]
			end_time = time.time()
			print(end_time-start_time,len(paper_id_dict))

print("start writing out")
with open(paper_id_path,"wb") as fout:
	pickle.dump(paper_id_dict,fout,pickle.HIGHEST_PROTOCOL)
with open(citation_graph_path,"wb") as fout:
	pickle.dump(citation_graph,fout,pickle.HIGHEST_PROTOCOL)
with open(n_citation_path,"wb") as fout:
	pickle.dump(n_citation,fout,pickle.HIGHEST_PROTOCOL)
