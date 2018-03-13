# naive version: jaccard of word
# further improvement: n-gram, stem

import json

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_path = dir_path+"/venue.txt"
fos_path = dir_path+"/fos.txt"
out_path = dir_path+"/venue_fos.json"

# jaccard similarity
def j_sim(venue,fos):
	return 1.0*len(venue & fos)/len(venue | fos)

# load venues/foss
def load_dict(path):
	dict = []
	with open(path,"r") as fin:
		for line in fin:
			dict.append(line)
	return dict


# split string to set of words
def split(s):
	words = s.split(" ")
	word_set = set()
	for w in words:
		word_set.add(w)
	return word_set


if __name__ == "__main__":
	venues = load_dict(venue_path)
	foss = load_dict(fos_path)
	# turn fos string into set
	fos_sets = {}
	for fos in foss:
		fos_sets[fos] = split(fos)
	fout = open(out_path,"w")
	for venue in venues:
		best_score = 0.0
		best_fos = []
		venue_set = split(venue)
		res = {}
		res["venue"] = venue
		# iterate over fos_sets
		for fos in fos_sets:
			score = j_sim(venue_set,fos_sets[fos])
			if score > best_score:
				best_score = score
				del best_fos[:]
				best_fos.append(fos)
			elif score == best_score:
				best_fos.append(fos)
		if len(best_fos) == 0:
			print("WARNING: 0 FOS")
		res["fos"] = best_fos
		fout.write(json.dumps(res))
		print(venue,best_fos)
	fout.close()

