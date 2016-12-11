import json
import ast

f=open('C:/Users/Dawei/Downloads/final_dict3.csv','r')
jsonList=[]
j=0
for line in f:
    dict1={}
    aList=line.split('"')
    for i in range(len(aList)):
       aList[i]=aList[i].rstrip('\n')
       aList[i]=aList[i].rstrip(',')
       aList[i]=aList[i].lstrip(',')
       aList[i]=aList[i].lstrip('\xef\xbb\xbf')
    if len(aList)==3:
        dict1['Index']=j
        #print aList[2]
        a=ast.literal_eval(aList[1])
        del a['business']
        '''if a['singlets']==[]:
            del a['singlets']
        if a['pairs']==[]:
            del a['pairs']'''
        if a['triplets']==[]:
            a['triplets']=['nan']
        dict1['RestaurantName']=a["RestaurantName"]
        del a["RestaurantName"]
        dict1['Review']=a
        j=j+1
        jsonList.append(dict1)

#print jsonList[0]

i=0
MapDict={}
k=0
while i<len(jsonList):
    rev=[]
    name=jsonList[i]['RestaurantName']
    Lon,Lat=jsonList[i]['Review']['longitude'],jsonList[i]['Review']['latitude']
    for j in range(i,len(jsonList)):
        if name==jsonList[j]['RestaurantName']:
            del jsonList[j]['Review']['longitude']
            del jsonList[j]['Review']['latitude']
            rev.append(jsonList[j]['Review'])
            k=k+1
        else:
            break
    i=k
    MapDict[name]=[Lon,Lat,rev]
#print MapDict
with open('C:/Users/Dawei/Downloads/data1.json', 'w') as outfile:
    json.dump(MapDict,outfile)


