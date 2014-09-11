#!/usr/bin/env python

import sys
import requests
import time
import re
from bs4 import BeautifulSoup

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Usage:\n\tpython getscore.py [school] [period] [uri]\n"
		sys.exit()
	school = sys.argv[1]
	try:
		period = float(sys.argv[2])
	except ValueError:
		print "[period] parameter must be valid floating point number"
		sys.exit(1)
	uri = sys.argv[3]
	while True:
		try:
			response = requests.get(uri)
		except Exception as e:
			print e
			sys.exit(1)
		soup = BeautifulSoup(response.content)
		gametag = soup.find('em', text=re.compile('^'+school+'$'))
		if not gametag:
			print "Game not found"
			sys.exit()
		game = gametag.parent.parent.parent
		try:
			teams = [game.find_all('span', {'class':'team'})[0].em.text, game.find_all('span', {'class':'team'})[1].em.text]
			scores = [game.find('span', {'class':'away'}).text, game.find('span', {'class':'home'}).text]
		except:
			print "Game not found"
			sys.exit()
		print teams[0] + ' ' + scores[0] + ', ' + teams[1] + ' ' + scores[1]
		time.sleep(period)