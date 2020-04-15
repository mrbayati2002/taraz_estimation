#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import csv  
from sklearn import tree
import sqlite3
import sys


def create_table(lname, con, c):
    lname = lname_remove_spaces(lname_exr(lname))
    c.execute('CREATE TABLE IF NOT EXISTS %s(count INT, taraz INT)'%lname)

def ins_to_table(lname, cnt, trz, con, c):
    lname = lname_remove_spaces(lname_exr(lname))
    c.execute('INSERT INTO %s VALUES(%i, %i)'%(lname, cnt, trz))

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

def conv_lname(lname):
    new_lname = ''
    names = {
        'آمارواحتمال' : 'amrehtml',
        'آمارواحتمالگواه' : 'amrehtmlgvh',
        'ادبيات' : 'adbt',
        'حساباندوازدهم' : 'hsbn2',
        'دينوزندگي1' : 'dni1',
        'دينوزندگي3دوازدهم' : 'dni3',
        'رياضي' : 'ryz',
        'رياضياتگسستهدوازدهم' : 'gsst',
        'رياضيپايهدوازدهم' : 'ryz3',
        'زبانانگليسي1و3' : 'zbn1_3',
        'شيمي' : 'shmi',
        'شيمي1دهم' : 'shmi1',
        'شيمي2يازدهم' : 'shmi2',
        'شيمي3دوازدهم' : 'shmi3',
        'عربي،زبانقرآن1و3' : 'arbi1_3',
        'فارسي1' : 'frsi1',
        'فارسي3' : 'frsi3',
        'فيزيك' : 'phy',
        'فيزيك1دهم' : 'phy1',
        'فيزيك2يازدهم' : 'phy2',
        'فيزيك3دوازدهم' : 'phy3',
        'معارف' : 'dni',
        'هندسه1دهم' : 'hnds1',
        'هندسه1گواهدهم' : 'hnds1g',
    }
    if lname in names.keys():
        new_lname = names[lname]
    else:
        print('!!!!!!!!!!!!       %s :lname does\'nt exists in names dict        !!!!!!!!!!!!!!!!'%lname)
        new_lname = '0'
    return new_lname

def extract_data(date, base_url, post_url):
    con = sqlite3.connect('dbs/%s.db'%date)
    c = con.cursor()
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'lxml')
    students = soup.find_all('a', class_='swb')
    for count in range(len(students)):
    # for count in range(1, 2):
        this_id = students[count]['id']
        payload = '{"ID":"%s"}'%this_id
        headers = {
                'Host': 'www.kanoon.ir',
                'Proxy-Connection': 'keep-alive',
                'Content-Length': '53',
                'Proxy-Authorization': 'Basic Lmh4QDMxMzE3MzY7aXIuOmJ3K0tHK2oyTzdLVjRPdzNGeUIvOWJsbUhRZXVHcnZjVjhQUUVhWnAxL05NMmlJZHZMaW1Rdz09',
                'Accept': '*/*',
                'Origin': 'http://www.kanoon.ir',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.108 Chrome/78.0.3904.108 Safari/537.36',
                'Content-Type': 'application/json; charset=UTF-8',
                'Referer': 'http://www.kanoon.ir/Public/TopStudents?main=1&group=1&date=%s&year=99'%date,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': '_ga=GA1.2.1633088994.1574772182; _gid=GA1.2.1072446753.1574772182; kfasession=4yqpdxkdf3x23fh3iaapdjfi; error=1',
        }
        r = requests.post(post_url, data=payload, headers=headers)
        rsoup = BeautifulSoup(r.content, 'lxml')
        scores = rsoup.find_all('td')
        # infos = []
        for i in range(12, len(list(scores)) - 2, 3):
            x = []
            x.append(lname_exr(scores[i].text))
            x.append(int(scores[i + 1].text))
            x.append(int(scores[i + 2].text))
            create_table(x[0], con, c)
            ins_to_table(x[0], x[1], x[2], con, c)
            # infos.append(x)
        # with open('output.csv', 'wb') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerows(tmp)

        # f = open('tests/test%s.txt'%str(count + 1), 'w')
        # for i in infos:
            # x = ''
            # for j in i:
                # x += str(j) + '\t'
            # f.write(x + '\n')
        # f.close()
        print(count + 1)
        sys.stdout.flush()
    con.commit()
    print('done')

def a_lesson(date, lname, cad):
    con = sqlite3.connect('dbs/%s.db'%date)
    c = con.cursor()
    datas = c.execute('select * from %s'%lname).fetchall()
    x = []
    y = []
    for data in datas:
        x.append([data[0]])
        y.append(data[1])
    clf = tree.DecisionTreeClassifier()
    clf.fit(x, y)
    res = clf.predict([[cad]])
    return res[0]


if __name__ == "__main__":
    #date = '13980901'
    date = input("eneter date like: 13980901")
    base_url = 'http://www.kanoon.ir/Public/TopStudents?main=1&group=1&date=%s&year=99'%date
    post_url = 'http://www.kanoon.ir/Public/TopStudentsWorkbook'
