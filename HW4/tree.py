# CSE6242/CX4242 Homework 4 Sketch Code
# Please use this outline to implement your decision tree. You can add any code around this.

import csv
import numpy as np
from math import log
import itertools

# Enter You Name Here
myname = "Dawei-Geng" 

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
class DecisionTree(): 

    def learn(self, data,List_attr):
        # implement this function
        self.tree={}
        default=major_num(data)
        if not data:
            return default
        elif IsAllSame(data):
            return Return_Num(data)
        elif len(data)<200:
           return major_num(data)
        Best,Split,List1,List2=BestAttr(data,List_attr)
        Split=round(Split,3)
        self.tree={Best:{}}
        Dict={Split:List1,-Split:List2}
        for key,val in Dict.iteritems():
            subtree=self.learn(val,[i for i in range(11) if i!=Best])
            self.tree[Best][key]=subtree       

    # implement this function
    def classify(self, instance):
     # baseline: always classifies as 0
        if not type(tree)==dict:
            return tree
        attr_index1=list(tree.keys())[0]#10
        attr_values1=list(tree.values())[0]#rest of tree
        attr_index2=abs(attr_values1.keys()[0])#median
        attr_index3=attr_values1.keys()[0]#median 
        attr_index4=attr_values1.keys()[1]#median 
        attr_values2=attr_values1[attr_index3]#subtree
        attr_values3=attr_values1[attr_index4]#subtree
        instance_attr=instance[attr_index1]
        print attr_index1, attr_index3,attr_index4
        #print attr_values1,attr_values2,attr_values3
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

    # Load data set
    with open("hw4-data.csv") as f:
        next(f, None)
        data = [tuple(line) for line in csv.reader(f, delimiter=",")]
    print "Number of records: %d" % len(data)

    # Split training/test sets
    # You need to modify the following code for cross validation.
    K = 10
    training_set = [x for i, x in enumerate(data) if i % K != 9]
    test_set = [x for i, x in enumerate(data) if i % K == 9]
    
    tree = DecisionTree()
    # Construct a tree using training set
    List_attr=range(11)
    tree.learn( training_set,List_attr)

    # Classify the test set using the tree we just constructed
    results = []
    for instance in test_set:
        result = tree.classify( instance[:-1] )
        results.append( result == instance[-1])

    # Accuracy
    accuracy = float(results.count(True))/float(len(results))
    print "accuracy: %.4f" % accuracy       
    

    # Writing results to a file (DO NOT CHANGE)
    f = open(myname+"result.txt", "w")
    f.write("accuracy: %.4f" % accuracy)
    f.close()


if __name__ == "__main__":
    run_decision_tree()
