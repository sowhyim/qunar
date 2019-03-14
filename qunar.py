from bs4 import BeautifulSoup
# import pandas as pd
import requests
import json
import ipcheck
import csv
import random
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
    proxy = ipcheck.GetIP()
    print(proxy)
    res = requests.get(url)
    content = res.text
    msg = BeautifulSoup(content, 'lxml')
    a = msg.find_all('a', {'data-beacon': 'SC_resault'})
    for i in range(0, len(a)):
        print(a[i].attrs['href'])
        GetPJUrl(a[i].attrs['href'], file, proxy)


def GetPJUrl(url, file, proxy):
    a = url.split("-")[1][:2]
    if a != 'oi':
        print("找不到指定的景点信息！")
        return
    print("开始输出评论信息！")
    b = random.randint(0, len(proxy) - 1)
    z = "http://" + proxy[b]
    proxyurl = {'http': z}
    url = 'http://travel.qunar.com/place/api/html/comments/poi/' + \
          url.split("-")[1][2:] + '?poiList=true&sortField=1&rank=0&pageSize=50&page='
    print(url)
    i = 1
    while 1 == 1:  # 为什么要用while true？？？？？？？？？？
        heihei, proxyurl = AutoProxy(1, proxy, proxyurl, url + str(i))
        json_str = heihei.text
        try:
            json_data = json.loads(json_str)['data']
        except:
            print(json_str)
            return
        msg = BeautifulSoup(json_data, 'lxml')
        a = msg.find_all('a', {'data-beacon': 'comment_title'})
        if len(a) == 0:
            return
        for j in range(0, len(a)-1):
            if a[j].attrs['href'].find("javascript")==-1:
                proxyurl = GetData(a[j].attrs['href'], file, proxy, proxyurl)
        i += 1


def GetData(url, file, proxy, proxyurl):
    res, proxyurl = AutoProxy(2, proxy, proxyurl, url)
    msg = BeautifulSoup(res.text, "lxml")
    title = msg.find_all("div", {'class': 'comment_title'})
    a1 = msg.find_all('p')
    a = []
    if len(title) > 0:
        a.append(str(title[0].text))
    for val in a1:
        if val.text != "":
            a.append(str(val.text))
    file.writerow(a[:len(a) - 2])
    return proxyurl


def AutoProxy(flag, proxy, proxyurl, url):
    while True:
        try:
            heihei = requests.get(url, proxies=proxyurl, timeout=5)
            if heihei.url.find("space/captcha") == -1:
                return heihei, proxyurl
        except BaseException:
            print(proxyurl, "已经失效，需要更换proxy")
            b = random.randint(0, len(proxy)-1)
            z = "http://" + proxy[b]
            proxyurl = {'http': z}
            print("更换后的proxy：", proxyurl)


if __name__ == '__main__':
    GetInput()
