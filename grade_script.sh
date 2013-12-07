#!/usr/bin/env bash

echo 'grading'

cp -f /home/molu8455/projects/teaching/current/bitbucket/grading/lab-05/test_hello.py .
cp -f /home/molu8455/projects/teaching/current/bitbucket/grading/lab-05/compare.py .
cp -f /home/molu8455/projects/teaching/current/bitbucket/grading/lab-05/check_bugs.py .

sleep 2
python test_hello.py


sleep 2
python check_bugs.py

sleep 2
python compare.py -a ../data/matrix.500x -b ../data/matrix.500x
python compare.py -a ../data/matrix.1000x -b ../data/matrix.1000x
python compare.py -a ../data/matrix.1500x -b ../data/matrix.1500x
python compare.py -a ../data/matrix.2000x -b ../data/matrix.2000x
python compare.py -a ../data/matrix.2500x -b ../data/matrix.2500x

#rm -f output
#rm -f grade_script.sh
#rm -f compare.py
#rm -f test_hello.py
#rm -f check_bugs.py

sleep 2
name=$(basename `pwd`)
acount=$(cat grading.out | grep A_POINT  | wc -l)
bcount=$(cat grading.out | grep B_POINTS  | wc -l)
ccount=$(cat grading.out | grep C_POINTS  | wc -l)
echo $name,$acount,$bcount,$ccount >> /home/molu8455/projects/teaching/current/bitbucket/grading/lab-05/points.csv 

