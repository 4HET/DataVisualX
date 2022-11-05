import json
import pprint

import requests
import execjs
from fake_useragent import UserAgent

def get_commit(shop_id):
    with open('./rohr.min.js', 'r', encoding='utf-8') as fp:
        js = fp.read()

    JS = execjs.compile(js)
    sign = JS.call("hhh_token",'https://www.dianping.com?shopId={}'.format(shop_id))
    print(sign)

    url = 'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId={}&cityId=8&shopType=10&tcv=4e7hqrxmfg&_token={}&uuid=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368&platform=1&partner=150&optimusCode=10&originUrl=https://www.dianping.com/shop/l2g0kxUJRpV1bdZr'.format(shop_id, sign)

    headers = {
        'Cookie': 'fspop=test; cy=153; cye=rizhao; _lxsdk_cuid=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _lxsdk=18403c22a69c8-0cbd5899ee277f-7b555472-384000-18403c22a69c8; _hc.v=7db62757-4617-03c5-8227-a3b30a9803c6.1666510368; s_ViewType=10; WEBDFPID=5w0830xz08w35yvu197y7429u76xy6u781596x519x997958zvww6ww3-1981870520158-1666510519831MQUYSAUfd79fef3d01d5e9aadc18ccd4d0c95077639; dper=ab7eef6129a412b25b0ac3854ff9e3bd0bf35371e8df4c10679b2f4ae332c4520bd2d188510101887353e78941e52b4a8a57ffa532d2ed4c662b55acd1dda1b993627620ed1e01619351ee224709f7c84571b76e4d9481e5692247f0803176e1; ua=dpuser_3830243167; ctu=3eada7613bfd5549da00debc4ee9ff6190908a18a5ec7383aee478c9ff16b664; _lx_utm=utm_source=bing&utm_medium=organic; ll=7fd06e815b796be3df069dec7836c3df; dplet=a1ded827ad67a2f1eaf855c2d2249de0; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666950926,1666995148,1667001764,1667098148; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667099170; _lxsdk_s=18426cafb66-ae0-e72-2ab||121',
        'User-Agent': UserAgent().random,
        'Host': 'www.dianping.com',
        'Referer': 'https://www.dianping.com/shop/{}'.format(shop_id),
    }

    resp = requests.get(url=url, headers=headers).json()

    with open('./resp.json', 'w', encoding='utf-8') as fp:
        json.dump(resp, fp, ensure_ascii=False)

    pprint.pprint(json.dumps(resp, ensure_ascii=False))

    # with open('./resp.json', 'r', encoding='utf-8') as fp:
    #     json_data = json.load(fp)
    #
    # for i in json_data['summarys']:
    #     print(i['summaryString'])
    # print(json_data['summarys'])

if __name__ == '__main__':
    get_commit('H9JCXW6aTaQrRWcZ')