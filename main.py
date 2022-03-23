import random
import numpy as np
import copy
import csv
import pandas as pd

INPUTS = 7


class Gene:
    def __init__(self,inp,):
        self.inputNodes = inp
        self.inputConnectionsAmt = random.randint(0,INPUTS//2)
        self.connections = self.inputConnectionsAmt
        self.outputConnectionsAmt = 0

        self.inputConnections = []
        self.outputConnections = []
        self.inputMatrix = 2*np.random.rand(self.inputConnectionsAmt,self.inputConnectionsAmt)-1
        self.outMatrix = (2*np.random.rand(self.inputConnectionsAmt,1)-1)
        for x in range(self.inputConnectionsAmt):
            inputNodeIndex = random.randint(0,len(self.inputNodes)-1)
            self.inputConnections.append(self.inputNodes[inputNodeIndex])
            self.inputNodes.pop(inputNodeIndex)
        self.generateMatrixAfterRun()
    def generateMatrixAfterRun(self,scm=0.1):
        self.inputMatrix = self.inputMatrix + np.random.normal(loc=0,scale=1*scm,size=self.inputMatrix.shape)
        self.outMatrix = self.outMatrix + np.random.normal(loc=0,scale=1*scm,size=self.outMatrix.shape)
        if random.random() > 0.90:
            add = random.random()
            if len(self.inputConnections) != 0 and add < 0.0:

                row=random.randint(0,len(self.inputConnections)-1)
                self.inputNodes.append(self.inputConnections.pop(row))
                self.inputMatrix = np.delete(self.inputMatrix,np.s_[row],1)
                self.outMatrix = np.delete(self.outMatrix,row)
                self.inputConnectionsAmt -= 1

            elif len(self.inputNodes) != 0:
                inpReadjCol = (2*np.random.rand(len(self.inputConnections),1)-1).reshape(len(self.inputConnections),1)
                inpReadjRow = (2*np.random.rand(len(self.inputConnections)+1,1)-1).reshape(1,len(self.inputConnections)+1)
                outReadj =(2*np.random.rand(1)-1).reshape(1,1)
                self.inputMatrix=np.c_[self.inputMatrix,inpReadjCol]
                self.inputMatrix=np.r_[self.inputMatrix,inpReadjRow]
                self.outMatrix = np.r_[self.outMatrix,outReadj]
                inputNodeIndex = random.randint(0,len(self.inputNodes)-1)
                self.inputConnections.append(self.inputNodes[inputNodeIndex])
                self.inputNodes.pop(inputNodeIndex)
                
                self.inputConnectionsAmt += 1

        #print(self.inputMatrix)
    def getVal(self):
        inpArray = []
        for item in self.inputConnections:
            inpArray.append(item.getVal())
        inpMatrix = np.array(inpArray)
        r1=np.matmul(inpArray,self.inputMatrix)
        r2=np.matmul(r1,self.outMatrix)
        return r2[0]

class InputNode:
    def __init__(self,val):
        self.val = val
    def setVal(self,val):
        self.val = val
    def getVal(self):
        return self.val

class Being:
    def __init__(self,inp):
        self.inp = inp
        self.value = 100.0
        self.buying = True
        self.L1Genes = []
        self.L2Genes = []
        for _ in range(5):
            self.L1Genes.append(Gene(copy.copy(inp)))


        for _ in range(5):
            tempArr = copy.copy(inp) + copy.copy(self.L1Genes)
            self.L2Genes.append(Gene(tempArr))
    def setInp(self,inp):
        for _ in range(len(inp)):
            self.inp[_].setVal(inp[_].getVal()) 
    def createOffSpring(self):
        offspring = copy.deepcopy(self)
        offspring.calcAllGenes()
        return offspring
    def calcAllGenes(self):
        for gene in self.L1Genes:
            gene.generateMatrixAfterRun()
        for gene in self.L2Genes:
            gene.generateMatrixAfterRun()
    def outVal(self):
        total = 0
        for gene in self.L2Genes:
            total+=gene.getVal()
        return total
    def doAction(self,price):
        if self.outVal() > 0 and self.buying: ##Buy
            self.value = self.value/price
            self.value *=0.999
            self.buying = False
        if self.outVal() < 0 and not self.buying:
            self.value = self.value*price
            self.value *=0.999
            self.buying = True
    def printOptions(self,p):
        if self.outVal() > 0 and self.buying: ##Buy
            print("I have",self.value,"USD , im going to buy",self.value/p,"doge"," for",p)
            print("SHOULD BUY")
        if self.outVal() < 0 and not self.buying:
            print("I have",self.value,"Doge , im going to buy",self.value*p,"usd"," for",p)
            print("SHOULD SELL")

    def getScore(self,price):
        if not self.buying:
            return self.value*price
        else: return self.value


def loadData(filename):
    df = pd.read_csv(filename)
    print(df)
    df = df.replace(',','', regex=True)
    col = df.Open.astype(float)
    return col[::-1]




testData=[99,4,5,3,2,6,8,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,17,13,5,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,1,1,1,1,1]
testData = loadData("FTSEDATA.csv")
allInputNodes = []
offset =INPUTS-1 
      
for _ in range(offset,len(testData)):
    entryNodes = []
    entryNodes.append(InputNode(testData[_]))  
    for x in range(1,INPUTS):
        entryNodes.append(InputNode(testData[_]-testData[_-x]))
    allInputNodes.append(entryNodes)


MAXBEINGS = 500
allBeings = []
for _ in range(MAXBEINGS):
    testBeing = Being(allInputNodes[0])

    allBeings.append(testBeing)

    print(testBeing.outVal())

for _ in range(5):
    laps = INPUTS-1
    for y in range(1,len(allInputNodes)):
        allVal = []
        for being in allBeings:
            being.setInp(allInputNodes[y])
        for being in allBeings:
            val=being.inp[0].getVal()
            being.doAction(val)
            if y % laps == 0:
                allVal.append([being.getScore(val),being])
        if y % laps ==0:
            allVal =sorted(allVal,key=lambda x: x[0],reverse=True)
            allVal = allVal[0:(len(allBeings)//10)-1]
            allBeings = []
            for val in allVal:
                allBeings.append(val[1])
            while len(allBeings) < MAXBEINGS:
                for val in allVal:
                        allBeings.append(val[1].createOffSpring())
            print(allVal[0][0])
            print("AMT:"+str(len(allBeings)))
            lastBeing = allVal[0][1]
            allVal = []
            for being in allBeings:
                being.value = 100
                being.buying = True
        

    print("-----------")
    lastBeing.value = 100  
    lastBeing.buying = True     
    for item in allInputNodes:       
        lastBeing.setInp(item)
        lastBeing.printOptions(item[0].getVal())
        lastBeing.doAction(item[0].getVal())

        print(lastBeing.getScore(item[0].getVal()))
    input()
    

        






"""
testGene = Gene(entryNodes)
for _ in range(random.randint(10,100)):
    testGene.generateMatrixAfterRun()
print(testGene.getVal())
"""
