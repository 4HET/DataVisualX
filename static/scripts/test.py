import requests

ip = requests.get(url='http://47.98.116.174:5000/get/?type=http').json()
# print(ip['proxy'])

res = requests.get('http://myip.ipip.net').text
print(res.split(' ')[-3])