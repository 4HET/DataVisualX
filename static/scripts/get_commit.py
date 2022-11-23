import requests
import re    # re库是对字符串进行解析，而lxml文件可以对xml文件进行解析
from lxml import etree
from fake_useragent import UserAgent
import time    #暂停程序，避免封号
import random    #生成随机时间值

def get_url_list():
    url_list = []
    for i in list(range(1, 2)):  # 我所抓的评论一共72页，尚未完善自动化获取评论页数的代码
        url_list.append('http://www.dianping.com/shop/l2Tn63E9MaXvTEel/review_all/p' + str(i))
    return url_list

def get_css_content(html, headers):
    print('------begin to get css content------')
    # print(html)
    css_l = re.search(r'<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.net.*?.css)">', html)
    print(css_l)
    css_link = 'http:' + css_l.group(1)
    html_css = requests.get(css_link, headers).text
    return html_css

def get_font_dic(css_content):
    print('------begin to get font dictionary------')
    # 获取svg链接和svg页面的html源码
    svg_l = re.search(r'svgmtsi.*?(//s3plus.meituan.net.*?svg)\);', css_content)
    svg_link = 'http:' + svg_l.group(1)
    svg_html = requests.get(svg_link).text
    # 解析出字典
    y_list = re.findall('d="M0 (.*?) H600"', svg_html)  # y_list的元素为str
    font_dic = {}
    j = 0    # j为第j行
    font_size = int(re.findall(r'font-size:(.*?)px;fill:#333;}', svg_html)[0])
    for y in y_list:
        font_l = re.findall(r'<textPath xlink:href="#' + str(j + 1) + '" textLength=".*?">(.*?)</textPath>', svg_html)
        font_list = re.findall(r'.{1}', font_l[0])
        for x in range(len(font_list)):    # x为每一行第x个字
            font_dic[str(x * font_size) + ',' + y] = font_list[x]
        j += 1
    return font_dic, y_list

def get_html_full_review(html, css_content, font_dic, y_list):
    font_key_list = re.findall(r'<svgmtsi class="(.*?)"></svgmtsi>', html)
    # print(len(font_key))
    for font_key in font_key_list:
        pos_key = re.findall(r'.' + font_key + '{background:-(.*?).0px -(.*?).0px;}', css_content)
        pos_x = pos_key[0][0]
        pos_y_original = pos_key[0][1]
        for y in y_list:
            if int(pos_y_original) < int(y):
                pos_y = y
                break
        html = html.replace('<svgmtsi class="' + font_key + '"></svgmtsi>', font_dic[pos_x + ',' + pos_y])
    print(html)
    return html

def reviews_output(html_full_review, flag):
    print('------开始提取评论并写入文件------')
    html = etree.HTML(html_full_review)
    reviews_items = html.xpath("//div[@class='reviews-items']/ul/li")
    for i in reviews_items:
        r = []    #初始化数组
        r = i.xpath("./div/div[@class='review-words Hide']/text()")
        if r:
            pass
        else:
            r = i.xpath("./div/div[@class='review-words']/text()")    #评论较短不需要展开的时候
        flag += 1
        #print(r)
        #print('第' + str(flag) + '条评论：\n' + r[0].strip())
        with open('reviews.txt', 'a+', encoding='UTF-8') as f:
            f.write('第' + str(flag) + '条评论：\n' + r[0].strip() + '\n\n')
            print('第' + str(flag) + '条评论：\n' + r[0].strip() + '\n')
        f.close()
    print('------写入完成，延迟10-25秒------')
    time.sleep(10 + 15 * random.random())

if __name__ == '__main__':
    url_list = get_url_list()
    flag = 0    # 统计评论数量
    # url = 'http://www.dianping.com/shop/18335920/review_all/p1'
    headers = {
        'Cookie': 's_ViewType=10; _lxsdk_cuid=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _lxsdk=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _hc.v=652bc9d6-1f70-3c7b-55b7-445886fd6498.1667281185; WEBDFPID=9y5708w5vu5059xv0u815u3519wx6y2881568y530zu979588v74z2vx-1982641217806-1667281217370SOQMUYYfd79fef3d01d5e9aadc18ccd4d0c95071750; ctu=3eada7613bfd5549da00debc4ee9ff61cf0c6fe7b9b663833fc2c67b06018752; fspop=test; cy=57; cye=alashan; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1668918849,1668945415,1669007193,1669169028; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1669169649; _lxsdk_s=184a23a173b-9de-d83-5e5%7C%7C202',
        'host': 'www.dianping.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': UserAgent().random
    }
    res = requests.get(url_list[0], headers=headers)
    # 获取css文件内容
    css_content = get_css_content(res.text, headers)
    # 获取字体字典
    font_dic, y_list = get_font_dic(css_content)
    #解析第一个网页
    print('------开始解析第1个网页------')
    html_full_review = get_html_full_review(res.text, css_content, font_dic, y_list)
    reviews_output(html_full_review, flag)
    flag += 15
    #解析从第二个网页开始的所有网页
    for n in list(range(len(url_list)-1)):
        print('------开始解析第' + str(n + 2) + '个网页------')
        res = requests.get(url_list[n+1], headers=headers)
        if res:
            html_full_review = get_html_full_review(res.text, css_content, font_dic, y_list)
            reviews_output(html_full_review, flag)
            n += 1
            flag += 15
        else:
            print('无法请求网页')