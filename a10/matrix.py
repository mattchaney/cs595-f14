import feedparser
import futures
import math
import md5
import re
import sys
import json

blog_uri = 'http://kevinmorrow.blogspot.com/feeds/posts/default'
data_file = 'blog_content'

def get_next(d):
	for item in d.feed.links:
		if item['rel'] == u'next':
			return item['href']
	return None

def get_words(text):
	txt = re.compile(r'<[^>]+>').sub('', text)
	words = re.compile(r'[^A-Z^a-z]+').split(txt)
	return [word.lower() for word in words if word != '']

def parse_entries(uri):
	print('processing {}'.format(uri))
	next = uri
	entries = {}
	while next is not None:
		feed = feedparser.parse(next)
		next = get_next(feed)
		print('next {}'.format(next))
		for entry in feed.entries:
			words = get_words(entry.summary)
			entries[entry.title] = words
			if len(entries) == 100:
				next = None
				break
	return entries

def load_data(filename):
	entries = {}
	with open(filename) as infile:
		for line in infile.readlines():
			tup = line.split('\t')
			title = tup[0]
			entry = ' '.join(json.loads(tup[1]))
			entries[title] = entry
	return entries

if __name__ == '__main__':
	entries = parse_entries(blog_uri)
	with open(data_file, 'w') as outfile:
		for title, wc in entries.iteritems():
			outfile.write(title + '\t')
			json.dump(wc, outfile)
			outfile.write('\n')
