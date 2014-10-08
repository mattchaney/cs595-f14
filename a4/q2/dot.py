#! /usr/bin/python

import os
import random
from urlparse import urlparse

LINKS_DIR = 'links' + os.sep

def extract(uri):
	'''Strip the path from the URI and return the domain name'''
	parsed = urlparse(uri.strip())
	if parsed.netloc:
		return parsed.netloc + parsed.path[:20]
	else:
		return ''

def write_dot(uri, links, outfile):
	'''Write the uri and all of its links (with labels) to the file "outfile" in dot format'''
	for link, label in links.iteritems():
		outfile.write('\t"{}" -> "{}";\n'.format(uri, link))
		outfile.write('\t"{}" [label="{}"]\n'.format(uri, extract(uri)))
		outfile.write('\t"{}" [label="{}"]\n'.format(link, label))

if __name__ == '__main__':
	with open('links.gv', 'w') as outfile:
		outfile.write('digraph unix {\n')
		for filename in os.listdir('links'):
			with open(LINKS_DIR + filename, 'r') as infile:
				uri = infile.readline().rstrip('\n')
				links = {link.rstrip('\n'): extract(link) for link in infile if extract(link)}
				write_dot(uri, links, outfile)
		outfile.write('}')