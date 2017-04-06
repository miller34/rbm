#! /usr/bin/env python
import math
import sys
import random
import numpy as np
from collections import Counter
import argparse






def parseArgs():
	parser = argparse.ArgumentParser(description='Find Orthologs in MultiSpecies FASTA file.')
	parser.add_argument("-i",help="Input CSV File",action="store", dest="input",required=True)
	#parser.add_argument("-o",help="Output CSV File",action="store",dest="output", required=True)
	#parser.add_argument("-t",help="Number of Cores",action="store",dest="threads",default=1,type=int, required=False)
	parser.add_argument("-c",help="Number of Context Nodes",action="store",dest="contextNodes",type=int, required=True)
	parser.add_argument("-l",help="Number of Hidden Layers",action="store",dest="hiddenNum",default=2,type=int, required=False) ##how many layers of hidden nodes
	parser.add_argument("-n",help="Number of Hidden Nodes per Layer",action="store",dest="hiddenNodes",default=3,type=int, required=False) ##Number of hidden nodes per layer. Set equal to the number of initial instances...or whatever you want
	parser.add_argument("-g",help="Number of Instances to Generate",action="store",dest="numGenerate",default=5,type=int, required=False)
	parser.add_argument("-d",help="Max Weight to Dropout",action="store",dest="dropoutMax",default=0.001,type=float, required=False)
	parser.add_argument("-r",help="Number of Iterations through Input File",action="store",dest="numRepeats",default=1,type=int, required=False)
	args = parser.parse_args()
	return args

def setInitialWeights(contextNodes,hiddenNum,hiddenNodes):
	hiddenLayer = []
	upperBias = [] ###assuming num hidden nodes = num context nodes
	lowerBias = []
	lowerBias.append([])
	hiddenWeights = contextNodes ##Number of weights going to each node (i.e., the number of context nodes
	for _ in xrange(contextNodes):
		lowerBias[0].append(random.uniform(-0.5,0.5))
	###Check this part to make sure it's correct
	for x in xrange(hiddenNum):
		hiddenLayer.append([])
		upperBias.append([])
		if x+1 < hiddenNum:
			lowerBias.append([])
		for y in xrange(hiddenNodes):
			hiddenLayer[x].append([])
			for z in xrange(hiddenWeights):
				hiddenLayer[x][y].append(random.uniform(-0.5,0.5)) #x=hidden layer, y=hidden node, z=context node
			upperBias[x].append(random.uniform(-0.5,0.5))
			if x+1 < hiddenNum:
				lowerBias[x+1].append(random.uniform(-0.5,0.5))
		hiddenWeights = hiddenNodes ##For each layer after the context layer, the number of hidden weights will be equal to the number of nodes in the previous layer
	return hiddenLayer,upperBias,lowerBias


def getSample(percent,rd=random):
	if rd.random()> percent:
		return 1.0
	return 0.0


def hiddenOutput(context, hidden, uBias):
	net = sum([a*b for a,b in zip(context,hidden)]) + uBias
	percent = 0
	if net < -9:
		percent = 0
	elif net > 9:
		percent = 1
	else:
		percent = 1.0 /(1+math.e**(-1*net))

	return percent

def contextOutput(hiddenProb,lBias,hidden, node):
	netContext = 0
	for hPos in xrange(len(hiddenProb)):
		for hNode in xrange(len(hidden)):	
			netContext += (hiddenProb[hPos] * hidden[hNode][node]) #hidden output * hidden weight 
	fcout = 0
	if netContext < -9:
		fcout = 0
	elif netContext > 9:
		fcout = 1
	else:
		fcout = 1.0 /(1+math.e**(-1*netContext))
	return fcout

def layerOutput(contextI, uBiasL, hiddenL, curHidden): #Get output of specific layer from the context node
	context = contextI
	for layer in xrange(curHidden):
		hidden = hiddenL[layer]
		uBias = uBiasL[layer]
		curContext = []
		for node in xrange(len(hidden)):
			percent = hiddenOutput(context,hidden[node],uBias[node])
			sample = getSample(percent)
			curContext.append(sample)
		context = curContext[:]

	return context

def updateWeights(contextI, uBiasL, lBiasL, hiddenL,curHidden): #value for input (list), upper bias (list), and lower bias (list), weight for hiddenNodes (list)
	###creates the initial context/hidden layer for whatever layer you're trying to train
	context = layerOutput(contextI,uBiasL,hiddenL,curHidden)
	uBias = uBiasL[curHidden]
	lBias = lBiasL[curHidden]
	hidden = hiddenL[curHidden]
	##	
	
	learningRate = 0.001	
	#learningRate = 1	
	hiddenPerc = []
	hiddenProb = []
	for node in xrange(len(hidden)):	
		percent = hiddenOutput(context,hidden[node],uBias[node])
		sample = getSample(percent)
		hiddenPerc.append(percent)
		hiddenProb.append(sample)
	contextProb = []
	contextPerc = []
	for node in xrange(len(context)):
		percent =  contextOutput(hiddenProb,lBias[node],hidden,node)
		sample = getSample(percent)
		contextPerc.append(percent)
		contextProb.append(sample)
	
	finalHiddenPerc = []
	for node in xrange(len(hidden)):	
		percent = hiddenOutput(contextProb,hidden[node],uBias[node])
		sample = getSample(percent)
		finalHiddenPerc.append(percent)
	
	deltaLBias = [] #list of updates to all context biases
	deltaW = [] #list of updates to context node weights to hidden node
	deltaUBias = [] #list of updates to all hidden biases
	for x in xrange(len(hidden)):
		deltaW.append([])
		for y in xrange(len(context)):
			deltaW[x].append(learningRate*((hiddenProb[x]*context[y])-(finalHiddenPerc[x]*contextProb[y])))
		deltaUBias.append(learningRate*(hiddenPerc[x]-finalHiddenPerc[x]))
	for x in xrange(len(context)):
		deltaLBias.append(learningRate*(context[x]-contextProb[x]))
	#print deltaW
	return deltaW, deltaUBias, deltaLBias




