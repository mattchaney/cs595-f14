# -*- encoding: utf-8 -*-
#! /usr/bin/python

import requests
import re

MW_URI = "http://mementoweb.org/timemap/link/"

if __name__ == '__main__':
	with open('output', 'r') as f:
		mementos = {}
		for uri in f.read().split('\n'):
			if uri is '':
				continue
			count = 0
			target_uri = MW_URI + uri
			while True:
				result = requests.get(target_uri)
				if result.ok:
					count = count + result.text.count('rel="memento"')
				last_line = result.text.split('\n')[-1]
				if 'rel="timemap"' not in last_line:
					break
				sites = re.findall(r'<([^<|^>]+)>', last_line)
				target_uri = sites[1]
			mementos[uri] = count
			print 'found %d mementos for uri: %s' % (count, uri)
	with open('results', 'w') as o:
		for item, num in mementos.iteritems():
			o.write('%s %d\n' % (item, num))