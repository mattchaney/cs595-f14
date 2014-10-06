#! /usr/bin/python

import md5
import requests
import os
from bs4 import BeautifulSoup

LINKS_DIR = 'links' + os.sep

def get_links(uri):
	try:
		response = requests.get(uri)
	except Exception as e:
		print('{} generated an exception: {}'.format(uri, e))
		return
	if not response.ok:
		print('Bad response from {}'.format(uri))
		return
	response.encoding = 'utf-8'
	return [link['href'] for link in BeautifulSoup(response.text).find_all('a')]

def write_links(uri, links):
	with open(LINKS_DIR + md5.new(uri).hexdigest(), 'w') as outfile:
		outfile.write('{}\n'.format(uri))
		for link in links:
			outfile.write('{}\n'.format(link))

if __name__ == '__main__':
	with open(uris) as infile:
		uris = [uri.rstrip('\n') for uri in infile]
	for uri in uris:
		write_links(uri, get_links(uri))