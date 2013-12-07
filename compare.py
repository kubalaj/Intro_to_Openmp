#!/usr/bin/env python
import sys
import argparse
import time
import numpy as np
import tables as tb
import subprocess
import os


def get_args(argv):
    parser = argparse.ArgumentParser()  
    parser.add_argument('-a', help='matrix.A')
    parser.add_argument('-b', help='matrix.B')
    return parser.parse_args(argv)

def read_h5(filename):
    filename = filename
    h5 = tb.openFile(filename, mode = "r")
    X = h5.root.x.read()
    h5.close()
    return X

def execute(fileA, fileB):

    if not fileA or not fileB:
        print 'please specify both -a and -b'
        exit()

    # Call python
    start = time.time()
    A = read_h5(fileA)
    B = read_h5(fileB)
    C = np.dot(A,B)
    python_time = time.time() - start

    start = time.time()
    cmd = 'export OMP_NUM_THREADS=1; make run A=' + fileA + ' B=' + fileB + ' C=output'
    pid = subprocess.Popen(cmd, shell=True)
    pid.wait()
    omp_num_1 = time.time() - start

    #Call your code
    start = time.time()
    cmd = 'export OMP_NUM_THREADS=12; make run A=' + fileA + ' B=' + fileB + ' C=output'
    pid = subprocess.Popen(cmd, shell=True)
    pid.wait()
    omp_num_12 = time.time() - start

    try:
        #Check the accuracy
        D = read_h5('output')
        accuracy = np.sum(abs(C-D)) 
    except IOError:
        print "IOERROR: could not open output file"
        accuracy = np.sum(abs(C)) 
    
    return accuracy, omp_num_1, omp_num_12


if __name__ == '__main__':

    args = get_args(sys.argv[1:])

    values = execute(args.a, args.b)

    print "accuracy:   ", values[0]
    print "1 thread:   ", values[1]
    print "12 threads: ", values[2]
    print "speedup:    ", values[1]/float(values[2])

    speedup = values[1]/float(values[2])

    if args.a == '../data/matrix.500x':
        threshold = 1.75
    if args.a == '../data/matrix.1000x':
        threshold = 7
    if args.a == '../data/matrix.1500x':
        threshold = 8
    if args.a == '../data/matrix.2000x':
        threshold = 8.5
    if args.a == '../data/matrix.2500x':
        threshold = 9
    else:
        threshold = 1
    try:
        with open('/home/molu8455/projects/teaching/current/bitbucket/grading/lab-05/results.csv','a') as results:
            name = os.path.split(os.getcwd())[1]
            results.write(name + ',' + args.a.split('/')[-1] + ',' + str(values[0]) + ',' + str(values[1]) + ',' + str(speedup) + '\n')
    except:
        pass

    if values[0] < 1e-2:
        print 'accuracy'
        print 'C_POINTS:    5'
    
        if speedup > threshold:
            print 'C_POINTS:    5    for speedup', threshold           


