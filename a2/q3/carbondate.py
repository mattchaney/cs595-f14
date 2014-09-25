#! /usr/bin/python

from local import cd
import json

ECD = 'Estimated Creation Date'

def getdate(uri):
	uri_json = json.loads(cd(uri))
	if uri_json[ECD]:
		print 'Found creation date: %s' % uri_json[ECD]
		outfile.write('%s %s\n' % (uri, uri_json[ECD]))
	else:
		print 'Found no ECD'

if __name__ == '__main__':
	# Remove already completed links
	with open('output', 'r') as outfile:
		output = [line.rstrip('\n') for line in outfile]
	with open('results', 'r') as prevfile:
		prev = [line.split(' ')[0] for line in prevfile]	
	output = [line for line in output if line not in prev]
	print "Starting on uri #%d" % len(output)

	# Work on the rest
	with open('output', 'r') as infile:
		with open('results','a') as outfile:
			for uri in infile:
				uri = uri.strip()
				print 'Searching for uri: %s' % uri
				getdate(uri)
