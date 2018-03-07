from time import time
from zipfile import ZipFile
import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


dir_path = "/mnt/ds3lab/yanping/mag"
n_features = 1000
n_components = 300
n_top_words = 20

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

# build content
content = []
for idx in range(1):
	with ZipFile(dir_path+"/data/mag_papers_"+str(idx)+".zip", "r") as myzip:
		zip_files = myzip.namelist()
		for file_name in zip_files:
			print("zip",idx,file_name)
			start_time = time()
			with myzip.open(file_name) as fin:
				for line in fin:
					a = json.loads(line.decode('utf-8'))
					if "abstract" in a:
						content.append(a["abstract"])
			end_time = time()
			print(end_time-start_time, len(content))
			break

n_samples = len(content)

# construct matrix
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english')
t0 = time()
tf = tf_vectorizer.fit_transform(content)
print("done in %0.3fs." % (time() - t0))

print("Fitting LDA models with tf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)