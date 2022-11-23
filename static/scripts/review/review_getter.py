import json
import random
import time

import requests
import pandas as pd
from fake_useragent import UserAgent
import re

from lxml import etree

# 获取html源码
def get_html(url):
    headers = {
        'User-Agent': UserAgent().random,
        'Host': 'www.dianping.com',
        'Cookie': 's_ViewType=10; _lxsdk_cuid=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _lxsdk=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _hc.v=652bc9d6-1f70-3c7b-55b7-445886fd6498.1667281185; WEBDFPID=9y5708w5vu5059xv0u815u3519wx6y2881568y530zu979588v74z2vx-1982641217806-1667281217370SOQMUYYfd79fef3d01d5e9aadc18ccd4d0c95071750; ctu=3eada7613bfd5549da00debc4ee9ff61cf0c6fe7b9b663833fc2c67b06018752; fspop=test; cy=57; cye=alashan; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668918849,1668945415,1669007193,1669169028; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1669170595; _lxsdk_s=184a23a173b-9de-d83-5e5%7C%7C518',
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    return resp.text

def get_html_full_review(url):
    fp = open('hou.html', 'a', encoding='utf-8')
    f = open('qian.html', 'a', encoding='utf-8')
    # 获取源码
    html_source = get_html(url)
    # 正则表达式img标签替换为空
    html_source = re.sub(r'<img.*?>', '', html_source)
    print(html_source, file=f)
    # print(html_source)
    # 解析出css的url
    css_link = css_url(html_source)
    # 解析出css的源码
    css_source = css(css_link)
    # 解析出css源码中的对应关系
    # k_v = kv(css_source)
    # 解析出css源码中的字体url
    font_urls = get_font_url(css_source)
    # print(k_v)
    print(font_urls)

    for font_url in font_urls:
        print(font_url)
        # 获取字体文件xml源码
        xml_info = font(font_url)
        # 获取字体文件的标签和对应数字
        font_dic, y_list = get_font_dic(xml_info)
        if y_list == []:
            continue
        print(f"font_dic:\t{font_dic}\n{y_list}")
        # 获取svg的class标签
        font_key_list = re.findall(r'<svgmtsi class="(.*?)"></svgmtsi>', html_source)
        print(font_key_list)
        # '看大众点评来<svgmtsi class="nznlgx"></svgmtsi>，整体来说<svgmtsi class="nznigy"></svgmtsi><svgmtsi class="nzn3yz"></svgmtsi><img class="emoji-img" src="https://img.meituan.net/ugcpic/865d953ec5baf955ee0061270ed5b06d914.png" alt=""/><img class="emoji-img" src="https://img.meituan.net/ugcpic/865d953ec5baf955ee0061270ed5b06d914.png" alt=""/>，环境<svgmtsi class="nzn21w"></svgmtsi><svgmtsi class="nzn3os"></svgmtsi><svgmtsi class="nzn666"></svgmtsi>，<svgmtsi class="nznhra"></svgmtsi>合<svgmtsi class="nznpnn"></svgmtsi><svgmtsi class="nznia9"></svgmtsi><svgmtsi class="nznkcd"></svgmtsi>卡，吃完<svgmtsi class="nzn9xs"></svgmtsi>可以<svgmtsi class="nzn0kx"></svgmtsi><svgmtsi class="nznitk"></svgmtsi><svgmtsi class="nzncai"></svgmtsi>营<svgmtsi class="nzncsh"></svgmtsi><svgmtsi class="nzn2hd"></svgmtsi><svgmtsi class="nzncsh"></svgmtsi>，溜溜食儿，菜<svgmtsi class="nzn49j"></svgmtsi><svgmtsi class="nznsa2"></svgmtsi>体<svgmtsi class="nzne8o"></svgmtsi>是<svgmtsi class="nznigy"></svgmtsi><svgmtsi class="nzn3yz"></svgmtsi><svgmtsi class="nznlgx"></svgmtsi>，可能我们是南方人，吃<svgmtsi class="nznlgx"></svgmtsi><svgmtsi class="nznq0y"></svgmtsi><svgmtsi class="nznbsy"></svgmtsi>淡，有些<svgmtsi class="nznigy"></svgmtsi>是<svgmtsi class="nzn7ge"></svgmtsi><svgmtsi class="nznlfl"></svgmtsi>能<svgmtsi class="nznhra"></svgmtsi>应，<svgmtsi class="nzne4a"></svgmtsi>是<svgmtsi class="nznams"></svgmtsi><svgmtsi class="nzn8ld"></svgmtsi><svgmtsi class="nznkh4"></svgmtsi><svgmtsi class="nzn7y9"></svgmtsi><svgmtsi class="nzne8o"></svgmtsi><svgmtsi class="nznbsy"></svgmtsi><svgmtsi class="nzn666"></svgmtsi><img class="emoji-img" src="https://img.meituan.net/ugcpic/77767c628a19e6d0a84e9558551634ca2205.png" alt=""/><img class="emoji-img" src="https://img.meituan.net/ugcpic/77767c628a19e6d0a84e9558551634ca2205.png" alt=""/><img class="emoji-img" src="https://img.meituan.net/ugcpic/77767c628a19e6d0a84e9558551634ca2205.png" alt=""/>'
        # print(len(font_key))
        for font_key in font_key_list:
            pos_key = re.findall(r'.' + font_key + '{background:-(.*?).0px -(.*?).0px;}', css_source)
            pos_x = pos_key[0][0]
            pos_y_original = pos_key[0][1]
            for y in y_list:
                if int(pos_y_original) < int(y):
                    pos_y = y
                    break
            html_source = html_source.replace('<svgmtsi class="' + font_key + '"></svgmtsi>', font_dic[pos_x + ',' + pos_y])
    print(html_source, file=fp)
    return html_source

def reviews_output(html_full_review, flag):
    print('------开始提取评论并写入文件------')
    html = etree.HTML(html_full_review)
    reviews_items = html.xpath("//div[@class='reviews-items']/ul/li")
    for i in reviews_items:
        r = []    #初始化数组
        r = i.xpath("./div/div[@class='review-words Hide']//text()")
        if r:
            pass
        else:
            r = i.xpath("./div/div[@class='review-words']//text()")    #评论较短不需要展开的时候
        flag += 1
        #print(r)
        #print('第' + str(flag) + '条评论：\n' + r[0].strip())
        with open('reviews.txt', 'a+', encoding='UTF-8') as f:
            print(r[0].strip() + '\n')
            f.write('第' + str(flag) + '条评论：\n' + r[0].strip() + '\n\n')
        f.close()
    print('------写入完成，延迟10-25秒------')
    time.sleep(10 + 15 * random.random())

# 获取css的url
def css_url(resp):
    pattern = re.compile(r'<link rel="stylesheet" type="text/css" href="(.*?)">')
    result = pattern.findall(resp)
    return 'http:' + result[1]

# 获取css的信息
def css(url):
    headers = {
        'User-Agent': UserAgent().random,
    }
    css_info = requests.get(url, headers=headers).text
    return css_info

# 获取svg标签属性的对应关系
def kv(resp):
    pattern = re.compile(r'\.(?P<tag>.*?)\{background:-(?P<x>.*?)px -(?P<y>.*?)px')
    result = pattern.finditer(resp)
    tag = {}
    for groups in result:
        if len(groups.group('tag')) >= 20:
            tag[groups.group('tag').split('.')[-1]] = [int(eval(groups.group('x'))), int(eval(groups.group('y')))]
        else:
            tag[groups.group('tag')] = [int(eval(groups.group('x'))), int(eval(groups.group('y')))]
    return tag

# 获取svg标签的信息
def writing(resp):
    pattern = re.compile(r'\[class\^="(?P<tag>.*?)"]\{width: (?P<width>.*?)px;height: (?P<height>.*?)px;margin-top: -(?P<top>.*?)px;background-image: url\((?P<url>.*?)\);backgro')
    result = pattern.finditer(resp)
    tag = {}
    for groups in result:
        tag[groups.group('tag')] = [int(eval(groups.group('width'))), int(eval(groups.group('top'))), 'http:' + groups.group('url')]
    return tag

# 获取html中加密后的文件
def secret(resp):
    tree = etree.HTML(resp)
    review_sec = tree.xpath('//div[@class="reviews-items"]/ul')
    for i in review_sec:
        # 替换空白字符
        review_i = i.xpath('./li/div[@class="main-review"]/div[@class="dper-info"]/a/text()')
        print(review_i)

# 获取字体的url
def get_font_url(resp):
    print('------begin to get font url------')
    font_url = re.findall(r'background-image: url\((.*?)\);', resp)
    return font_url

# 获取字体文件xml的源码
def font(url):
    print('------begin to get font------')
    # url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/c52c5f54f0f55645b6995aa1db09182b.svg'
    url = 'http:' + url
    print(url)
    headers = {
        'User-Agent': UserAgent().random,
    }
    xml_info = requests.get(url, headers=headers).text
    return xml_info

# 获取字体文件中的标签和对应的数字
def get_font_dic(xml_info):
    print('------begin to get font dictionary------')
    # 解析出字典
    y_list = re.findall('d="M0 (.*?) H600"', xml_info)  # y_list的元素为str
    font_dic = {}
    j = 0    # j为第j行
    font_size = int(re.findall(r'font-size:(.*?)px;fill:#.*?;}', xml_info)[0])
    for y in y_list:
        font_l = re.findall(r'<textPath xlink:href="#' + str(j + 1) + '" textLength=".*?">(.*?)</textPath>', xml_info)
        font_list = re.findall(r'.{1}', font_l[0])
        for x in range(len(font_list)):    # x为每一行第x个字
            font_dic[str(x * font_size) + ',' + y] = font_list[x]
        j += 1
    return font_dic, y_list

def redu():
    with open('../json/city_list.json', 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    city_list = data.keys()

    path = r'../log/log.csv'
    city_log = pd.read_csv(path).iloc[:, 0].values
    log = pd.read_csv(path).iloc[:, 0].values
    log = pd.DataFrame(log, columns=['shop_url'])

    for city in city_list:
        pds = pd.read_csv(f'../csv/{city}.csv').iloc[:, 1].values
        # numpy转为DataFrame
        df = pd.DataFrame(pds)
        # 去重
        df.drop_duplicates(inplace=True)
        # 删除两个DataFrame中相同的行
        pds = df[~df.isin(log)]
        print(pds)
        if city in city_log:
            print("已经爬取过")
        for urls in pds.iloc[:, 0].values:
            url = urls + '/review_all'
            # print(self.shop_id)
            headers = {
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'User-Agent': UserAgent().random,
                'Host': 'www.dianping.com',
                'Cookie': '_lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=9fec2d1c-9253-9f08-843d-4d8d0bd47aaa.1668095623; s_ViewType=10; fspop=test; __utma=205923334.1124010926.1668848108.1668848108.1668848108.1; __utmz=205923334.1668848108.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WEBDFPID=8x7y7yz136w6589yz97u5zwy8z6x294v8151u8y12zx979588w9915xu-1984208257365-1668848257101QMIMWGKfd79fef3d01d5e9aadc18ccd4d0c95071406; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; cy=4; cye=guangzhou; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668918822,1668945215,1669003562,1669080037; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1669082774; _lxsdk_s=1849cec2e9e-6f7-26d-0f5%7C%7C414'
            }
            print(f"step 1:\nurl:\t{url}")
            resp = requests.get(url, headers=headers)

if __name__ == '__main__':
    url = 'http://www.dianping.com/shop/l2Tn63E9MaXvTEel/review_all/p1'
    html = get_html_full_review(url)
    reviews = reviews_output(html, 1)
    # # 获取源码
    # html_source = get_html(url)
    # # 解析出css的url
    # css_link = css_url(html_source)
    # # 解析出css的源码
    # css_source = css(css_link)
    # # 解析出css源码中的对应关系
    # k_v = kv(css_source)
    # # 解析出css源码中的字体url
    # font_url = get_font_url(css_source)[0]
    # print(k_v)
    # print(font_url)
    #
    # # 获取字体文件xml源码
    # xml_info = font(font_url)
    # # 获取字体文件的标签和对应数字
    # font_dic, y_list = get_font_dic(xml_info)
    # print(font_dic)