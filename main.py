#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
# import sqlite3
from sys import argv

# con = sqlite3.connect('database.db')
# c = con.cursor()
ts = {}

def doing(date, base_url, post_url):
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'lxml')
    students = soup.find_all('a', class_='swb')
    # for i in range(1, len(students)):
    for i in range(1, 2):
        this_id = students[i]['id']
        payload = '{"ID":"JI/zAToNZghpYO6W8fn7hpq7aFOpRAqu2rWf1oAuHSI="}'
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
        f = open('test.txt', 'w')
        for x in scores:
            f.write(x.text + '\n')
        f.close()
        print('done')
        

if __name__ == "__main__":
    date = '13980901'
    base_url = 'http://www.kanoon.ir/Public/TopStudents?main=1&group=1&date=%s&year=99'%date
    post_url = 'http://www.kanoon.ir/Public/TopStudentsWorkbook'
    doing(date, base_url, post_url)