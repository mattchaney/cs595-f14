#! /usr/bin/python

import os
from urlparse import urlparse

LINKS_DIR = 'links' + os.sep

def extract(uri):
	return urlparse(uri.strip()).netloc

def write_dot(uri, links, outfile):
	for link, label in links.iteritems():
		outfile.write('\t"{}" -> "{}" [label="{}"];\n'.format(uri, link, label))

if __name__ == '__main__':
	with open('dot', 'w') as outfile:
		outfile.write('digraph unix {\n')
		for filename in os.listdir('links'):
			with open(LINKS_DIR + filename, 'r') as infile:
				uri = infile.readline().rstrip('\n')
				links = {link.rstrip('\n'): extract(link) for link in infile if extract(link)}
				write_dot(uri, links, outfile)
		outfile.write('}')