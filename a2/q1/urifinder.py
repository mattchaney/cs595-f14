# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
from urllib import quote
from pprint import pprint

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "PDBekXkvUto4V0XYZrrizcEub"
CONSUMER_SECRET = "OElKNfpNWF8Eh4iwbDFYFKDMBSouni3uRZrpsoGhbJcLZZmnBq"

OAUTH_TOKEN = "2560074793-g7ESlsQmwl3YKAfCJnIBa0lh3wHLjmPqj96XFuV"
OAUTH_TOKEN_SECRET = "tGYCQa9LL2i6wmApJzbGzHdVIVA65xiwVffPmbqWJwZPs"

SEARCH_URI = "https://api.twitter.com/1.1/search/tweets.json?q="

SEARCH_ITEMS = map(quote, ['space x', 
                           'elon musk', 
                           'richard garriott', 
                           'starcraft', 
                           'ebola virus',
                           'space balls',
                           'space ghost',
                           'rick and morty',
                           'ren and stimpy',
                           'android'])

def search():
    for item in SEARCH_ITEMS: 
        result = requests.get(SEARCH_URI + item + '&filter%3Alinks', auth=oauth)

def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    oauth = get_oauth()
    r = requests.get(url="https://api.twitter.com/1.1/statuses/mentions_timeline.json", auth=oauth)
    print r.json()