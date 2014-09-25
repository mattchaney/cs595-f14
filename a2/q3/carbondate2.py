#! /usr/bin/python

from local import cd
import json
import futures

ECD = 'Estimated Creation Date'

def getdate(uri):
	uri = uri.strip()
	print 'Searching for uri: %s' % uri
	uri_json = json.loads(cd(uri))
	if uri_json[ECD]:
		print 'Found creation date: %s' % uri_json[ECD]
		return uri_json[ECD]
	else:
		print 'Found no ECD'
		return None

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
		uris = [line.rstrip('\n') for line in infile]
	with open('results2','a') as outfile:
		with futures.ThreadPoolExecutor(max_workers=5) as executor:
 			for uri in uris:
 				future_to_url = executor.submit(getdate, uri)
 			for future in futures.as_completed(future_to_url):
     			try:
     				data = future.result()
     			except Exception as exc:
     				print "%s generated an exception: %s" % (uri, exc)
     			else:
     				print "Data: %s" % data
     				outfile.write('%s %s\n' % (uri, uri_json[ECD]))

		