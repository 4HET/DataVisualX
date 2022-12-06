import json

import requests
def get_province():
    key = 'PFQu9WDiiiwqNhWxGMobLFqZDxTBPy1E'
    # r = requests.get(url=f'https://api.map.baidu.com/location/ip?ak=您的AK&ip=您的IP&coor=bd09ll //GET请求',
    #                  params={'location': '32.03805,120.275443', 'ak': key, 'output': 'json'})
    #
    # result = r.json()
    # print(result)
    # province = result['result']['addressComponent']['province']
    # city = result['result']['addressComponent']['city']
    # print(province, city)


def baidu(addr):
    url = "http://api.map.baidu.com/geocoding/v3/?"
    para = {
        "address": addr,
        "output": "json",
        "ak": "QI7v1o5Xu8zpZYMezsHufF1Yew3mFBke"
    }
    req = requests.get(url, para)
    print(req.text)
    req = req.json()
    # print('-' * 30)
    # json转化为字符串
    # print(json.dumps(req, indent=4, ensure_ascii=False))
    # print(json.dumps(req, ensure_ascii=False))
    # 查看字典是否包含某个键
    if 'result' not in req:
        return 0, 0
    m = req["result"]["location"]
    # print(m)
    g = f"{m['lng']},{m['lat']}"
    # print(g)
    return m['lat'], m['lng']

if __name__ == '__main__':
    print(baidu('日照'))
