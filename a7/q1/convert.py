#! /usr/bin/python

import pickle

FILENAME = 'karate.pickle'

data = pickle.loads(open(FILENAME).read())['karate']
factions = data.vs['Faction']

def build_matrix(raw, n):
	matrix = [[0 for y in range(n)] for x in range(n)]
	for idx, line in enumerate(raw):
		for idy, val in enumerate(line.split()):
			matrix[idx][idy] = int(val)
	return matrix

def write_nodes(output, graph):
	node = {}
	for idx, club in enumerate(factions):
		output.write("\t\t{ \"id\":%d, \"club\":%d }" % (idx, club))
		if idx+1 != len(factions):
			output.write(',')
		output.write('\n')


def write_links(output, egraph, cgraph):
	for idx, line in enumerate(egraph):
		for idy, val in enumerate(line):
			if val == 1:
				output.write("\t\t{ \"source\":%d, \"target\":%d, \"value\":%d }" % (idx, idy, cgraph[idx][idy]))
				if idy+1 != len(line):
					output.write(',')
				output.write('\n')

if __name__ == '__main__':
	lines = [line.strip() for line in open('karate.txt').readlines()]

	# get length of line
	n = int(lines[1].split()[0].replace('N=',''))

	ename = lines[4]
	egraph = build_matrix(lines[7:41], n)

	cname = lines[5]
	cgraph = build_matrix(lines[41:], n)

	with open('out.json', 'w') as output:
		output.write('{\n')
		output.write('\t"graph": [\n\t\t["name", "Zachary\'s Karate Club"]\n\t],\n')
		
		output.write('\t"nodes": [\n')
		# write nodes
		write_nodes(output, egraph)
		output.write('\t],\n')
		output.write('\t"links": [\n')

		# write links
		write_links(output, egraph, cgraph)
		output.write('\t],\n')

		output.write("\t\"multigraph\": false\n")
		output.write('}\n')