def generate(hiddenL,lBiasL, contextLength):
	cProb = []
	cPerc = []
	net = []
	startLayer =1
	while len(hiddenL[-1*startLayer])==0:
		startLayer +=1
	for z in xrange(len(hiddenL[-1*startLayer])):
		cProb.append(random.randint(0,1)) 
	########print "Prob",cProb

	for layer in xrange(len(hiddenL)-startLayer,-1,-1):
		hidden = hiddenL[layer]
		lBias = lBiasL[layer]
		hProb = cProb[:]
		cProb = []
		cPerc = []
		net = []
		lenContext = 0
		if layer ==0:
			lenContext = contextLength
		else:
			lenContext = len(hiddenL[layer-1])
		#print lenContext
		for node in xrange(lenContext):
			percent =  contextOutput(hProb,lBias[node],hidden,node)
			sample = getSample(percent)
			cPerc.append(percent)
			cProb.append(sample)

	#return net
	##return cPerc
	return cProb

#for all hidden nodes, knowing all context nodes
##L1 weight decay = abs(theta)
##L2 weight decay = theta**2
#L1 =0.001
#L2 =0.001

def newWeight(deltaW, curVal):
	learningDecay = 0.001
	#return curVal + deltaW
	if curVal <0:
		curVal +=  deltaW + (learningDecay*(curVal**2))-(0.5*learningDecay*curVal)
		if curVal>0:
			return 0
		return curVal
	curVal += deltaW - (learningDecay*(curVal**2)) - (0.5*learningDecay*curVal)
	if curVal<0:
		return 0

	return curVal


def readFile(hiddenLayer,hiddenNum,upperBias,lowerBias,inputF,dropoutMax,numRepeats):
	for curHidden in xrange(hiddenNum):
		for _ in xrange(numRepeats):
			input = open(inputF)
			for line in input:
				#info = map(float, line.strip().upper().split(',')[0:-1])
				info = map(float, line.strip().upper().split(','))
				deltaW, deltaUBias, deltaLBias = updateWeights(info,upperBias,lowerBias,hiddenLayer,curHidden)
				for i in xrange(len(deltaUBias)):
					curVal = upperBias[curHidden][i]
					upperBias[curHidden][i] = newWeight(deltaUBias[i],curVal)
		
				for i in xrange(len(deltaLBias)):
					curVal = lowerBias[curHidden][i]
					lowerBias[curHidden][i] = newWeight(deltaLBias[i],curVal)
	
				allDrop = []
				for x in xrange(len(deltaW)):
					dropout = True
					for y in xrange(len(deltaW[x])):
						curVal = hiddenLayer[curHidden][x][y]
						newVal= newWeight(deltaW[x][y], curVal)
						hiddenLayer[curHidden][x][y] =newVal
						if abs(newVal)>dropoutMax:
							dropout =False
							continue
					if dropout:
						#print "all",x
						allDrop.append(x)
				for x in allDrop[::-1]:
					#print x
					del hiddenLayer[curHidden][x]
					del upperBias[curHidden][x]
					if curHidden<hiddenNum-1:
						del lowerBias[curHidden+1][x]
			input.close()


if __name__ =='__main__':
	args = parseArgs()
	dropoutMax =args.dropoutMax
	hiddenLayer,upperBias,lowerBias= setInitialWeights(args.contextNodes,args.hiddenNum,args.hiddenNodes)
	print "Layers=",len(hiddenLayer),"NumNodes=",args.hiddenNodes,"NumRepeats=",args.numRepeats
	readFile(hiddenLayer,args.hiddenNum,upperBias,lowerBias,args.input,args.dropoutMax,args.numRepeats)

	inputFile = open(args.input)
	allInfo = []
	for line in inputFile:
		allInfo.append(map(float,line.strip().split(",")))

	correct = 0
	incorrect = 0
	everything = []
	for i in xrange(args.numGenerate):
		seq=  generate(hiddenLayer, lowerBias,args.contextNodes)
		if seq in allInfo:
			correct +=1
			if seq[-1]==0:
				seq[-1] =1
			else:
				seq[-1] = 0
			#if seq in allInfo:
			#	print seq, "C", "I"
			#else:
			#	print seq, "C","C"
		else:
			if seq[-1]==0:
				seq[-1] =1
			else:
				seq[-1] = 0
			#if seq in allInfo:
			#	print seq, "I", "I"
			#else:
			#	print seq, "I","C"
			incorrect +=1
		if seq not in everything:
			everything.append(seq)
	print "correct",correct
	print "incorrect",incorrect
	print "Unique prediction:",len(everything)
	if len(everything)==1:
		print "OVERFIT!"
	print









