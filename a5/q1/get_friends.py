# -*- encoding: utf-8 -*-

import json
import requests
import time
from requests_oauthlib import OAuth1
from pprint import pprint

CONSUMER_KEY = "PDBekXkvUto4V0XYZrrizcEub"
CONSUMER_SECRET = "OElKNfpNWF8Eh4iwbDFYFKDMBSouni3uRZrpsoGhbJcLZZmnBq"
OAUTH_TOKEN = "2560074793-g7ESlsQmwl3YKAfCJnIBa0lh3wHLjmPqj96XFuV"
OAUTH_TOKEN_SECRET = "tGYCQa9LL2i6wmApJzbGzHdVIVA65xiwVffPmbqWJwZPs"
SEARCH_URI = "https://api.twitter.com/1.1/friends/list.json"
LIMIT_URI = "https://api.twitter.com/1.1/application/rate_limit_status.json"

def get_oauth():
	return OAuth1(CONSUMER_KEY,
				client_secret=CONSUMER_SECRET,
				resource_owner_key=OAUTH_TOKEN,
				resource_owner_secret=OAUTH_TOKEN_SECRET)

OAUTH = get_oauth()

def get_limit():
	response = requests.get(LIMIT_URI, params={'resources':'friends'}, auth=OAUTH)
	data = json.loads(response.text)
	return data['resources']['friends']['/friends/list']['remaining'], data['resources']['friends']['/friends/list']['reset']

def wait_for_reset(reset):
	naptime = reset - time.time() + 5
	print("Limit reached, sleeping for {}".format(naptime))
	time.sleep(naptime)
	print("Time to get up and go to work")
	return get_limit()

def get_friends(screen_name):
	print("Getting {}'s friends".format(screen_name))
	friends = []
	next_cursor = -1
	limit, reset = get_limit()
	if limit == 0:
		limit, reset = wait_for_reset(reset)
	while True:
		response = requests.get(SEARCH_URI,
					params={'screen_name':screen_name, 
					'cursor':next_cursor, 
					'count':200},
					auth=OAUTH)
		if not response:
			print("Bad response: {}".format(response.reason))
			return []
		limit = limit - 1
		data = json.loads(response.text)
		print("Got {} friends, limit: {}".format(len(data['users']), limit))
		next_cursor = data['next_cursor']
		friends.extend(data['users'])
		if next_cursor == 0:
			return [friend['screen_name'] for friend in friends]
		if limit == 0:
			limit, reset = wait_for_reset(reset)

if __name__ == '__main__':
	with open('friends') as infile:
		friends = [line.strip() for line in infile]

	friend_counts = {friend:0 for friend in friends}

	with open('friend_counts') as infile:
		for line in infile:
			friend, counts = line.strip().split(' ')
			friend_counts[friend] = counts

	for friend, count in friend_counts.iteritems():
		if count > 0:
			friends.remove(friend)

	with open('friend_counts', 'a') as outfile:
		for friend in friends:
			friend_list = get_friends(friend)
			if friend_list is None:
				continue
			outfile.write('{} {}\n'.format(friend, len(friend_list)))