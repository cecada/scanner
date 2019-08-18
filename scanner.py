#!/usr/bin/env python3

import curses
import datetime
import random
import time
import requests
import string

from html.parser import HTMLParser
from urllib.request import Request, urlopen	

TORSERVER = '127.0.0.1'
TORPORT = 9050
BASEURL = 'https://example.com/'
KEYLEN = 10
PAUSE = 0.5
NEWIP = 10
LOOTPATH = "finds.txt"
DEBUGPATH = "debug.txt"
VERBOS = True

class TitleParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.match = False
		self.title = ''

	def handle_starttag(self, tag, attributes):
		self.match = True if tag == 'title' else False

	def handle_data(self, data):
		if self.match:
			self.title = data
			self.match = False

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def get_title(html):
	parser = TitleParser()
	parser.feed(html)
	return parser.title

def log(path, logstr):
	datestr = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
	logstr = "[" + datestr +"] " + logstr

	with open(path, 'a') as out:
		out.write(logstr + '\n')

def update_ip(session):
	response = session.get('https://api.ipify.org')
	ip = response.text
	response.close()
	return ip

def refresh_circut():
	session = requests.session()
	creds = str(random.randint(10000,0x7fffffff)) + ":" + "foobar"
	connstr = 'socks5h://'+creds+'@'+TORSERVER+':'+str(TORPORT)
	session.proxies = {'http':connstr,'https':connstr}
	return session

def fetch_site(session, url):

	verbosstr = ''

	with session as s:
		response = s.get(url)

	code = response.status_code
	
	if code == 200 or code == 201 or code == 202:
		html = response.text
		response.close()		
		return [True, html]

	else:
		verbosstr = 'HTTP Error code: ' + str (code)
		response.close()
		return [False,verbosstr]

def report_progress(details,ip,tries,found):
	stdscr.addstr(0, 0, "Running... Press ctl-c to quit")
	stdscr.addstr(1, 0, str(found) + " Found of " + str(tries) + " Tries")
	stdscr.addstr(2, 0, ip)
	if VERBOS:
		stdscr.addstr(3, 0, details[1])
		stdscr.clrtoeol()
		stdscr.clearok(3)
	stdscr.refresh()

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

def main():

	session = refresh_circut()
	ip = update_ip(session)

	try:
		tries = 1
		found = 0
		
		while True:
			key = id_generator(KEYLEN)			
			if tries % NEWIP == 0:
				session = refresh_circut()
				ip = update_ip(session)
				key = 'q0KbV42fn4'

			time.sleep(PAUSE)
			url = BASEURL + key

			tries += 1
			
			html = fetch_site(session, url)

			if html[0]:
				found += 1
				title = get_title(html[1])
				html[1] = "FOUND! " + title				
				log(LOOTPATH, url + "," + title)

			if VERBOS:
				log(DEBUGPATH, url + "," + html[1])

			report_progress(html,ip,tries,found)

	except KeyboardInterrupt:
		curses.endwin()
		print("Shutdown Complete\n")
main()
