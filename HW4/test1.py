
import csv
import numpy as np
from math import log
import itertools

# Enter You Name Here
myname = "Dawei-Geng-" 

def QualityTotal(training_set):
    quality=[int(training_set[i][11]) for i in range(len(training_set))]
    QualityCountY, QualityCountN=0.0,0.0
    for j in range(len(quality)):
        if quality[j]==1:
            QualityCountY+=1
        else:
            QualityCountN+=1
    return (QualityCountY, QualityCountN)


#sort according to median
def SplitBasedOnMedian(training_set):
    Col,median,List_left,List_right=[],[],[],[]
    for j in range(len(training_set[0])-1):
        Col.append([float(training_set[i][j]) for i in range(len(training_set))])
        median.append(np.median(np.array(Col[j])))
        left=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])<=median[j]]
        right=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])>median[j]]
        List_left.append(left)
        List_right.append(right)
    return List_left, List_right,median

def SplitThreeBranch(training_set):
    Col,median,List_left,List_mid,List_right=[],[],[],[],[]
    for j in range(len(training_set[0])-1):
        Col.append([float(training_set[i][j]) for i in range(len(training_set))])
        median.append(np.percentile(Col[j],[33.3,66.6]))
        left=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])<=median[j][0]]
        right=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])>median[j][1]]
        mid=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])<median[j][1] and float(training_set[i][j])>median[j][0]]
        List_mid.append(mid)
        List_left.append(left)
        List_right.append(right)
    return List_left, List_mid, List_right,median

def random_pick(training_set):
    Col,pick,List_left,List_right=[],[],[],[]
    for j in range(len(training_set[0])-1):
        Col.append([float(training_set[i][j]) for i in range(len(training_set))])
        pick.append(np.random.choice(Col[j]))
        left=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])<=pick[j]]
        right=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])>pick[j]]
        List_left.append(left)
        List_right.append(right)
    return List_left, List_right,pick

def Entropy(Quality):
    entropy=-(Quality[0]/(Quality[0]+Quality[1]))*log((Quality[0]/(Quality[0]+Quality[1])),2)-(Quality[1]/(Quality[0]+Quality[1]))*log((Quality[1]/(Quality[0]+Quality[1])),2)
    return entropy 
    
def InfoGain(QualityTotal, QualityBranchLeft,QualityBranchMid,QualityBranchRight):
    entropy1=Entropy(QualityTotal)
    entropy2=Entropy(QualityBranchLeft)
    entropy3=Entropy(QualityBranchRight)
    entropy4=Entropy(QualityBranchMid)
    infogain=entropy1-sum(QualityBranchLeft)/sum(QualityTotal)*entropy2-sum(QualityBranchRight)/sum(QualityTotal)*entropy3-sum(QualityBranchMid)/sum(QualityTotal)*entropy4
    return infogain

def major_num(List):
    num1=[List[i][11] for i in range(len(List))].count(1)
    num2=[List[i][11] for i in range(len(List))].count(0)
    if num1>num2:
        return 1
    else:
        return 0
def Return_Num(List):
    num1=[List[i][11] for i in range(len(List))].count(1)
    num2=[List[i][11] for i in range(len(List))].count(0)
    if num1==len(List):
        return 1
    elif num2==len(List):
        return 0
def IsAllSame(List):
    num1=[List[i][11] for i in range(len(List))].count(1)
    num2=[List[i][11] for i in range(len(List))].count(0)
    if num1==len(List) or num2==len(List):
        return True
    else:
        return False

def BestAttr(training_set,List_attr):
    TotalQuality=QualityTotal(training_set)
    List1,List3,List2,median=SplitThreeBranch(training_set)
    ListInfo,MAX,LeftQuality,RightQuality,MidQuality=[],0,{},{},{}
    for j in List_attr:
        Left=QualityTotal(List1[j])
        if any([i==0 for i in Left]):
            return j,median[j],List1[j],List2[j],List3[j]
        LeftQuality[j]=Left
    for j in List_attr:
        Right=QualityTotal(List2[j])
        if any([i==0 for i in Right]):
            return j,median[j],List1[j],List2[j],List3[j]
        RightQuality[j]=Right
    for j in List_attr:
        Mid=QualityTotal(List3[j])
        if any([i==0 for i in Mid]):
            return j,median[j],List1[j],List2[j],List3[j]
        MidQuality[j]=Mid 
    for i in List_attr:
        gain=InfoGain(TotalQuality,LeftQuality[i],MidQuality[i],RightQuality[i])
        ListInfo.append((i,gain))
        if gain>MAX: MAX=gain
    attr=[ListInfo[i][0] for i in range(len(ListInfo)) if ListInfo[i][1]==MAX][0]
    return attr,median[attr],List1[attr],List2[attr],List3[attr]
   
# Implement your decision tree below
def create_decision_tree(data,List_attr):
    tree={}
    default=major_num(data)
    if not data:
        return default
    elif IsAllSame(data):
        return Return_Num(data)
    elif len(data)<20:
       return major_num(data)
    Best,Split,List1,List2,List3=BestAttr(data,List_attr)
    Split1=round(Split[0],3)
    Split2=round(Split[1],3)
    tree={Best:{}}
    Dict={Split1:List1,Split2:List3,'Mid':List2}
    for key,val in Dict.iteritems():
        subtree=create_decision_tree(val,[i for i in range(11) if i!=Best])
        tree[Best][key]=subtree
    return tree

with open("hw4-data.csv") as f:
    next(f, None)
    data = [tuple(line) for line in csv.reader(f, delimiter=",")]
print "Number of records: %d" % len(data)

K = 10
training_set = [x for i, x in enumerate(data) if i % K != 9]
test_set = [x for i, x in enumerate(data) if i % K == 9]
List1,List3,List2,median=SplitThreeBranch(training_set)
print median
'''
attr=range(11)
tree= create_decision_tree(training_set,attr)
from pprint import pprint
pprint(tree)'''
