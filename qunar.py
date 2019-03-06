from bs4 import BeautifulSoup
# import pandas as pd
import requests
import json
import ipcheck
import csv
import codecs

url = "http://travel.qunar.com/search/all/"


def GetInput():
    while 1 == 1:
        x = input("请输入想要查询的字段名：")
        print(x)
        for jd in x.split():
            csvfile = open(jd + "数据.csv", 'a', newline='', encoding='utf-8-sig')
            csvfile = csv.writer(csvfile)
            GetUrl(url + jd, csvfile)


def GetUrl(url, file):
    print(url)
    res = requests.get(url)
    content = res.text
    msg = BeautifulSoup(content, 'lxml')
    a = msg.find_all('a', {'data-beacon': 'SC_resault'})
    for i in range(0, len(a)):
        print(a[i].attrs['href'])
        GetPJUrl(a[i].attrs['href'], file)


def GetPJUrl(url, file):
    a = url.split("-")[1][:2]
    if a != 'oi':
        print("找不到指定的景点信息！")
        return

    url = 'http://travel.qunar.com/place/api/html/comments/poi/' + \
          url.split("-")[1][2:] + '?poiList=true&sortField=1&rank=0&pageSize=50&page='
    print(url)
    i = 1
    while 1 == 1:
        json_str = requests.get(url + str(i)).text
        print(i)
        if json_str == None:
            return
        json_data = json.loads(json_str)['data']
        msg = BeautifulSoup(json_data, 'lxml')
        a = msg.find_all('a', {'data-beacon': 'comment_title'})
        print(len(a))
        for j in range(0, len(a)):
            GetData(a[j].attrs['href'], file)
        i += 1


def GetData(url, file):
    res = requests.get(url)
    msg = BeautifulSoup(res.text, "lxml")
    title = msg.find_all("div", {'class': 'comment_title'})
    a1 = msg.find_all('p')
    a = []
    if title != None:
        a.append(str(title[0].text))
    for val in a1:
        if val.text != "":
            a.append(str(val.text))
    file.writerow(a)


if __name__ == '__main__':
    GetInput()
