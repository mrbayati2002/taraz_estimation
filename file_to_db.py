#!/usr/bin/python3

import sqlite3
from sys import argv

date = argv[1]
con = sqlite3.connect('dbs/%s.db'%date)
c = con.cursor()

def lname_remove_spaces(lname):
    s = ''
    for c in lname:
        if c not in [' ', '-', ',', '.', ':']:
            s += c
    return s

def lname_exr(lname):
    l = 0
    while lname[l] in [' ', '.', ':', '\t'] and l < len(lname):
        l += 1
    r = len(lname) - 1
    while lname[r] in [' ', '.', ':', '\t'] and r >= 0:
        r -= 1
    r += 1
    return lname[l:r]

l = 1
r = 99
for cf in range(l, r + 1):
    # with open('tests/%s/test%s.txt'%(date, str(cf), 'r')) as f:
    with open('tests/test%s.txt'%str(cf), 'r') as f:
        for i in f:
            lname, count, taraz, tmp = i.split('\t')
            lname = lname_remove_spaces(lname_exr(lname))
            count = int(count)
            taraz = int(taraz)
            c.execute('CREATE TABLE IF NOT EXISTS %s(count INT, taraz INT)'%lname)
            c.execute('INSERT INTO %s VALUES(%i, %i)'%(lname, count, taraz))
    print(cf)

con.commit()
print('done')
