# naive version: jaccard of word
# further improvement: n-gram, stem

import json
import pickle

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_path = dir_path+"/venue.pkl"
fos_path = dir_path+"/FieldOfStudy.txt"
out_path = dir_path+"/venue_fos.pkl"

# jaccard similarity
def j_sim(venue,fos):
	return 1.0*len(venue & fos)/len(venue | fos)

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
			parts = line.split("\t")

			dic[parts[0]] = parts[1]
	return dic

# split string to set of words
def split(s):
	words = s.split(" ")
	word_set = set()
	for w in words:
		word_set.add(w)
	return word_set


if __name__ == "__main__":
	venues = load_venue(venue_path)
	foss = load_fos(fos_path)
	# turn fos string into set
	fos_sets = {}
	for key in foss:
		fos_sets[key] = split(foss[key])
	mapping = {}
	for venue in venues:
		best_score = 0.0
		best_fos = []
		venue_set = split(venue)
		res = {}
		# iterate over fos_sets
		for fos in fos_sets:
			score = j_sim(venue_set,fos_sets[fos])
			if score > best_score:
				best_score = score
				del best_fos[:]
				best_fos.append(fos)
			elif score == best_score and score != 0:
				best_fos.append(fos)
		if len(best_fos) == 0:
			print("WARNING: 0 FOS")
		elif len(best_fos) > 0:
			print("WARNING: more than 1 FOS")
		mapping[venue] = best_fos
		print(venue,)
		for f in best_fos:
			print(foss[f],)
		print()
	with open(out_path,"wb") as fout:
		pickle.dump(mapping,out_path,pickle.HIGHEST_PROTOCOL)

