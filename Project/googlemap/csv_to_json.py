import csv
import json

csvfile = open('E:/A+GTCLASS/CSE6242/Project/googlemap/geo.csv', 'r')

j=0
dict1={}
for line in csvfile:
    
    aList=line.split(',')
    if j==0:
        list_name=aList
    else:
        key=aList[1]
        del aList[1]
        dict1[key]=aList
    j=j+1

with open('E:/A+GTCLASS/CSE6242/Project/googlemap/geo.json', 'w') as outfile:
    json.dump(dict1,outfile)
