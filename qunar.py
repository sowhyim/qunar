from bs4 import BeautifulSoup
# import pandas as pd
import requests
import json

url = "http://travel.qunar.com/search/all/"


def main():
    GetInput()


def GetInput():
    while True:
        x = input("请输入想要查询的字段名：")
        for jd in x.split():
            GetUrl(url + jd)


def GetUrl(url):
    res = requests.get(url)
    content = res.text
    msg = BeautifulSoup(content, 'lxml')
    a = msg.find_all('a', {'data-beacon': 'SC_resault'})
    for i in range(0, len(a)):
        GetPJUrl(a[i].attrs['href'])


def GetPJUrl(url):
    url = 'http://travel.qunar.com/place/api/html/comments/poi/' + \
          url.split("-")[1][2:] + '?poiList=true&sortField=1&rank=0&pageSize=50&page='
    print(url)
    i = 1
    while 1 == 1:
        json_str = requests.get(url + str(i)).text
        json_data = json.loads(json_str)['data']
        msg = BeautifulSoup(json_data, 'lxml')
        a = msg.find_all('a', {'data-beacon': 'comment_title'})
        print(len(a))
        for j in range(0, len(a)):
            print(a[j].attrs['href'])
        i += 1


if __name__ == '__main__':
    main()
