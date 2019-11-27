#!/usr/bin/python3
from funcs import *
from sys import argv

date = '13980901'
base_url = 'http://www.kanoon.ir/Public/TopStudents?main=1&group=1&date=%s&year=99'%date
post_url = 'http://www.kanoon.ir/Public/TopStudentsWorkbook'

# extract_data(date, base_url, post_url)
# lname = 'آمارواحتمال'
# cad = 1
date, lname, cad = argv[1], argv[2], int(argv[3])
res = a_lesson(date, lname, cad)
print(cad, ': ', res)