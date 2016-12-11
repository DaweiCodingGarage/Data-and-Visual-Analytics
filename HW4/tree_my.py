# CSE6242/CX4242 Homework 4 Sketch Code
# Please use this outline to implement your decision tree. You can add any code around this.

import csv
import numpy as np
from math import log
import itertools
import sys

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
    
def InfoGain(QualityTotal, QualityBranchLeft, QualityBranchRight):
    entropy1=Entropy(QualityTotal)
    entropy2=Entropy(QualityBranchLeft)
    entropy3=Entropy(QualityBranchRight)
    infogain=entropy1-sum(QualityBranchLeft)/sum(QualityTotal)*entropy2-sum(QualityBranchRight)/sum(QualityTotal)*entropy3
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
    List1,List2,median=SplitBasedOnMedian(training_set)
    ListInfo,MAX,LeftQuality,RightQuality=[],0,{},{}
    for j in List_attr:
        Left=QualityTotal(List1[j])
        if any([i==0 for i in Left]):
            return j,median[j],List1[j],List2[j]
        LeftQuality[j]=Left
    for j in List_attr:
        Right=QualityTotal(List2[j])
        if any([i==0 for i in Right]):
            return j,median[j],List1[j],List2[j]
        RightQuality[j]=Right 
    for i in List_attr:
        gain=InfoGain(TotalQuality,LeftQuality[i],RightQuality[i])
        ListInfo.append((i,gain))
        if gain>MAX: MAX=gain
    attr=[ListInfo[i][0] for i in range(len(ListInfo)) if ListInfo[i][1]==MAX][0]
    return attr,median[attr],List1[attr],List2[attr]
   
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
    Best,Split,List1,List2=BestAttr(data,List_attr)
    Split=round(Split,4)
    tree={Best:{}}
    Dict={Split:List1,-Split:List2}
    for key,val in Dict.iteritems():
        subtree=create_decision_tree(val,[i for i in range(11) if i!=Best])
        tree[Best][key]=subtree
    return tree

    # implement this function
def classify(tree,instance):
    if not type(tree)==dict:
        return tree
    attr_index1=list(tree.keys())[0]#10
    attr_values1=list(tree.values())[0]#rest of tree
    attr_index2=abs(attr_values1.keys()[0])#median
    attr_index3=attr_values1.keys()[0]#median 
    attr_index4=attr_values1.keys()[1]#median 
    attr_values2=attr_values1[attr_index3]#subtree
    attr_values3=attr_values1[attr_index4]#subtree
    instance_attr=float(instance[attr_index1])
    if instance_attr<attr_index2:
        if attr_index3>0:
            return classify(attr_values2,instance)
        else:
            return classify(attr_values3,instance)
    else:
        if attr_index3>0:
            return classify(attr_values3,instance)
        else:
            return classify(attr_values2,instance)

def run_decision_tree():
      sys.setrecursionlimit(1500)
    # Load data set
    with open("hw4-data.csv") as f:
        next(f, None)
        data = [tuple(line) for line in csv.reader(f, delimiter=",")]
    print "Number of records: %d" % len(data)

    # Split training/test sets
    # You need to modify the following code for cross validation.
    K = 10
    Accuracies=[]
    f = open(myname+"result.txt", "w")
    for j in range(10):
        training_set = [x for i, x in enumerate(data) if i % K != j]
        test_set = [x for i, x in enumerate(data) if i % K == j]
    
        List_attr=range(11)
        tree= create_decision_tree(training_set,List_attr)

    # Classify the test set using the tree we just constructed
        results = []
        for instance in test_set:
            result = classify(tree,instance[:-1] )
            results.append( int(result) == int(instance[-1]))

    # Accuracy
        accuracy = float(results.count(True))/float(len(results))
        print "accuracy: %.4f" % accuracy
        Accuracies.append(accuracy)
        f.write("accuracy: %.4f" % accuracy)
    
    mean=np.mean(np.array(Accuracies))
    print mean
 
    # Writing results to a file (DO NOT CHANGE)
    f.write("mean of accuracy: %.4f" % mean)
    
    f.close()


if __name__ == "__main__":
    run_decision_tree()
