#!/bin/bash
source /etc/profile
date >> /home/zkr/testcron.txt
/home/zkr/anaconda2/bin/python /home/zkr/pyWorkSpace/For_Majesty/reconstruct/src/main_test.py
