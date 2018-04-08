'''
build citation graph
id to index mapping
collect n_citation statistics
skip non-english papers
skip papers never cited
'''

import time
import pickle

dir_path = "/mnt/ds3lab/yanping/mag"
paper_cid_path = dir_path+"/paper_id.pkl"
citation_graph_path = dir_path+"/citation_graph.pkl"
citation_idx_path = dir_path+"/citation_indexed.txt"
#paper_author_path = dir_path+"/paper_author.pkl" #[[]]

paper_cid_dict = {}
citation_graph = []
edge_count = 0
with open(citation_graph_path,"rb") as fin:
	start_time = time.time()
	counter = 0
	for line in fin:
		terms = line.split(",")
		citer = line[0]
		for i in range(1,len(terms)): # for every citee
			citee = terms[i]
			if citee not in paper_cid_dict:
				paper_cid_dict[citee] = len(citation_graph)
				citation_graph.append([])
			citation_graph[paper_cid_dict[citee]].append(citer)
		counter += 1
		if counter%1000000 == 0:
			print("time",time.time()-start_time,"count",counter,"size",len(citation_graph))
			start_time = time.time()

print("start writing out")
with open(paper_cid_path,"wb") as fout:
	pickle.dump(paper_cid_dict,fout,pickle.HIGHEST_PROTOCOL)
with open(citation_graph_path,"wb") as fout:
	pickle.dump(citation_graph,fout,pickle.HIGHEST_PROTOCOL)
