from urllib2 import Request, urlopen
false=False
null=None
true=True
headers = {
  'Accept': 'application/json'
}
count,i=0,1
Movie=[]
while count<=300:
    request1 = Request('https://api.themoviedb.org/3/search/movie?api_key=da4968151cb84cdbe9091470652ab77c&query=life&page='+str(i), headers=headers)
    response_body1 = urlopen(request1).read()
    dict_body=eval(response_body1)
    for item in dict_body["results"]:
        Info=[item["id"],item["title"]]
        Movie.append(Info)
        count=count+1
    i=int(i)+1
        
item_id=[]
f=open("movie_ID_name.txt","w")
for item in Movie[0:300]:
    item_id.append(item[0])
    f.write(str(item[0])+","+item[1]+"\n")
f.close()

import time
Movie_list=[]
Movie1_list=[]
for i in item_id:
    request2 = Request('http://api.themoviedb.org/3/movie/'+str(i)+'/similar?api_key=da4968151cb84cdbe9091470652ab77c', headers=headers)
    response_body2 = urlopen(request2).read()
    dict_body2=eval(response_body2)
    for item in dict_body2["results"][0:5]:
        Movie1_list.append([i,item["id"]])
        if i>item["id"]:
            Movie_list.append((item["id"],i))
        else:
            Movie_list.append((i,item["id"]))
    time.sleep(0.25)
Set_list=set(Movie_list)

"""

Unique_list=[]
for j in Movie_list:
    if j in Unique_list:
        pass
    else:
        Unique_list.append(j)"""


f=open("movie_ID_sim_movie_ID.txt","w")
for item in range(0,len(Movie1_list)):
    f.write(str(Movie1_list[item][0])+","+str(Movie1_list[item][1])+"\n")
f.close()




