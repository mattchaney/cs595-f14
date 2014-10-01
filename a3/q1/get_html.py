#! /usr/bin/python

import requests
import futures
import md5

def convert(uri):
	return md5.new(uri).hexdigest()

def get_html(uri):
	print('Getting {}'.format(uri))
	response = requests.get(uri)
	return response.url, response.status_code, response.content

if __name__ == '__main__':
	with open('uris') as infile:
		uris = [uri.rstrip('\n') for uri in infile]

	with futures.ThreadPoolExecutor(max_workers=8) as executor:
		with open('html/uri_map', 'w') as map_file:
			uri_futures = [executor.submit(get_html, uri) for uri in uris]
			for future in futures.as_completed(uri_futures):
				try:
					uri, status_code, content = future.result()
				except Exception as exc:
					print('{} generated an exception: {}'.format(uri, exc))
					continue
				if status_code == 200:
					hashed_uri = convert(uri)
					print('Writing {} as {}'.format(uri, hashed_uri))
					map_file.write('{} {}\n'.format(uri, hashed_uri))
					with open('html/raw/' + hashed_uri, 'w') as outfile:
						outfile.write(content)
				else:
					print('Not writing {}, bad status code: {}'.format(uri, status_code))