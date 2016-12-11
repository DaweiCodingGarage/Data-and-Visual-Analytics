import csv
import json


f=open("arsenal_players.csv","r")
myReader=csv.reader(f,delimiter=",")
data=list(myReader)

data_copy=data[1:360][:]
data_copy_app=[]
for alist in data_copy:
    data_copy_app.append(int(alist[6]))
data_copy_app.sort(reverse=True)
data_copy_50=list(set(data_copy_app[0:50]))

keys=[]
for j in range(len(data_copy_50)):
    keys.extend([i for i in range(359) if int(data_copy[i][6])==data_copy_50[j]])

New_List=[]
New_dict={}
for item in keys:
    New_List.append({"name":data_copy[item][0],"position":data_copy[item][1],"appearance":data_copy[item][6],"goals":data_copy[item][7]})
New_dict.update({"nodes":New_List})

New_link=[]
#There is a link between any two players if their careers at Arsenal FC overlapped by at least one year.
for items in keys:
    New_link.append(range(int(data_copy[items][2]),int(data_copy[items][3])+1))

time_dict=[]
for i in range(len(New_link)):
    for j in range(i + 1, len(New_link)):
        if len(list(set(New_link[i]).intersection(New_link[j])))>0:
               time_dict.append({"source":i,"target":j,"value":len(list(set(New_link[i]).intersection(New_link[j])))})
New_dict.update({"links":time_dict})
with open('afc.json', 'w') as outfile:
    json.dump(New_dict,outfile)

