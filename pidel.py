import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('dirpath')
args = parser.parse_args()
dp = args.dirpath

#Execute remote command
os.system('ssh root@silver-08 "isi quota list --path %s"'%(dp))

#remove smartquota
os.system('ssh root@silver-08 "isi quota delete -f --type directory %s"'%(dp))

#delete folder
os.system("rm -rf %s"%(dp))
