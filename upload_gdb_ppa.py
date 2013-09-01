#!/usr/bin/python

import os

always_yes = False

while 1:
	try:
		n = raw_input("Want alway answer yes?[n]/y:")
		if n == 'y':
			always_yes = True
		elif n != '' and n != 'n':
			continue
	except:
		continue
	break

def query_continue():
	if not always_yes:
		while 1:
			try:
				n = raw_input("Continue?")
			except:
				continue
			if n == "y":
				break
			elif n == "n":
				exit(0)


ppa_dir = "/home/teawater/gdb/git/"

#call command
def callcmd(cmd):
	if os.system(cmd) != 0:
		raise Exception("Call \""+cmd+"\" got error.")

def find_change(version):
	for f in os.listdir(ppa_dir):
		if f.find(".changes") > 0 and f.find(version) > 0:
			return ppa_dir+f
	raise Exception("Try to find \""+version+"\" got error.")

callcmd("proxychains dput  ppa:teawater/gdb-10.04 "+find_change("lucid"))
query_continue()

#callcmd("proxychains dput  ppa:teawater/gdb-10.04 "+find_change("maverick"))
#query_continue()

callcmd("proxychains dput  ppa:teawater/gdb-10.04 "+find_change("natty"))
query_continue()

callcmd("proxychains dput  ppa:teawater/gdb-10.04 "+find_change("oneiric"))
query_continue()

callcmd("proxychains dput  ppa:teawater/gdb-10.04 "+find_change("precise"))
query_continue()

callcmd("proxychains dput  ppa:teawater/gdb-10.04 "+find_change("quantal"))
query_continue()

callcmd("proxychains dput  ppa:teawater/gdb-10.04 "+find_change("saucy"))
query_continue()
