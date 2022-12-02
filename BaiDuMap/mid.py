import json

import requests


def baidu(addr):
    url = "http://api.map.baidu.com/geocoding/v3/?"
    para = {
        "address": addr,
        "output": "json",
        "ak": "QI7v1o5Xu8zpZYMezsHufF1Yew3mFBke"
    }
    req = requests.get(url,para)
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
baidu(addr="南环街道")
