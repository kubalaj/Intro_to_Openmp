#!/usr/bin/env python

import subprocess
import os
import numpy as np

# does the file exists?
if os.path.exists('hello_world.c'):
	print 'A_POINT 1: file exists'
else:
	print 'ERROR: Cannot file hello_world.c'
	exit(1)

# does it compile without openmp?
cmd = 'gcc  hello_world.c -o aout'
pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid.wait()
if os.path.exists('aout'):
	print 'A_POINT 1: compiles without openmp'
else:
	print 'ERROR: does not compile without openmp'

os.remove('aout')

# does it compile with openmp?
cmd = 'gcc -fopenmp hello_world.c -o aout'
pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid.wait()
if os.path.exists('aout'):
	print 'A_POINT 1: compiles with openmp'
else:
	print 'ERROR: does not compile with openmp'
	exit(1)

# output
cmd = './aout'
pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid.wait()
out, err = pid.communicate()

threads = []
for line in out.split('\n'):
	try:
		threads.append(int(line.split(':')[1]))
	except IndexError:
		pass
if np.array(threads).sum() == 78:
	print 'A_POINT 1: Correct number of threads'
	print 'A_POINT 1: Output looks correct'
else:
	print 'ERROR: something is wrong with your output'
	exit(1)








