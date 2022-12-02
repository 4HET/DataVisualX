# -*- coding: utf-8 -*-

from django.http import HttpResponse

from .models import LatLng


# 数据库插入操作
def insert(name, lat, lng):
    data = LatLng(name=name, lat=lat, lng=lng)
    data.save()

# 数据库查询操作
def select(name):
    data = LatLng.objects.filter(name=name).count()
    if data == 0:
        return 0
    else:
        data = LatLng.objects.values('lat', 'lng').filter(name=name)
        return data[0]