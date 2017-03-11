import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('dirpath')
args = parser.parse_args()

#Testing argument function
#print("~ Directory: {}".format(args.dirpath))

#Remove SmartQuota
os.system("isi quota delete --type directory {}".format(args.dirpath))

#Delete folder
os.system("rm -rf {}".format(args.dirpath))
