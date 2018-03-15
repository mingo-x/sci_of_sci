import pickle
dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_path = dir_path+"/venue.pkl"
fos_path = dir_path+"/FieldsOfStudy.txt"
venue_voc_path = dir_path+"/venue_voc.pkl"
fos_voc_path = dir_path+"/fos_voc.pkl"

# venue
venue_voc = {}
with open(venue_path,"rb") as fin:
	venue_set = pickle.load(fin)
	for v in venue_set:
		words = v.lower().split(" ")
		for w in words:
			venue_voc[w] += 1
print("###venue vocabulary")
for v in venue_voc:
	print(v,venue_voc[v])
with open(venue_voc_path,"wb") as fout:
	pickle.dump(venue_voc,fout,pickle.HIGHEST_PROTOCOL)

#fos
fos_voc = {}
with open(fos_path,"r") as fin:
	for line in fin:
		parts = line[:-1].split("\t")
		words = parts[1].lower().split(" ")
		for w in words:
			fos_voc[w] += 1
print("###fos vocabulary")
for f in fos_voc:
	print(f,fos_voc[f])
with open(fos_voc_path,"wb") as fout:
	pickle.dump(fos_voc,fout,pickle.HIGHEST_PROTOCOL)

# split string to set of words
def split_and_stem(s,stopword):
	words = s.lower().split(" ")
	word_set = set()
	
	for w in words:
		if w in stopword:
			continue
		word_set.add(stem(w))
	#print(len(words),len(word_set))
	return word_set