# naive version: jaccard of word
# further improvement: n-gram, stem

import json
import pickle
from stemming.porter2 import stem
from time import time
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.classify import textcat
#from nltk.stem import PorterStemmer

dir_path = "/mnt/ds3lab/yanping/mag/data"
venue_path = dir_path+"/venue.pkl"
fos_path = dir_path+"/FieldsOfStudy.txt"
out_path = dir_path+"/venue_fos.pkl"
fos_level_path = dir_path+"/fos_level.pkl"

# jaccard similarity
def j_sim(venue,fos):
	union = venue  | fos
	intersection = venue & fos
	if len(union)==0:
		return 0.0, len(intersection)
	else:
		return 1.0*len(intersection)/len(union), len(intersection)

def c_sim(venue,fos):
	intersection = venue & fos
	return len(intersection), len(intersection)

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
def split_and_stem(s,stopword,tknz,stemmer,prep_set):
	words = tknz.tokenize(s.lower())
	word_set = set()
	and_flag = False

	for w in words:
		if w in prep_set:
			and_flag = True
		if w in stopword:
			continue
		word_set.add(stemmer.stem(w))
	#print(len(words),len(word_set))
	return word_set, and_flag

def get_stopword():
	# stopwords
	stopword = stopwords.words("english")
	stopword.extend(["journal","journals","proceedings","conference","yearly","quarterly","monthly","weekly","research","studies","review","&",
		",",":","-",".","(",")","\\","/"])
	return stopword

if __name__ == "__main__":
	#ps = PorterStemmer()
	stemmer = SnowballStemmer("english", ignore_stopwords=True)
	stopword = get_stopword()
	tknz = TweetTokenizer()
	venues = load_venue(venue_path)
	foss = load_fos(fos_path)
	prep_set = set(["of","and","&","in","on"])
	cat = textcat.TextCat()
	# turn fos string into set
	fos_sets = {}
	for key in foss:
		fos_sets[key], and_flag = split_and_stem(foss[key],stopword,tknz,stemmer,prep_set)
		if len(fos_sets[key])==0:
			print(key)
	mapping = {}
	with open(fos_level_path,"rb") as fin:
		fos_level = pickle.load(fin)
	counter_0 = 0
	counter_1 = 0
	total = 0
	start_time = time()
	and_count = 0
	dup_count = 0
	many_count = 0
	prob_count = 0
	for venue in venues:
		prob_flag = False
		best_score = 0.0
		best_hit = 0
		best_fos = []
		venue_set, and_flag = split_and_stem(venue,stopword,tknz,stemmer,prep_set)
		if len(venue_set)==0:
			print(venue)
		if and_flag:
			and_count += 1
			prob_flag = True
		res = {}
		# iterate over fos_sets
		for fos in fos_sets:
			score, hit = j_sim(venue_set,fos_sets[fos])
			#score, hit = c_sim(venue_set,fos_sets[fos])
			if score > best_score or (score==best_score and hit>best_hit):
				best_score = score
				best_hit = hit
				del best_fos[:]
				best_fos.append(fos)
			elif score == best_score and score != 0:
				best_fos.append(fos)
		# check for duplicate
		dup_set = set()
		for fos in best_fos:
			if foss[fos] in dup_set:
				dup_count += 1
				prob_flag = True
				break
			else:
				dup_set.add(foss[fos])
		# too many foss
		if len(best_fos) > 4:
			many_count += 1
			prob_flag = True
		mapping[venue] = best_fos
		# zero fos
		if len(best_fos) == 0:
			counter_0 += 1
			prob_flag = True
		if prob_flag:
			prob_count += 1
		print("---",venue)
		for f in best_fos:
			print("***",f,foss[f])

		total += 1
		#if total == 1000:
		#	break
	print("0 FOS:",counter_0)
	print("too many FOSs:",many_count)
	print("duplicate FOSs:",dup_count)
	print("time:",time()-start_time)
	print("venue with \'and\':", and_count, "in total:", total)
	print("problematic venues:",prob_count)
	with open(out_path,"wb") as fout:
		pickle.dump(mapping,fout,pickle.HIGHEST_PROTOCOL)

