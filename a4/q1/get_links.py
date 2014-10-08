#! /usr/bin/python

import os
import random
import pickle
from bs4 import BeautifulSoup

LINKS_DIR = 'links' + os.sep
HTML_DIR = 'html' + os.sep

uri_map = pickle.load(open('uri_map', 'rb'))

def get_links(filename):
	'''Parses HTML contents and returns tuple of (filename, uri, list of links)'''
	with open(HTML_DIR + filename) as infile:
		uri = infile.readline().rstrip('\n')
		soup = BeautifulSoup(infile.read())
		links = [link['href'].encode('utf-8') for link in soup.find_all('a') if link.has_attr('href')]
		return filename, uri, links

def write_links(filename, uri, links):
	'''Writes URI and outlinks to file'''
	print('Writing {}'.format(uri))
	with open(LINKS_DIR + filename, 'w') as outfile:
		outfile.write('{}\n'.format(uri))
		for link in links:
			outfile.write('{}\n'.format(link))

if __name__ == '__main__':
	# random selection of 100 URIs in series from sorted list
	start = random.randint(0, 899)
	keys = uri_map.keys()
	keys.sort()
	for i in xrange(start, start + 100):
		write_links(*get_links(uri_map[keys[i]]))