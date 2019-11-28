#!/usr/bin/python3

import sqlite3
from sys import argv
from funcs import lname_exr, lname_remove_spaces, create_table, ins_to_table

date = argv[1]
con = sqlite3.connect('dbs/%s.db'%date)
c = con.cursor()

l = 1
r = 99
for cf in range(l, r + 1):
    # with open('tests/%s/test%s.txt'%(date, str(cf), 'r')) as f:
    with open('tests/test%s.txt'%str(cf), 'r') as f:
        for i in f:
            lname, count, taraz, tmp = i.split('\t')
            count ,taraz = int(count), int(taraz)
            create_table(lname, con, c)
            ins_to_table(lname, count, taraz, con, c)
    print(cf)

con.commit()
print('done')
