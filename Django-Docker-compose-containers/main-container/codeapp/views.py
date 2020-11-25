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
        c1=requests.get('http://insertion-sort:8000/check/?arr='+query).json() #Add ip address of your pc
        c2=requests.get('http://quicksort-container:8000/check/?arr='+query).json()
        c3=requests.get('http://bubble-sort:8000/check/?arr='+query).json() #Add ip address of your pc
        c4=requests.get('http://selection-sort:8000/check/?arr='+query).json()
    return HttpResponse(str(c1['text'])+' : '+str(c1['arr'])+' ********* '+str(c2['text'])+' : '+str(c2['arr'])+"Quik sort "+str(c3['text'])+str(c3['arr'])+str(c4['text'])+' : '+str(c4['arr']))

def test(request):
    return HttpResponse('You are in container 2!!!')
