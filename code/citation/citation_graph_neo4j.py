from pymongo import MongoClient
from py2neo import Graph
from py2neo import Node, Relationship

def is_qualified(paper):
	# Is English?
	# Has references?
	return ('lang' in paper and paper['lang'] == 'en') and ('references' in paper and len(paper['references']) > 0)

def create_author_node(author):
	# Create an author node identified by name and org.
	name = author.pop('name', None)
	org = author.pop('org', None)

	# TODO: Disambiguation.
	# Check if the author with same name and org exists in graph.
	query_filters = []
	if name is not None:
		query_filters.append("name:'{}'".format(name))
	if org is not None:
		query_filters.append("org:'{}'".format(org))
	query_filters = ','.join(query_filters)
	data = g.data('MATCH (a:Author {{{}}}) return a'.format(query_filters))
	if len(data) > 0:
		return data[0]['a']

	# Create author node.
	node = Node(
		'Author',
		name=name,
		org=org,
		)
	g.create(node)
	return node

def create_paper_node(paper):
	# Create a paper node identified by DOI or id (if no DOI).
	# Assume that a paper always has an id.
	doi = paper.pop('doi', None)
	id_ = paper.pop('id', None)

	# TODO: Disambiguation, replace same DOI with the most complete paper.
	# Check if the paper with same DOI or id exists in graph.
	if doi is not None:
		query_filter = "doi:'{}'".format(doi)
	else:
		query_filter = "id:'{}'".format(id_)
	data = g.data('MATCH (p:Paper {{{}}}) return p'.format(query_filter))
	if len(data) > 0:
		return data[0]['p']

	# Create a paper node.
	node = Node(
		'Paper',
		venue=paper.pop('venue', None),
		year=paper.pop('year', None),
		keywords=paper.pop('keywords', None),
		fos=paper.pop('fos', None),
		n_citation=paper.pop('n_citation', None),
		doc_type=paper.pop('doc_type', None),
		lang=paper.pop('lang', None),
		title=paper.pop('title', None),
		id=id_,
		doi=doi,
		)
	g.create(node)
	return node


def process_one_paper(paper):
	paper_node = create_paper_node(paper)

	# Create paper-author relationship
	authors = paper.pop('authors', None)
	if authors is not None:
		for author in authors:
			author_node = create_author_node(author)
			rel = Relationship(paper_node, 'HAS_AUTHOR', author_node)
			g.create(author_node|rel)

	# Create paper-reference relationship.
	references = paper.pop('references', None)
	if references is not None:
		for ref_id in references:
			# Query the referred paper from MongoDB.
			ref_paper = conn.wosdb.magfinal.find_one({'id':ref_id})
			if not is_qualified(ref_paper):
				continue
			ref_node = create_paper_node(ref_paper)
			rel = Relationship(ref_node, 'IS_CITED', paper_node)
			g.create(ref_node|rel)

	
conn = MongoClient(
	'mongodb://127.0.0.1:27017', 
	username='yash', 
	password='yash', 
	authSource='wosdb',
	authMechanism='SCRAM-SHA-1')
g = Graph()


if __name__ == '__main__':
	# Loop over all documents in MongoDB.
	for paper in conn.wosdb.magfinal.find():
		if not is_qualified(paper):  # Remove non-English and no reference papers.
			continue
		process_one_paper(paper)
	



