#-*- coding:utf-8 -*-

import base64
import csv
import json
import os.path
import random
import re
import time
import traceback

import pandas as pd

import requests
from fake_useragent import UserAgent
from lxml import etree
import get_css_url

# json_data = json.loads('shop_name.json')
with open("./json/city_list.json", encoding="utf-8") as f:
    json_data = json.load(f)
# print(json_data)

def get_shop(pahe_source):
    if get_css_url.css_url_getter(pahe_source) == 'error':
        return 'error'
    else:
        url = get_css_url.css_url_getter(pahe_source)
        woff_path = get_css_url.shop_name_css_url_getter(url)
        json_path = get_css_url.shop_name_json_getter(woff_path)
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
        return json_data
def get_tag(pahe_source):
    if get_css_url.css_url_getter(pahe_source) == 'error':
        return 'error'
    else:
        url = get_css_url.css_url_getter(pahe_source)
        woff_path = get_css_url.tag_name_css_url_getter(url)
        json_path = get_css_url.shop_name_json_getter(woff_path)
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
        return json_data

def get_csv(hu, idx, flag=False):
    pos = hu.split('/')[-1]
    # 人气
    url = hu + '/ch10/o2p{}'.format(idx)

    headers = {
    'Cookie': '_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368; s_ViewType=10; WEBDFPID=5w0830xz08w35yvu197y7429u76xy6u781596x519x997958zvww6ww3-1981870520158-1666510519831MQUYSAUfd79fef3d01d5e9aadc18ccd4d0c95077639; ctu=3eada7613bfd5549da00debc4ee9ff6190908a18a5ec7383aee478c9ff16b664; fspop=test; cy=1946; cye=bange; dper=de89a983a903d8800d8406b5e096b455290424d5cd5b889f9d0313532957c54f62516b79d73044ac32008348c20522b285b6d3a3a37fcca240e3362fe3d1ded7; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1667300145,1667380665; _lxsdk_s=18437a1da35-371-25-597%7C%7C77; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667380682',
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
    # 'User-Agent': UserAgent().random,
    }

    resp = requests.get(url=url, headers=headers)
    # print(resp.text)
    so = resp.text
    with open('./html/{}_page{}.html'.format(pos, idx), 'w', encoding='utf-8') as fp:
        fp.write(so)
    json_data = get_shop(so)
    tag_data = get_tag(so)
    if json_data != 'error':
        hx = re.findall(r'<svgmtsi class="shopNum">(.*?)</svgmtsi>', so)
        so = str(so)
        print('hx', hx)
        for i in hx:
            uni = i.replace('&#x', 'uni').replace(';','')
            so = so.replace(i, json_data[uni])

    if json_data != 'error':
        hx = re.findall(r'<svgmtsi class="tagName">(.*?)</svgmtsi>', so)
        so = str(so)
        print('hx', hx)
        for i in hx:
            uni = i.replace('&#x', 'uni').replace(';', '')
            if len(i) >= 5:
                so = so.replace(i, tag_data[uni])
        # print(i, uni, json_data[uni])
    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(so)
    # tree = etree.parse('index.html', parser=parser)
    father_tree = tree.xpath('//div[@id="shop-all-list"]/ul/li')
    h4_list = []
    url_list = []
    review_num = []
    mean_price = []
    recommend = []
    all_of_all = []
    for i in father_tree:
        mid = []
        name = i.xpath('./div[@class="txt"]/div[@class="tit"]/a/h4/text()')[0]
        h4_list.append(name)

        shop_url = i.xpath('./div[@class="txt"]/div[@class="tit"]/a/@href')[0]
        url_list.append(shop_url)

        mid.append(name)
        mid.append(shop_url)

        review = i.xpath('./div[@class="txt"]/div[@class="comment"]/a[@class="review-num"]//text()')
        score = i.xpath('./div[@class="txt"]/div[@class="comment"]/div[@class="nebula_star"]/div/span/@class')[0]
        score = int(re.findall(r'\d+', score)[0]) / 10
        mean = i.xpath('./div[@class="txt"]/div[@class="comment"]/a[@class="mean-price"]//text()')
        recommend_mid = i.xpath('./div[@class="txt"]/div[@class="recommend"]/a/text()')
        cata_pos = i.xpath('./div[@class="txt"]/div[@class="tag-addr"]//text()')
        cata_pos = ''.join([i.strip('\n').strip() for i in cata_pos]).split('|')
        cata = cata_pos[0]
        pos = cata_pos[1]
        counp = [p.strip('\n').strip() for p in i.xpath('./div[@class="svr-info"]//text()') if len(p.strip('\n').strip()) > 10]


        recommend_mid = ' '.join(recommend_mid)
        review = ''.join(review)
        mean = ''.join(mean)

        review_clean = review.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
        mean_clean = mean.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
        mid.append(review_clean)
        mid.append(mean_clean)
        mid.append(score)
        mid.append(recommend_mid)
        mid.append(cata)
        mid.append(pos)
        mid.append(counp)
        review_num.append(review_clean)
        mean_price.append(mean_clean)
        recommend.append(recommend_mid)

        all_of_all.append(mid)

    # print(h4_list)
    # print(url_list)
    # print(url)
    # print(review_num)
    # print(mean_price)
    # print(recommend)
    print("all_of_all",all_of_all)
    time.sleep(3)
    # if all_of_all == []:
    #     get_csv(hu, idx)
    # else:
    #     return all_of_all
    return all_of_all

def list_to_csv(csv_path, datas):
    # if not os.path.exists(csv_path):
    #     os.makedirs(csv_path)
    with open(csv_path, 'a+', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in datas:
            writer.writerow(row)

def update_log(url):
    with open('./log/logmore.csv', 'a+', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([url])

def spj(url):
    url_list = pd.read_csv('./log/logmore.csv')
    # print(url_list)
    try:
        if url in url_list['url'].values:
            print(url)
            return True
        return False
    except Exception as e:
        print(e)
        return False
if __name__ == '__main__':
    # if not os.path.exists(csv_path):
    #     os.makedirs(csv_path)
    ks = json_data.keys()
    cnt = 0
    for k in ks:
        try:
            url = json_data[k]
            if spj(url):
                print("{}已经爬取完成".format(k))
                continue
            for i in range(1, 5):
                csv_path = 'csvmore/{}.csv'.format(k)
                list_data = get_csv(url, i)
                list_to_csv(csv_path, list_data)
                print("第{}页已爬取完成".format(i))
            print('{}已经爬取完成'.format(k))
            update_log(url)
            # time.sleep(random.randint(3))
        except Exception as e:
            print(traceback.format_exc())
            continue