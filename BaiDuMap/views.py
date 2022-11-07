import json

import numpy as np
import requests
from django.shortcuts import render
import pandas as pd

# Create your views here.
def mainmap(request):
    return render(request, 'main_map.html')

def now_pos(request):
    return render(request, 'now_pos.html')

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