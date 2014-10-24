#! /usr/bin/env python

import pickle
import igraph

FILENAME = 'karate.pickle'

if __name__ == '__main__':
	graph = pickle.loads(open(FILENAME).read())