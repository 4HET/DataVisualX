import requests
from lxml import etree
import re

from font_processor import woff_to_json

"""
获得css文件的url
page_source:网页源码数据
-> 整个css文件的地址
"""
def css_url_getter(page_source):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "Host": "s3plus.meituan.net"
    }
    html = etree.HTML(page_source)
    # print(re.sub('\s+', '', page_source).strip())
    """
    根据获取到的页面源码，正则匹配css的url
    """
    css_url = re.findall('<!--图文混排css--><linkrel=.*?href="(.*?)">', re.sub('\s+', '', page_source).strip(), re.M)
    # css_url = 'http:' + html.xpath('/html/head/link[4]/@href')[0]
    # print(css_url)
    return 'http:' + css_url[0]

"""
在整个css文件中获取shop name的url
url:传入的整个css文件的url，需要发送请求，接受数据后进行匹配
woff:css混淆的数据，转化为xml之后进行提取即可得到映射关系
woff地址:./woff/shop_name.woff
"""
def shop_name_css_url_getter(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "Host": "s3plus.meituan.net"
    }

    css_response = requests.get(url=url, headers=headers)

    #注意此处的编码
    css_response.encoding = 'windows-1252'

    #保存css文件
    # with open('./css/all_font.css','w',encoding='UTF-8') as f:
    #     f.write(css_response.text)
        # print(css_response.text)

    font_group = re.search(r'url\("(.*?)"\);} .shopNum', css_response.text)
    font_url = 'http:' + font_group[1].split('"')[-1]
    print("shop name的css url:", font_url)

    woff_path = './woff/shop_name.woff'
    myfile = requests.get(url=font_url, headers=headers)
    open(woff_path, 'wb').write(myfile.content)
    print('字体样式css已获取成功')
    return woff_path

'''
获取shop name的字体对应键值对
调用woff_to_json方法，将编码对应文字以json形式存储
woff_path:woff的地址，xml以及ttf地址是将woff替换
生成完的json路径：./json/shop_name.json
-> json的路径
'''
def shop_name_json_getter(woff_path):
    return woff_to_json(woff_path)


if __name__ == '__main__':
    # with open('./index.html', 'r', encoding='utf-8') as fp:
    #     so = fp.read()
    # url = css_url_getter(so)
    # shop_name_css_url_getter(url)
    woff_path = './woff/shop_name.woff'
    shop_name_json_getter(woff_path)