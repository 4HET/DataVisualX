# -*- coding:utf-8 -*-

import json
import pprint
import re

import numpy as np
import requests
from django.shortcuts import render
import pandas as pd
from xpinyin import Pinyin

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
def mainmap(request):
    path = './static/scripts/json/city_list.json'
    with open(path, 'r', encoding='utf-8') as fp:
        city = json.load(fp)
        fp.close()
    city_keys = list(city.keys())
    first_pinyin = {}
    p = Pinyin()
    # 以a-z为键的字典
    for i in range(26):
        first_pinyin[chr(ord('a') + i)] = []
    for i in range(len(city_keys)):
        a = p.get_pinyin(city_keys[i], '')[0]
        first_pinyin[a].append(city_keys[i])
    ks = list(first_pinyin.keys())
    ks.sort()
    # print(first_pinyin)
    ctx = {'city': city_keys,
           'first_pinyin': first_pinyin,
           'ks': ks}
    return render(request, 'main_map.html', ctx)


def now_pos(request):
    return render(request, 'now_pos.html')

def get_cata(source):
    pass

def get_pos(source):
    pass

def index(request):
    k = '日照'
    if request.method == 'GET':
        print('---------------------------------')
        k = request.COOKIES.get('name')
        print('---------------------------------')
    path = './static/scripts/json/city_list.json'
    with open(path, 'r', encoding='utf-8') as fp:
        city = json.load(fp)
        fp.close()
    city_keys = list(city.keys())

    data = []
    money = []
    review = []
    cata = []
    pos = []
    special = {}

    if k in city_keys:
        path = f'./static/scripts/csvmore/{k}.csv'
        top = pd.read_csv(path)
        # 替换nan
        top = top.fillna('0')
        cata = get_cata(top)
        pos = get_pos(top)
        special_list = np.array(top)[:, [0, 5]]
        data = np.array(top)

        for i in range(len(data)):
            data[i][2] = data[i][2].replace('o', '0')
            data[i][3] = data[i][3].replace('o', '0')

        top = np.array(top)[:, [0, 2, 3]]
        for i in range(len(top)):
            top[i][1] = eval(top[i][1].replace('o', '0').replace('条评价', ''))
            top[i][2] = ''.join(re.findall(r'\d+', top[i][2].replace('o', '0')))

        tep = np.delete(np.array(top), np.where(top == ''), axis=0)
        # print(tep)
        tep[:, 1] = tep[:, 1].astype(int)
        tep[:, 2] = tep[:, 2].astype(int)
        # print(tep)
        money = tep[np.argsort(-tep[:, 2])][:, [0]][:min(len(tep), 3), :][:, 0]
        review = tep[np.argsort(-tep[:, 1])][:, [0, 1]][:min(len(tep), 5), :]

        # print(special_list)
        for i in special_list:
            # print(i[1])
            special[i[0][0:3]] = i[1].split(' ')[0: min(len(i[1].split(' ')), 4)]

    # return render(request, 'index.html', {'hotop': data.tolist(), 'len': len(data) * 2})
    ctx = {'hotop': data.tolist(),
           'len': len(data) * 2,
           'review': review.tolist(),
           'money': money.tolist(),
           'special': special,
           'cata': cata,
           'pos': pos}
    return render(request, 'index.html', ctx)


def hot(request):
    path = './static/scripts/json/city_list.json'
    with open(path, 'r', encoding='utf-8') as fp:
        city = json.load(fp)
        fp.close()
    city_keys = list(city.keys())

    k = get_key()
    if k in city_keys:
        path = f'./static/scripts/csv/{k}.csv'
        top = pd.read_csv(path)
        # print(type(top))
        # print(top)
    return render(request, 'hotop.html', {'hotop': np.array(top).tolist()})


def get_key():
    ip = requests.get(url='http://47.98.116.174:5000/get/?type=http').json()
    # print(ip['proxy'])

    res = requests.get('http://myip.ipip.net').text
    return res.split(' ')[-3]


if __name__ == '__main__':
    path = '../static/scripts/json/city_list.json'
    with open(path, 'r', encoding='utf-8') as fp:
        city = json.load(fp)
        fp.close()
    city_keys = list(city.keys())

    k = get_key()
    if k in city_keys:
        path = f'../static/scripts/csv/{k}.csv'
        top = pd.read_csv(path)

