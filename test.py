#!/usr/bin/python3
from funcs import *
from sys import argv

date = '13980901'
base_url = 'http://www.kanoon.ir/Public/TopStudents?main=1&group=1&date=%s&year=99'%date
post_url = 'http://www.kanoon.ir/Public/TopStudentsWorkbook'

up = open('up.txt', 'r')
date, lname, cad = up.read().split(' ')
cad = int(cad)
res = a_lesson(date, lname, cad)
print(lname, ': ', cad, ': ', res)
