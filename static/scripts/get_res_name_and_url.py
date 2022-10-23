import time

import requests
from lxml import etree

for i in range(2, 3):
    url = 'https://www.dianping.com/chengdu/ch10/g110p{}'.format(i)

    headers = {
    'Cookie': 'fspop=test; cy=153; cye=rizhao; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368; s_ViewType=10; WEBDFPID=5w0830xz08w35yvu197y7429u76xy6u781596x519x997958zvww6ww3-1981870520158-1666510519831MQUYSAUfd79fef3d01d5e9aadc18ccd4d0c95077639; dplet=77569f358366ac46ae8b340c7a828c92; dper=ab7eef6129a412b25b0ac3854ff9e3bd0bf35371e8df4c10679b2f4ae332c4520bd2d188510101887353e78941e52b4a8a57ffa532d2ed4c662b55acd1dda1b993627620ed1e01619351ee224709f7c84571b76e4d9481e5692247f0803176e1; ua=dpuser_3830243167; ctu=3eada7613bfd5549da00debc4ee9ff6190908a18a5ec7383aee478c9ff16b664; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=184046b7e55-cec-64f-c45%7C%7C20; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666510368,1666521465; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1666521465',
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'
    }

    # resp = requests.get(url=url, headers=headers)
    # print(resp.text)
    # with open('./index.html', 'w', encoding='utf-8') as fp:
    #     fp.write(resp.text)
    parser = etree.HTMLParser(encoding="utf-8")
    # tree = etree.HTML(resp.text)
    tree = etree.parse('index.html', parser=parser)
    father_tree = tree.xpath('//div[@id="shop-all-list"]/ul/li/div[@class="txt"]/div[@class="tit"]')
    h4_list = []
    url_list = []
    for i in father_tree:
        h4_list.append(i.xpath('./a/h4/text()')[0])
        url_list.append(i.xpath('./a/@href')[0])
    print(h4_list)
    print(url_list)
    print(url)
    time.sleep(4)