#!/usr/bin/python

import sys, getopt

def main(argv):
   dirpath = ''
   try:
      opts, args = getopt.getopt(argv,"hd:",["dirpath="])
   except getopt.GetoptError:
      print 'pidel.py -d <directorypath>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'pidel.py -d <directorypath>'
         sys.exit()
      elif opt in ("-d", "--dirpath"):
         dirpath = arg
   print 'Directory path is', dirpath

if __name__ == "__main__":
   main(sys.argv[1:])
