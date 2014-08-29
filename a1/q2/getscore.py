#!/usr/bin/env python

import sys
import requests
import time
import re
from bs4 import BeautifulSoup

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Usage:\n\tpython getscore.py [school] [seconds] [uri]\n"
		sys.exit()
	school = sys.argv[1]
	period = float(sys.argv[2])
	uri = sys.argv[3]
	while True:
		soup = BeautifulSoup(requests.get(uri).content)
		gametag = soup.find('em', text=re.compile('^'+school+'$'))
		if not gametag:
			print "Game not found"
			sys.exit()
		game = gametag.parent.parent.parent
		teams = [game.find_all('span', {'class':'team'})[0].em.text, game.find_all('span', {'class':'team'})[1].em.text]
		scores = [game.find('span', {'class':'away'}).text, game.find('span', {'class':'home'}).text]
		print teams[0] + ' ' + scores[0] + ', ' + teams[1] + ' ' + scores[1]
		time.sleep(period)