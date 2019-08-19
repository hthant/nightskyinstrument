import csv, sys

satinfo = open('prediction.csv',"rb")
reader = csv.reader(satinfo)
rownum = 9
colnum = 9

satinfo.close()