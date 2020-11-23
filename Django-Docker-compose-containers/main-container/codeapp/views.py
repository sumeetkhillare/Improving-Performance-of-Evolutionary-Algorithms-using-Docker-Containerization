from django.shortcuts import render
import requests
from django.http import HttpResponse
import json


def home(request):
    # return HttpResponse('You are in container 2!!!')
    return render(request,'codeapp/home.html')
def code(request):
    if request.method=="POST":
        query=request.POST['array']
        print(query)
        l=requests.get('http://192.168.0.5:4000/check/?arr='+query).json() #Add ip address of your pc
        k=requests.get('http://192.168.0.5:4002/check/?arr='+query).json() #Add ip address of your pc
    return HttpResponse(str(l['text'])+' : '+str(l['arr'])+' ********* '+str(k['text'])+' : '+str(l['arr']))


def test(request):
    return HttpResponse('You are in container 2!!!')
