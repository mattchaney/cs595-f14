# -*- encoding: utf-8 -*-
#! /usr/bin/python

import requests
import pickle

MW_URI = "http://mementoweb.org/timemap/link/"

if __name__ == '__main__':
	with open('output', 'r') as f:
		mementos = {}
		for uri in f.read().split('\n'):
			if uri is '':
				continue
			count = 0
			result = requests.get(MW_URI + uri)
			if result.ok:
				count = result.text.count('rel="memento"')
			mementos[uri] = count
			print 'found %d mementos for uri: %s' % (count, uri)
	with open('results', 'w') as o:
		for item, num in mementos.iteritems():
			o.write('%s %d\n' % (item, num))