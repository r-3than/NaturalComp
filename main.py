import random
import numpy as np
import copy
INPUTS = 4


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
    def generateMatrixAfterRun(self):
        self.inputMatrix = self.inputMatrix + np.random.normal(loc=0,scale=1,size=self.inputMatrix.shape)
        self.outMatrix = self.outMatrix + np.random.normal(loc=0,scale=1,size=self.outMatrix.shape)
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
        for _ in range(10):
            self.L1Genes.append(Gene(copy.copy(inp)))
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
    def outVal(self):
        total = 0
        for gene in self.L1Genes:
            total+=gene.getVal()
        return total
    def doAction(self,price):
        if self.outVal() > 0 and self.buying: ##Buy
            self.value = self.value/price
            self.value *=0.999
            self.buying = False
        elif self.outVal() < 0 and not self.buying:
            self.value = self.value*price
            self.value *=0.999
            self.buying = True
    def getScore(self,price):
        if not self.buying:
            return self.value*price
        else: return self.value



testData=[1,4,5,3,2,6,8,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,17,13,5,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5,4,2,4,10,12,15,17,13,5]
allInputNodes = []
offest =3 
      
for _ in range(3,len(testData)):
    entryNodes = []  
    for x in range(4):
        entryNodes.append(InputNode(testData[_]-testData[x]))
    allInputNodes.append(entryNodes)


MAXBEINGS = 500
allBeings = []
for _ in range(MAXBEINGS):
    testBeing = Being(allInputNodes[0])

    allBeings.append(testBeing)

    print(testBeing.outVal())

laps = 3
for y in range(1,len(allInputNodes)):
    allVal = []
    for being in allBeings:
        val=being.inp[0].getVal()
        being.doAction(val)
        if y % laps == 0:
            allVal.append([being.getScore(val),being])
    if y % laps ==0:
        allVal =sorted(allVal,key=lambda x: x[0],reverse=True)
        allVal = allVal[0:49]
        allBeings = []
        for val in allVal:
            allBeings.append(val[1])
        for val in allVal:
            for _ in range(10):
                allBeings.append(val[1].createOffSpring())
        print(allVal[0][0])
        allVal = []
        for being in allBeings:
            being.value = 100
    for being in allBeings:
        being.setInp(allInputNodes[y])
            
        






"""
testGene = Gene(entryNodes)
for _ in range(random.randint(10,100)):
    testGene.generateMatrixAfterRun()
print(testGene.getVal())
"""
