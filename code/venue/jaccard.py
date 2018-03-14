# naive version: jaccard of word
# further improvement: n-gram, stem

import json
import pickle
from stemming.porter2 import stem
from time import time
from nltk.corpus import stopwords
#from nltk.stem import PorterStemmer

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_path = dir_path+"/venue.pkl"
fos_path = dir_path+"/FieldsOfStudy.txt"
out_path = dir_path+"/venue_fos.pkl"
fos_level_path = dir_path+"/fos_level.pkl"

# jaccard similarity
def j_sim(venue,fos):
	return 1.0*len(venue & fos)/len(venue | fos), len(venue & fos)

# load venues
def load_venue(path):
	dic = []
	with open(path,"rb") as fin:
		venue_set = pickle.load(fin)
		for v in venue_set:
			dic.append(v)
	return dic

def load_fos(path):
	dic = {}
	with open(path,"r") as fin:
		for line in fin:
			parts = line[:-1].split("\t")

			dic[parts[0]] = parts[1]
	return dic

# split string to set of words
def split_and_stem(s,stopword):
	words = s.lower().split(" ")
	word_set = set()
	
	for w in words:
		nw = stem(w)
		if nw in stopword:
			continue
		word_set.add(nw)
	print(len(words),len(word_set))
	return word_set


if __name__ == "__main__":
	#ps = PorterStemmer()
	stopword = stopwords.words("english")
	venues = load_venue(venue_path)
	foss = load_fos(fos_path)
	# turn fos string into set
	fos_sets = {}
	for key in foss:
		fos_sets[key] = split_and_stem(foss[key],stopword)
	mapping = {}
	with open(fos_level_path,"rb") as fin:
		fos_level = pickle.load(fin)
	counter_0 = 0
	counter_1 = 0
	total = 0
	start_time = time()
	for venue in venues:
		best_score = 0.0
		best_hit = 0
		best_fos = []
		venue_set = split_and_stem(venue,stopword)
		res = {}
		# iterate over fos_sets
		for fos in fos_sets:
			score, hit = j_sim(venue_set,fos_sets[fos])
			if score > best_score or (score==best_score and hit>best_hit):
				best_score = score
				best_hit = hit
				del best_fos[:]
				best_fos.append(fos)
			elif score == best_score and score != 0:
				best_fos.append(fos)
		mapping[venue] = best_fos
		if len(best_fos) == 0:
			counter_0 += 1
		elif len(best_fos) > 1:
			counter_1 += 1
		print("---",venue)
		for f in best_fos:
			print("***",f,foss[f])
		total += 1
		if total == 10000:
			break
	print("0 FOS:",counter_0)
	print("more than 1 FOS:",counter_1)
	print("time:",time()-start_time)
	with open(out_path,"wb") as fout:
		pickle.dump(mapping,out_path,pickle.HIGHEST_PROTOCOL)

