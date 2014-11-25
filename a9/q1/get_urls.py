#! /usr/bin/env python

import requests
from bs4 import BeautifulSoup

default = 'http://www.blogger.com/next-blog?navBar=true&blogID=3471633091411211117'
must_haves = ['http://f-measure.blogspot.com/', 'http://ws-dl.blogspot.com/']

def get_atom(url):
	try:
		r = requests.get(url)
	except Exception, e:
		return None
	soup = BeautifulSoup(r.text)
	links = soup.find_all('link', {'type':'application/atom+xml'})
	if links: 
		return str(links[0]['href'])
	return None

def add_url(url, urls, outfile):
	if url and url not in urls:
		urls.add(url)
		outfile.write(url + '\n')
		print len(urls), url

if __name__ == '__main__':
	urls = set()
	with open('blog_urls', 'w') as outfile:
		for must_have in must_haves:
			url = get_atom(must_have)
			add_url(url, urls, outfile)
		while len(urls) < 100:
			url = get_atom(default)
			add_url(url, urls, outfile)