from bs4 import BeautifulSoup
import re
import requests
import execjs


findSeq = re.compile(r'<td align="center" height="32px">(.*)</td>')
findCate = re.compile(r'<td align="center" style="font-size: 9pt"><a href="\?infotype=.*">(.*)</a></td>')
findApart = re.compile(r'<td align="center" style="font-size: 9pt"><a href=".*\sonclick.*>(.*)</a></td>')
findDate = re.compile(r'<td align="center" style="font-size: 9pt">(\d*-\d*-\d*)</td>')
findId = re.compile(r'<a class="fontcolor3" href="view.asp\?id=(\d*)')


def main():
    url = "https://www1.szu.edu.cn/board/infolist.asp"
    return dataFilter(url)


def dataFilter(url):
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    datalist = []
    for itemSeq in soup.find_all(attrs={"align": "center", "height": "32px"}):
        # print(itemSeq.parent)
        item = itemSeq.parent
        itemStr = str(item)

        seq = re.findall(findSeq, itemStr)[0]
        cate = re.findall(findCate, itemStr)[0]
        apart = re.findall(findApart, itemStr)[0]
        title = item.find(attrs={"class": "fontcolor3"}).string
        date = re.findall(findDate, itemStr)[0]
        tapCount = item.find(attrs={"title": "累计点击数"}).string
        id = re.findall(findId, itemStr)[0]


        datalist.append([seq, cate, apart, title, date, tapCount, id])

    return datalist


def askURL(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
    session1 = requests.Session()
    session1.get("https://www1.szu.edu.cn/", headers=headers)

    # 获取加密的password 开始
    crypt = session1.get("https://authserver.szu.edu.cn/authserver/custom/js/encrypt.js", headers=headers).text
    encrypt = execjs.compile(crypt)  # 获取js加密代码
    res = session1.get("https://authserver.szu.edu.cn/authserver/login", headers=headers)  # 请求登录界面

    bs = BeautifulSoup(res.content, "html.parser")
    bs = bs.find_all('input', {'type': "hidden"})  # 寻找登录界面中需要的数据
    dist = {}
    for i in bs:
        try:
            dist[re.search('(?<=name=").*?(?=")', str(i)).group()] = re.search('(?<=value=").*?(?=")', str(i)).group()
        except:
            dist[re.search('(?<=id=").*?(?=")', str(i)).group()] = re.search('(?<=value=").*?(?=")', str(i)).group()

    username = '334837'
    password = '2945818Sz'
    enPassword = encrypt.call("encryptAES", password, dist["pwdDefaultEncryptSalt"])  # 利用js代码加密
    print(enPassword)
    # 获取加密过的password 结束

    # 登录时需要POST的数据
    data = {
        "username": username,
        "password": enPassword,
        "lt": dist["lt"],
        "dllt": dist["dllt"],
        "execution": dist["execution"],
        "_eventId": dist["_eventId"],
        "rmShown": dist["rmShown"]
    }

    login_url = "https://authserver.szu.edu.cn/authserver/login?service=http%3A%2F%2Fwww1%2Eszu%2Eedu%2Ecn%2Fmanage%2Fcaslogin%2Easp%3Frurl%3D%2F"
    session1.post(login_url, headers=headers, data=data)

    askRes = session1.get(url, headers=headers)
    askRes = session1.get(url, headers=headers)
    askRes.encoding = 'gbk'
    return askRes.text
