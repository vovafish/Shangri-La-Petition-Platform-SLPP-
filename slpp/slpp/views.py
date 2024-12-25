from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    #return HttpResponse("<h1>Shangri-La Petition Platform</h1>")
    return render(request, 'home.html')

def about(request):
    #return HttpResponse("<h1>About</h1>")
    return render(request, 'about.html')