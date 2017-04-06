#! /usr/bin/env python
import numpy as np
import sys
import random
output = open(sys.argv[1],'w')

used = []
for _ in xrange(512):
	choice = np.random.choice([0,1],10,p=[0.2,0.8]).tolist()
	while choice in used:
		choice = np.random.choice([0,1],10,p=[0.2,0.8]).tolist()
	for x in choice:
		output.write(str(x) + ",")
	output.write("1\n")
	used.append(choice)
	choice = np.random.choice([0,1],10,p=[0.8,0.2]).tolist()
	while choice in used:
		choice = np.random.choice([0,1],10,p=[0.8,0.2]).tolist()
	for x in choice:
		output.write(str(x) + ",")
	output.write("0\n")
	used.append(choice)

output.close()
