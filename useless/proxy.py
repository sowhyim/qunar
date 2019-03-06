import urllib.request
import requests
from bs4 import BeautifulSoup
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


if __name__ == '__main__':
    IPspider(3000)
