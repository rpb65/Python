#!/usr/bin/env python
# IsilonAccountingQuotas.py
# 2016/09/20 rrue x3662
# lists top-level researcher/division folders and maintains a matching list of accounting-only directory quotas

#load the required modules
import os, os.path, re, sys, time, datetime, shutil, subprocess
from subprocess import Popen, PIPE

def main():
	""" main entry point; only called if __main__ """
	
	server = 'silver'
	ssh_key = 'c:\ssh\sopus.ppk'
	
	# get the directories
	dirs = []
	commnd = 'ls -p /ifs/data/fast/'
	# "-p" flag adds a trailing slash to any directory in ls output so we can
	# identify and ignore files
	commnd = "plink -i %s root@%s-01 \"%s\"" % (ssh_key, server, commnd)
	
	lines = subprocess.check_output(commnd, shell=True, stdin=subprocess.PIPE).split("\n")
	for line in lines:
		if not line.endswith("/"): continue # it's not a directory, move on
		if line.startswith("_") or line[-3] == "_": # it follows our naming scheme for the division/researcher folders
			dirs.append(line[:-1])
	
	dirs.sort()
	
	# get the quotas via SSH
	quotas = []
	commnd = 'isi quota list --type directory --format=csv --no-header'
	commnd = "plink -i %s root@%s-01 \"%s\"" % (ssh_key, server, commnd)
	
	lines = subprocess.check_output(commnd, shell=True, stdin=subprocess.PIPE).split("\n")
	for line in lines:
		if not line.startswith("directory"): continue
		quotas.append(line.split(",")[2].split("/")[-1])
	
	quotas.sort()
	
	# use list comprehension to identify quotas to be added and removed
	to_add = [i for i in dirs if i not in quotas]
	to_remove = [i for i in quotas if i not in dirs]
	
	for dir in to_add:
		print "adding accounting quota for %s to %s" % (dir, server)
		print add_quota(server,ssh_key,dir)
	for dir in to_remove:
		print "removing accounting quota for %s to %s" % (dir, server)
		print del_quota(server,ssh_key,dir)
	
	
	
def add_quota(server,ssh_key,dir):
	commnd = 'isi quota quotas create /ifs/data/fast/%s directory --enforced false --include-snapshots true' % dir
	commnd = "plink -i %s root@%s-01 \"%s\"" % (ssh_key, server, commnd)
	return subprocess.check_output(commnd, shell=True, stdin=subprocess.PIPE)

def del_quota(server,ssh_key,dir):
	commnd = 'isi quota quotas delete /ifs/data/fast/%s directory' % dir
	commnd = "plink -i %s root@%s-01 \"%s\"" % (ssh_key, server, commnd)
	return subprocess.check_output(commnd, shell=True, stdin=subprocess.PIPE)

if __name__ == '__main__': main()