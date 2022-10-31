from django.shortcuts import render

# Create your views here.
def mainmap(request):
    return render(request, 'main_map.html')

def now_pos(request):
    return render(request, 'now_pos.html')