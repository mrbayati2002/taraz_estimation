#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import csv  
from sklearn import tree
import sqlite3
import sys


# ts = {}

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

def doing(date, base_url, post_url):
    con = sqlite3.connect('database.db')
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
                'Referer': 'http://www.kanoon.ir/Public/TopStudents?main=1&group=1&date=13980901&year=99',
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
            c.execute('CREATE TABLE IF NOT EXISTS %s(score BLOB)'%lname_remove_spaces(x[0]))
            c.execute('INSERT INTO %s VALUES("%s")'%(lname_remove_spaces(x[0]), str("[%s, %s]"%(x[1], x[2]))))
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
        

if __name__ == "__main__":
    date = '13980901'
    base_url = 'http://www.kanoon.ir/Public/TopStudents?main=1&group=1&date=%s&year=99'%date
    post_url = 'http://www.kanoon.ir/Public/TopStudentsWorkbook'
    doing(date, base_url, post_url)
