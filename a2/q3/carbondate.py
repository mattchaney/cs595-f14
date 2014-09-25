#! /usr/bin/python

from local import cd
import json
import futures

ECD = 'Estimated Creation Date'

def getdate(uri):
	uri = uri.strip()
	print 'Searching for uri: {}'.format(uri)
	uri_json = json.loads(cd(uri))
	if uri_json[ECD]:
		print 'Found creation date: {}'.format(uri_json[ECD])
		return (uri, uri_json[ECD])
	else:
		print 'Found no ECD'
		return None

if __name__ == '__main__':
	# Remove already completed links
	with open('output') as outfile:
		output = [line.split(' ')[0] for line in outfile if line.rstrip('\n').split(' ')[1] != '0']
	with open('results') as prevfile:
		prev = [line.split(' ')[0] for line in prevfile]	
	uris = [line for line in output if line not in prev]
	print "Starting on uri #{}".format(len(output))

	# Work on the rest
	with open('results','a') as outfile:
		with futures.ThreadPoolExecutor(max_workers=4) as executor:
 			urifutures = [executor.submit(getdate, uri) for uri in uris]
 			for future in futures.as_completed(urifutures):
	 			try:
	 				data = future.result()
	 			except Exception as exc:
	 				print "{} generated an exception: {}".format(uri, exc)
	 			if len(data) == 2:
	 				print "Writing data: {}".format(data)
	 				outfile.write('{} {}\n'.format(data[0], data[1]))
	 			else:
	 				print "Found no data"
		