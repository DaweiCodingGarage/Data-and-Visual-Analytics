import csv
import numpy as np
from math import log
import itertools
import sys


# Enter You Name Here
myname = "Dawei-Geng-" 
# count how many 0's and 1's in this branch
def QualityTotal(training_set):
    quality=[int(training_set[i][11]) for i in range(len(training_set))]
    QualityCountY, QualityCountN=0.0,0.0
    for j in range(len(quality)):
        if quality[j]==1:
            QualityCountY+=1
        else:
            QualityCountN+=1
    return (QualityCountY, QualityCountN)


#split according to median
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
#split into three branches

def SplitThreeBranch(training_set):
    Col,median,List_left,List_mid,List_right=[],[],[],[],[]
    for j in range(len(training_set[0])-1):
        Col.append([float(training_set[i][j]) for i in range(len(training_set))])
        median.append(np.percentile(Col[j],[5,95]))
        left=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])<=median[j][0]]
        right=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])>median[j][1]]
        mid=[training_set[i] for i in range(len(training_set)) if float(training_set[i][j])<median[j][1] and float(training_set[i][j])>median[j][0]]
        List_mid.append(mid)
        List_left.append(left)
        List_right.append(right)
    return List_left, List_mid, List_right,median
#random pick number to split

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
#compute entropy
def Entropy(Quality):
    entropy=-(Quality[0]/(Quality[0]+Quality[1]))*log((Quality[0]/(Quality[0]+Quality[1])),2)-(Quality[1]/(Quality[0]+Quality[1]))*log((Quality[1]/(Quality[0]+Quality[1])),2)
    return entropy 
#compute information gain    
def InfoGain(QualityTotal, QualityBranchLeft,QualityBranchMid,QualityBranchRight):
    entropy1=Entropy(QualityTotal)
    entropy2=Entropy(QualityBranchLeft)
    entropy3=Entropy(QualityBranchRight)
    entropy4=Entropy(QualityBranchMid)
    infogain=entropy1-sum(QualityBranchLeft)/sum(QualityTotal)*entropy2-sum(QualityBranchRight)/sum(QualityTotal)*entropy3-sum(QualityBranchMid)/sum(QualityTotal)*entropy4
    return infogain
#compute the most frequent number in a branch
def major_num(List):
    num1=[List[i][11] for i in range(len(List))].count(1)
    num2=[List[i][11] for i in range(len(List))].count(0)
    if num1>num2:
        return 1
    else:
        return 0
#return number according to the IsAllSame function
def Return_Num(List):
    num1=[List[i][11] for i in range(len(List))].count(1)
    num2=[List[i][11] for i in range(len(List))].count(0)
    if num1==len(List):
        return 1
    elif num2==len(List):
        return 0
#check if all are same in the quality
def IsAllSame(List):
    num1=[List[i][11] for i in range(len(List))].count(1)
    num2=[List[i][11] for i in range(len(List))].count(0)
    if num1==len(List) or num2==len(List):
        return True
    else:
        return False
#find the best attribute
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
   
# create decision tree below
def create_decision_tree(data,List_attr):
    tree={}
    default=major_num(data)
    if not data:
        return default
    elif IsAllSame(data):
        return Return_Num(data)
    elif len(data)==1:
       return major_num(data)
    Best,Split,List1,List2,List3=BestAttr(data,List_attr)
    if Split[0]==Split[1]:
        return major_num(data)
    Split1=round(Split[0],6)
    Split2=round(Split[1],6)
    tree={Best:{}}
    Dict={Split1:List1,Split2:List3,'Mid':List2}
    for key,val in Dict.iteritems():
        subtree=create_decision_tree(val,[i for i in range(11) if i!=Best])
        tree[Best][key]=subtree
    return tree

# classify based on trained data
def classify(tree,instance):
    if not type(tree)==dict:
        return tree
    attr_index1=list(tree.keys())[0]#10
    attr_values1=list(tree.values())[0]#rest of tree
    attr_index=attr_values1.keys()#median
    attr_index2='Mid'
    attr_index.remove('Mid')#mid
    if len(attr_index)==1:
        return attr_values1[attr_index[0]]
    elif attr_index[0]>attr_index[1]:
        attr_index3=attr_index[0]#big
        attr_index4=attr_index[1]#small
    else:
        attr_index3=attr_index[1]
        attr_index4=attr_index[0]
    attr_values2=attr_values1[attr_index2]#subtree mid
    attr_values3=attr_values1[attr_index3]#subtree big
    attr_values4=attr_values1[attr_index4]#subtree small
    
    instance_attr=float(instance[attr_index1])
    if instance_attr<=attr_index4:
        return classify(attr_values4,instance)
    elif instance_attr>=attr_index3:
        return classify(attr_values3,instance)
    else:
        return classify(attr_values2,instance)
#run decision tree
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
        #print tree
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
