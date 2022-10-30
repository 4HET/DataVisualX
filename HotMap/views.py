from django.shortcuts import render

from . import hot_map


# Create your views here.
def hotmap(request):
    hot_map.make_map()
    return render(request, 'hot_map.html')