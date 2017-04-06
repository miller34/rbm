#! /usr/bin/env python
import numpy as np
import sys
import random
output = open(sys.argv[1],'w')


for _ in xrange(1000):
	choice = np.random.choice([0,1],3,p=[0.1,0.9])
	for x in choice:
		output.write(str(x) + ",")
	output.write("0.01,0.01,0.01,1\n")
for _ in xrange(1000):
	output.write("0.01,0.01,0.01,")
	choice = np.random.choice([0,1],3,p=[0.1,0.9])
	for x in choice:
		output.write(str(x) + ",")
	output.write("0\n")

output.close()
