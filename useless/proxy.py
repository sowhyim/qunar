import urllib.request
import requests
from bs4 import BeautifulSoup

import json
import ipcheck
import re
import socket
import csv



def IPspider(numpage):
    url = 'http://ip.zdaye.com/dayProxy/2019/3/1.html'
    user_agent = 'IP'
    headers = {'User-agent': user_agent}
    for num in range(1, numpage + 1):
        ipurl = url + str(num)
        print('Now downloading the ' + str(num * 100) + ' ips')
        print(ipurl)
        request = urllib.request.Request(ipurl, headers=headers)
        flag = True
        while flag:
            try:
                content = urllib.request.urlopen(request).read()
                flag = False
            except Exception:
                continue

        bs = BeautifulSoup(content, 'html.parser')
        res = bs.find_all('tr')
        file = open("ip.txt", "w+", encoding='utf-8')
        for item in res:
            try:
                tds = item.find_all('td')
                b = IPCheck(tds[1].text + ":" + tds[2].text)
                if b != None:
                    file.write(str(b) + "\n")
            except IndexError:
                pass

        file.close()


def IPCheck(url):
    # socket.setdefaulttimeout(2)
    # proxy_handler = urllib.request.ProxyHandler({"http": url})
    # opener = urllib.request.build_opener(proxy_handler)
    # urllib.request.install_opener(opener)
    try:
        # html = urllib.request.urlopen('http://www.baidu.com')
        res = requests.get('http://www.baidu.com/', proxies={"http": "http://" + url}, timeout=2)
        print(url)
        return url
    except Exception:
        pass



def DoTimes():
    while True:
        j = 1
        res = requests.get(
            "http://travel.qunar.com/place/api/html/comments/poi/714422?poiList=true&sortField=1&rank=0&pageSize=50&page=" + str(
                1))
        print(res.links, res.url)
        try:
            json_data = json.loads(res.text)['data']
        except:
            return
        msg = BeautifulSoup(json_data, 'lxml')
        a = msg.find_all('a', {'data-beacon': 'comment_title'})
        print(len(a))
        for i in range(0, len(a)):
            print(a[i].attrs['href'])
        j += 1


def Strs():
    a = "asdasdasd"
    b = "xasd"
    print(a.find(b))


def Ceshi():
    url = "http://travel.qunar.com/p-pl5730006"
    res = requests.get(url)
    msg = BeautifulSoup(res.text,'lxml')
    title = msg.find_all("div",{'class':'e_comment_content_box'})
    for t in title:
        print(t.text)
    time = msg.find_all('li')
    for ti in time:
        print(ti.text)

def Ceshi2():
    res = requests.get('http://travel.qunar.com/p-pl5128801')
    msg = BeautifulSoup(res.text, 'lxml')
    emailid_regexp = re.compile("cur_star star_+\w")

    a1 = msg.find('div', {'class': 'e_comment_content_box'})
    print(a1.text.strip())
    username = msg.find('a', {'class': 'usr_name'})
    print(username.text)
    title = msg.find("div", {'class': 'comment_title'})
    print(title.text.strip())
    a = msg.find_all(text=re.compile('2016-+\d+-+\d'))
    if a == []:
        print("没有数据")
        return
    print(len(a))

    print(a[0].strip())

if __name__ == '__main__':
    Ceshi()
