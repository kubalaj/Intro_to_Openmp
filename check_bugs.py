#!/usr/bin/env python

# bug number one
import subprocess
import os
import numpy as np

# BUG ONE
if os.path.exists('omp_bug1.c'):
	print 'omp_bug1.c file exists'
else:
	print 'ERROR: Cannot file omp_bug1.c'

cmd = 'gcc -fopenmp omp_bug1.c -o aout'
pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid.wait()
if os.path.exists('aout'):
	print 'B_POINTS 5: omp_bug1.c compiles with openmp'
else:
	print 'ERROR: does not compile with openmp'

# BUG TWO
if os.path.exists('omp_bug2.c'):
	print 'omp_bug2.c file exists'

	cmd = 'gcc -fopenmp omp_bug2.c -o aout'
	pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	pid.wait()
	if os.path.exists('aout'):
		print 'compiles with openmp'

		cmd = './aout'
		pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		pid.wait()
		out, err = pid.communicate()

		number_of_lines = 0
		try:
			for lines in out.split('\n'):
				if lines.find('Total')>=0:
					if float(lines.split('=')[1]) > 4.9e11 and float(lines.split('=')[1]) < 5.1e11:
						number_of_lines+=1
		except:
			pass
		if number_of_lines == 12:
			print 'B_POINTS 5: omp_bug2 correct result'
		else:
			print 'ERROR: omp_bug2 does not give the correct results'
	else:
		print 'ERROR: does not compile with openmp'
else:
	print 'ERROR: Cannot file omp_bug2.c'


# Bug three
if os.path.exists('omp_bug3.c'):
	print 'B_POINTS 5: omp_bug3'
else:
	print 'ERROR: Cannot file omp_bug3.c'

# Bug four
if os.path.exists('omp_bug4.c'):
	print 'omp_bug4.c file exists'

	cmd = 'gcc -fopenmp omp_bug4.c -o aout'
	pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	pid.wait()
	if os.path.exists('aout'):
		print 'compiles with openmp'
		cmd = './aout'
		pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		pid.wait()
		out, err = pid.communicate()
		
		res = 0
		try:
			for lines in out.split('\n'):
				#print lines, lines.find('Sum')
				if lines.find('Sum')>=0:
					res = int(float(lines.split('=')[1]))
		except:
			pass
		if res == 328350:
			print 'B_POINTS 5: omp_bug4 correct result'
		else:
			print 'ERROR: omp_bug4 does not give the correct results'

	else:
		print 'ERROR: does not compile with openmp'
else:
	print 'ERROR: Cannot file omp_bug4.c'









