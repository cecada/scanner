# scanner
TL;DR: 
this script will randomly generate ids of n length and check to see if that combined with a file-sharing URL there, in fact, exists "hidden" content. 

Overview:

This script will randomly generate ids of n length and check to see if that combined with a file-sharing URL there, in fact, exists "hidden" content.  Many times users can share files with known users and are given an obscure URL. In theory, only those who know the URL will be able to find the content. However, by brute-forcing the URL string it is possible (and often time-consuming) to find content not otherwise known.

Example (made up url):
https://example.com/l9sbXtc2n1

l9sbXtc2n1 is the part this script will brute force. 

The script will make a request to <url>/<random string> over a TOR circuit. The script will then check the Http response code; because many file sharing sites I have observed display custom 404 error pages that look a lot like 200/201 pages in a browser but are in fact 404. So, obviously, if the code is 200 or 201 then it is logged in a loot file; otherwise, unless verbose logging is enabled the script just moves on.

Prerequisites:

Python 3
Python package curses
Python package requests
Tor

if you need help installing curses this guide may help:
https://www.cyberciti.biz/faq/linux-install-ncurses-library-headers-on-debian-ubuntu-centos-fedora/

Requests is a pretty common package, and you probably already have it, but in case you don't this link may help:
https://askubuntu.com/questions/504068/how-to-install-requests-module-for-python3

You may also need urllib; this link may help if you do not know how to install it:
https://www.quora.com/How-do-I-install-urllib-and-urllib2-for-Python-3-3-2

Still, need Python help:
Otherwise, Google something like "python3 install [curses | requests | urllib] on [your os here]"

To install Tor these are the official instructions from The Tor Project:
https://2019.www.torproject.org/docs/tor-doc-unix.html.en

Key Features:

Ability to set the length of the random string
Will make requests over TOR
Ability to set how many requests are made before the IP address changes
Ability to set a pause between requests (may help avoid DDOS protection)

Use:

Download the script (duh)
Set the global variables to suit your needs
Make file executable
Run script

Global Settings:

TORSERVER Default:127.0.0.1
The IP of the server the TOR process is running


TORPORT Default:9050
The port TOR is listening on


BASEURL  Default <none>
This is the URL you are going to scan for example https://example.com/
Note: terminate the URL with a backslash


KEYLEN Default:10
The length of the key. In the example above it would be the length of l9sbXtc2n1.


PAUSE Default:0.5
The time (in seconds) the script will pause between requests 


NEWIP Default:10
How many requests will be made before the script will request a new TOR circuit.


LOOTPATH Default:finds.txt
Filename which will store URLs found

DEBUGPATH Default:debug.txt
Filename which will store verbose (detailed) logging, should you enable it.


VERBOSE Default:True
Turn detailed logging on or off
