#-*- coding:utf-8 -*-

import json
import re

import numpy as np
import requests
from django.shortcuts import render
import pandas as pd

# Create your views here.
def mainmap(request):
    return render(request, 'main_map.html')

def now_pos(request):
    return render(request, 'now_pos.html')
def index(request):
    path = './static/scripts/json/city_list.json'
    with open(path, 'r', encoding='utf-8') as fp:
        city = json.load(fp)
        fp.close()
    city_keys = list(city.keys())

    k = get_key()
    data = []
    money = []
    review = []
    if k in city_keys:
        path = f'./static/scripts/csv/{k}.csv'
        top = pd.read_csv(path)
        special_list = np.array(top)[:, [0, 4]]
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

        special = {}

        for i in special_list:
            special[i[0][0:3]] = i[1].split(' ')[0: min(len(i[1].split(' ')), 4)]
    # return render(request, 'index.html', {'hotop': data.tolist(), 'len': len(data) * 2})
    return render(request, 'index.html', {'hotop': data.tolist(), 'len': len(data) * 2, 'review': review.tolist(), 'money': money.tolist(), 'special': special})

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
        special_list = np.array(top)[:,[0,4]]
        top = np.array(top)[:, [0, 2, 3]]
        for i in range(len(top)):
            top[i][1] = eval(top[i][1].replace('o', '0').replace('条评价', ''))
            top[i][2] = ''.join(re.findall(r'\d+', top[i][2].replace('o', '0')))

        tep = np.delete(np.array(top), np.where(top==''), axis=0)
        # print(tep)
        tep[:, 1] = tep[:, 1].astype(int)
        tep[:, 2] = tep[:, 2].astype(int)
        # print(tep)
        money = tep[np.argsort(-tep[:, 2])][:, [0]][:min(len(tep), 3), :][:,0]
        review = tep[np.argsort(-tep[:, 1])][:, [0, 1]][:min(len(tep), 5), :]

        special = {}

        for i in special_list:
            special[i[0][0:3]] = i[1].split(' ')

        print(special)
