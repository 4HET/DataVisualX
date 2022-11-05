import json
import pprint

import requests
from lxml import etree

url = 'https://www.dianping.com/citylist'

def get_html():
    url = 'https://www.dianping.com/citylist'

    headers = {
    'Cookie': 's_ViewType=10; _lxsdk_cuid=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _lxsdk=18431b3e864c8-01933c488e725a-26021b51-384000-18431b3e864c8; _hc.v=652bc9d6-1f70-3c7b-55b7-445886fd6498.1667281185; WEBDFPID=9y5708w5vu5059xv0u815u3519wx6y2881568y530zu979588v74z2vx-1982641217806-1667281217370SOQMUYYfd79fef3d01d5e9aadc18ccd4d0c95071750; ctu=3eada7613bfd5549da00debc4ee9ff61cf0c6fe7b9b663833fc2c67b06018752; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1667281216,1667281849,1667282211,1667291813; cy=344; cye=changsha; ll=7fd06e815b796be3df069dec7836c3df; dper=ab7eef6129a412b25b0ac3854ff9e3bd3dc4a83aed74d476e1c5a39441b4627d3399a311371a1dfce8f5aa65a53a76c065ffd899f11e49fec0e88bb747d27c29; lgtoken=035237a49-b634-46f5-8f76-c6117c9036b8; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667292003; _lxsdk_s=184325615a0-ee6-b1d-55c%7C%7C154',
    'Host': 'www.dianping.com',
    'Referer': 'https://www.dianping.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'
    }

    resp = requests.get(url=url, headers=headers)
    # print(resp.text)
    so = resp.text
    with open('./html/city_lisy.html', 'w', encoding='utf-8') as fp:
        fp.write(so)

    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(so)

    print(so)

def html_to_json():
    with open('./html/city_lisy.html', 'r', encoding='utf-8') as fp:
        so = fp.read()
    fp.close()
    # print(so)
    tree = etree.HTML(so)
    findHeight = tree.xpath('//div[@class="findHeight"]/a')

    url = []
    city_name = []
    for i in findHeight:
        url.append('https:' + i.xpath('./@href')[0])
        city_name.append(i.xpath('./text()')[0])
    print(len(url))
    all_dict = dict(zip(city_name, url))
    # pprint.pprint(dict(all_dict))
    print(all_dict)
    with open('./json/city_list.json', 'w', encoding='utf-8') as fp:
        json.dump(all_dict, fp, ensure_ascii=False)
    print(all_dict)


if __name__ == '__main__':
    html_to_json()