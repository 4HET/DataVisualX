import requests
from lxml import etree
import re

from static.scripts.font_processor import woff_to_json


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

    myfile = requests.get(url=font_url, headers=headers)
    open('./woff/shop_name.woff', 'wb').write(myfile.content)
    print('字体样式css已获取成功')

'''
获取shop name的字体对应键值对
'''
def shop_name_json_getter():
    woff_to_json('./woff/shop_name.woff')


if __name__ == '__main__':
    # with open('./index.html', 'r', encoding='utf-8') as fp:
    #     so = fp.read()
    # url = css_url_getter(so)
    # shop_name_css_url_getter(url)
    shop_name_json_getter()