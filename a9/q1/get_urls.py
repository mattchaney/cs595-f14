#! /usr/bin/env python

import requests

with open('blog_urls') as infile:
	urls = set([line.strip() for line in infile.readlines()])

with open('blog_urls', 'w') as outfile:
	for url in urls:
		if 'rss.xml' not in url:
			url = url + 'rss.xml'
		outfile.write(url + '\n')

with open('blog_urls', 'a') as outfile:
	while len(urls) < 100:
		try:
			r = requests.get('http://www.blogger.com/next-blog?navBar=true&blogID=3471633091411211117')
		except Exception, e:
			continue
		url = r.url.replace('?expref=next-blog', '')
		if url not in urls:
			urls.add(url)
			outfile.write(url + 'rss.xml\n')
			print url