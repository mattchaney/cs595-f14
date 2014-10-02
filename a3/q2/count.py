#! /usr/bin/python

import os
import sys
import re
import pickle
from string import punctuation

def count_terms(term, file_list=os.listdir('html/processed')):
	for filename in file_list:
		with open('html/processed/' + filename) as infile:
			uri = infile.readline().strip()
			text = infile.read()
			count = text.count(term)
			if count > 0:
				print('{} {}'.format(count, uri))
				return count, uri
	return None, None

def get_uri(uri):
	for filename in os.listdir('html/processed/'):
		with open('html/processed/' + filename) as infile:
			if uri in infile.readline():
				return uri, filename
	return None, None

def get_uris():
	uri_file = {}
	for uri in open('uris').read().split('\n'):
		uri, filename = get_uri(uri)
		if not uri:
			continue
		uri_file[uri] = filename
	return uri_file

def process_file(uri):
	filename = get_filename(uri)
	with open('html/processed/' + filename) as infile:
		# To remove URI in first line
		infile.readline()
		# Removing all punctuation
		strs = infile.read()
		r = re.compile(r'[{}]'.format(punctuation))
		content = r.sub(' ', strs)
	return content

def get_tf(content, term):
	return float(content.count(term)) / float(len(content.split()))

def get_idf(content, term):
	uri_map = pickle.load(open('uri_map', 'rb'))
	present = set()
	absent = set()
	for uri, filename in uri_map.iteritems():
		content = process_file(filename)
		if term in content:
			present.add(uri)
		else:
			absent.add(uri)
	return float(len(present)) / float(len(absent))

def get_tfidf(content, term):
	pass

def get_filename(uri):
	uri_map = pickle.load(open('uri_map', 'rb'))
	return uri_map[uri]

if __name__ == '__main__':
	# Used to bulk print all occurences > 0 of search term
	if len(sys.argv) == 3 and sys.argv[1] == 'count':
		count_terms(sys.argv[2], os.listdir('html/processed'))

	# Used to build the uri_map file, which maps the uri to 
	# the filename the dereferenced content is stored in
	elif len(sys.argv) == 2 and sys.argv[1] == 'uri_map':
		uris = get_uris()
		pickle.dump(uris, open('uri_map', 'w'))

	# Used to count occurences of the search term in a list
	# of URIs specified in the 'uri_counts' file
	elif len(sys.argv) == 4 and sys.argv[1] == 'count':
		uri_map = pickle.load(open('uri_map', 'rb'))
		with open('uri_counts', 'w') as outfile:
			for uri, filename in uri_map.iteritems():
				count, uri = count_terms(sys.argv[2], [filename])
				outfile.write('{} {}\n'.format(count, uri))

	# Used as a utility to simply get the filename for the given URI
	elif len(sys.argv) == 3 and sys.argv[1] == 'uri':
		print get_filename(sys.argv[2])

	else:
		print('Usage:\n\tpython grep.py <SEARCH_TERM>')