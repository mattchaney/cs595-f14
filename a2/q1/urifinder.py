# -*- encoding: utf-8 -*-
import requests
from requests_oauthlib import OAuth1
from urllib import quote

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "PDBekXkvUto4V0XYZrrizcEub"
CONSUMER_SECRET = "OElKNfpNWF8Eh4iwbDFYFKDMBSouni3uRZrpsoGhbJcLZZmnBq"

OAUTH_TOKEN = "2560074793-g7ESlsQmwl3YKAfCJnIBa0lh3wHLjmPqj96XFuV"
OAUTH_TOKEN_SECRET = "tGYCQa9LL2i6wmApJzbGzHdVIVA65xiwVffPmbqWJwZPs"

SEARCH_URI = "https://api.twitter.com/1.1/search/tweets.json?q="

SEARCH_ITEMS = map(quote, [ 'space x', 
							'elon musk', 
							'richard garriott', 
							'starcraft 2', 
							'ebola virus',
							'world cup',
							'singularity',
							'rick and morty',
							'iphone 6',
							'android',
							'robin williams',
							'tony stewart',
							'bitcoin',
							'game of thrones',
							'facebook',
							'youtube',
							'google',
							'chris roberts',
							'hyper light drifter',
							'golang'])

def get_oauth():
	return OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)

def find_uris(uris):
	with open('output', 'a') as outfile:
		for search_item in SEARCH_ITEMS:
			result = requests.get(SEARCH_URI + search_item + '&filter%3Alinks&count=1000', auth=oauth)
			for status in result.json()['statuses']:
				for url in status['entities']['urls']:
					if len(uris) == 1000:
						return
					if 'expanded_url' in url:
						try:
							result = requests.get(url['expanded_url'], timeout=4)
							# only add expanded uris if they aren't in the list already
							if result.status_code == 200 and result.url not in uris:
								add_uri(uris, result.url)
								outfile.write('%s\n' % result.url)
						except Exception as e:
							print e
							continue

def add_uri(uris, uri):
	uris.add(uri)
	print 'added uri #%d: %s' % (len(uris), uri)

if __name__ == "__main__":
	oauth = get_oauth()
	uris = set()
	# read in previous set of uris
	try:
		with open('output', 'r') as infile:
			for line in infile.readlines():
				add_uri(uris, line.strip())
	except IOError:
		pass
	find_uris(uris)