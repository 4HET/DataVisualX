import requests

from xpinyin import Pinyin

p = Pinyin()

ip = requests.get(url='http://47.98.116.174:5000/get/?type=http').json()
print(ip['proxy'])

proxy = {
    "http": 'http://172.99.174.91:55485'
}
print(proxy)
res = requests.get('http://myip.ipip.net').text
print(res)
result = p.get_pinyin(res, '')
print(result)