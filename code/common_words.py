import pickle
import operator
from nltk.tokenize import TweetTokenizer
dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_path = dir_path+"/venue.pkl"
fos_path = dir_path+"/FieldsOfStudy.txt"
venue_voc_path = dir_path+"/venue_voc.pkl"
fos_voc_path = dir_path+"/fos_voc.pkl"

tknz = TweetTokenizer()
# venue
venue_voc = {}
with open(venue_path,"rb") as fin:
	venue_set = pickle.load(fin)
	for v in venue_set:
		words = tknz.tokenize(v.lower())
		for w in words:
			if w in venue_voc:
				venue_voc[w] += 1
			else:
				venue_voc[w] = 1
print("###venue vocabulary")
for key, value in sorted(venue_voc.items(), key= operator.itemgetter(1)):
	print(key,value)
with open(venue_voc_path,"wb") as fout:
	pickle.dump(venue_voc,fout,pickle.HIGHEST_PROTOCOL)

#fos
fos_voc = {}
with open(fos_path,"r") as fin:
	for line in fin:
		parts = line[:-1].split("\t")
		words = tknz.tokenize(parts[1].lower())
		for w in words:
			if w in fos_voc:
				fos_voc[w] += 1
			else:
				fos_voc[w] = 1
print("###fos vocabulary")
for key, value in sorted(fos_voc.items(), key= operator.itemgetter(1)):
	print(key,value)
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