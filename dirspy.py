#!/usr/bin/env python3

from datetime import datetime
from time import sleep, strftime
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import requests, sys, urllib3, argparse
import os, subprocess, resource

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Fix insecure ssl
resource.setrlimit(resource.RLIMIT_NOFILE, (8192, 8192)) # Fix to many open file (RAM => 8GB)
user_agent = {'User-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

class cl:
	pink = '\033[95m'
	blue = '\033[94m'
	green = '\033[92m'
	yellow = '\033[93m'
	red = '\033[91m'
	end = '\033[0m'
	white = '\033[1m'
	under = '\033[4m'

def sizeof(num, suffix='B'):
	for unit in [' ','K','M','G','T','P','E','Z']:
		if abs(num) < 1024.0:
			return('{:>4} {}{}'.format(format(num, '.3g'), unit, suffix))
		num /= 1024.0

def rikues(line):
	alamat = str(args.target) + str(line)
	if args.random_agent == True:
		user_agent = {'User-agent': UserAgent().random}
		r = requests.get(alamat, headers = user_agent, timeout = 5, allow_redirects = False, verify = False)
	else:
		user_agent = {'User-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
		r = requests.get(alamat, headers = user_agent, timeout = 5, allow_redirects = False, verify = False)

	num = int(len(r.text))
	status = r.status_code

	# Success
	if status == 200:
		if line == '': pass
		elif len(r.text) == leng: pass
		else: sys.stdout.write(cl.green + '| {} | {} - {} | {}\n'.format(datetime.now().strftime('%H:%M:%S'), status, sizeof(num), alamat) + cl.end)
	# Redirect
	elif status == 301:
		if len(r.text) == leng: pass
		else: sys.stdout.write(cl.red + '| {} | {} - {} | {}\n'.format(datetime.now().strftime('%H:%M:%S'), status, sizeof(num), alamat) + cl.end)
	#Internal server error
	elif status == 500:
		if len(r.text) == leng: pass
		else: sys.stdout.write(cl.pink + '| {} | {} - {} | {}\n'.format(datetime.now().strftime('%H:%M:%S'), status, sizeof(num), alamat) + cl.end)
	# Unauthenticated
	elif status == 401:
		if len(r.text) == leng: pass
		else: sys.stdout.write(cl.yellow + '| {} | {} - {} | {}\n'.format(datetime.now().strftime('%H:%M:%S'), status, sizeof(num), alamat) + cl.end)
	# Forbidden
	elif status == 403:
		if ".ht" in line: pass
		elif len(r.text) == leng: pass
		else: sys.stdout.write(cl.blue + '| {} | {} - {} | {}\n'.format(datetime.now().strftime('%H:%M:%S'), status, sizeof(num),alamat) + cl.end)

def prog():
	sys.stdout.flush()
	sys.stdout.write('| {} | [+] Wait a moment ...\r'.format(datetime.now().strftime('%H:%M:%S')))
	sys.stdout.flush()
	sys.stdout.write('| {} | [x] Wait a moment ...\r'.format(datetime.now().strftime('%H:%M:%S')))

print(' ____  _          ______   __')
print('|  _ \(_)_ __ ___|  _ \ \ / /')
print("| | | | | '__/ __| |_) \ V /")
print('| |_| | | |  \__ \  __/ | |')
print('|____/|_|_|  |___/_|    |_|\n')
print('')
print('DirsPY v3.0\n')

parser = argparse.ArgumentParser()
parser.add_argument("target", help="Your target (EX: http://www.target.com/)")
parser.add_argument("-w", "--wordlist", help="Wordlist file", default="dirs.txt")
parser.add_argument("-t", "--thread", help="Max thread (default:100)", type=int, default=100)
parser.add_argument("--random-agent", help="Random user agent", action="store_true")
args = parser.parse_args()

try:
	cek = requests.get(args.target, headers = user_agent, timeout = 5, verify = False)
	leng = len(cek.text)
except:
	print('ERROR: Invalid address or target is down..')
	sys.exit()

no = 0
file = open(args.wordlist, 'r', encoding='ISO-8859-1').read().split('\n')
lcount = sum(1 for line in open(args.wordlist, encoding='ISO-8859-1'))
print('Start scanning directory..')
print('Wordlist : {} | Thread : {} | Random agent : {}'.format(args.wordlist, args.thread, args.random_agent))
print('===============================================================================')
print('| Time     | Info          | URL                                              |')
print('===============================================================================')
executor = ThreadPoolExecutor(max_workers=args.thread)
futures = []
for line in file:
	try:
		a = executor.submit(rikues, line)
		futures.append(a)
		no = no + 1
		jumlah = ( no * 100 ) / lcount
		sys.stdout.flush()
		sys.stdout.write("| {} | {}% Line : {}\r".format(datetime.now().strftime('%H:%M:%S'), int(jumlah), int(no)))
		sys.stdout.flush()
	except(KeyboardInterrupt,SystemExit):
		print('\r| {} | Exiting program ...'.format(datetime.now().strftime('%H:%M:%S')))
		print('===============================================================================')
		os.kill(os.getpid(), 9)

while True:
	try:
		prog()
		cek = a.done()
		if cek == True:
			sleep(1)
			print('===============================================================================');
			exit()

	except KeyboardInterrupt:
		print('\r| {} | Exiting program ...'.format(datetime.now().strftime('%H:%M:%S')))
		print('===============================================================================')
		os.kill(os.getpid(), 9)
