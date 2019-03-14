import requests


def IPCheck():
    file = open("ip.txt", "r", encoding="utf-8")
    ipfile = open("proxy.txt", "w", encoding="utf-8")
    lines = file.readlines()
    for line in lines:
        if line != None:
            ipurl = line.split("@")[0]
            try:
                res = requests.get('http://www.baidu.com/', proxies={"http": "http://" + ipurl}, timeout=2)
                print(ipurl)
                ipfile.write(ipurl + "\n")
            except Exception:
                print(ipurl, "失败")
    ipfile.close()


def ProxyCheck(url):
    try:
        res = requests.get('http://www.baidu.com/', proxies={url}, timeout=2)
        print(res.links)
    except Exception:
        print(url, "失败")


def ReadIP():
    file = open("proxy.txt", "r", encoding="utf-8")
    lines = file.readlines()
    for line in lines:
        ProxyCheck(line.split("\n")[0])


def GetIP():
    file = open("proxy.txt", "r", encoding="utf-8")
    lines = file.readlines()
    i=0
    while i < len(lines):
        lines[i]=lines[i][:len(lines[i])-1]
        i+=1
    return lines


if __name__ == '__main__':
    IPCheck()
