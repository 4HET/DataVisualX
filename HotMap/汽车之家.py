import csv
import pprint

import requests
import json
import re


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response


def get_comments(url):
    res = get_html(url).text
    commtent = re.findall('<div class=".*? kb-item">(.*?)</div>', res, re.S)
    comments = []
    for i in commtent:
        i = re.sub('<.*?>', '', i)
        # 只保留一个空格
        i = re.sub('\s+', ' ', i)
        comments.append(i.strip())
    com = "\n".join(comments)
    return com


def get_list(url):
    res = get_html(url).json()
    pprint.pprint(res)
    comments_data = str(res['result']['structuredlist'])
    brandName = res['result']['brandName']
    seriesname = res['result']['seriesname']
    for i in res['result']['list']:
        buyprice = i['buyprice']
        buyplace = i['buyplace']
        specname = i['specname']
        distance = i['distance']
        boughtDate = i['boughtDate']
        showId = i['showId']
        comments_url = "https://k.autohome.com.cn/detail/view_{}.html".format(showId)
        comment = get_comments(comments_url)
        with open(brandName + ".json", 'a', encoding='utf-8-sig') as f:
            f.write(comments_data)
            f.close()
        with open("汽车之家.csv", "a", encoding="utf-8-sig", newline="") as f:
            f = csv.writer(f)
            f.writerow([brandName, seriesname, specname, buyprice, buyplace, distance, boughtDate, comment])


def get_info():
    url = "https://car.autohome.com.cn/searchcar/query?pageindex=1&pagesize=30&orderid=1&cityid=110100"
    res = get_html(url).json()
    for i in res['result']['seriesGroupList']:
        seriesId = i['seriesId']
        for j in i['specitems']:
            yearid = j['id']
            url = "https://koubeiipv6.app.autohome.com.cn/pc/series/list?pm=3&seriesId={}&pageIndex={}&pageSize=20&yearid=0&ge=0&seriesSummaryKey=0&order=0".format(seriesId, pageIndex)
            get_list(url)

