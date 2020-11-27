from django.shortcuts import render
import requests
from django.http import HttpResponse
import json
from .models import CodeInput
    

def home(request):
    # c1=requests.get('http://python-container:8000')
    # print(c1)
    return render(request,'codeapp/home.html')
def code(request):
    if request.method=="POST":
        query=request.POST['array']
        print(query)
        code_inp=CodeInput()
        code_inp.code_type='sorting'
        code_inp.codeinput=query
        code_inp.save()
        c1=requests.get('http://insertion-sort:8000/check/?arr='+query).json() #Add ip address of your pc
        c2=requests.get('http://quicksort-container:8000/check/?arr='+query).json()
        c3=requests.get('http://bubble-sort:8000/check/?arr='+query).json() #Add ip address of your pc
        c4=requests.get('http://selection-sort:8000/check/?arr='+query).json()
        code_inp.delete()
    # return HttpResponse(str(c1['text'])+' : '+str(c1['arr'])+str(c2['text'])+' : '+str(c2['arr'])+"Quik sort "+str(c3['text'])+str(c3['arr'])+str(c4['text'])+' : '+str(c4['arr']))
    dic1={'sortname':str(c1['text']),'sortoutput':str(c1['arr'])}
    dic2={'sortname':str(c2['text']),'sortoutput':str(c2['arr'])}
    dic3={'sortname':str(c3['text']),'sortoutput':str(c3['arr'])}
    dic4={'sortname':str(c4['text']),'sortoutput':str(c4['arr'])}
    alldic=[dic1,dic2,dic3,dic4]
    alldic={'alldic':alldic}
    return render(request,'codeapp/output.html',alldic)
def test(request):
    code_input =list( CodeInput.objects.values('codeinput','code_type'))
    print(code_input)
    s=''
    for i in code_input:
        s+=str(i['codeinput'])+"    "+str(i['code_type'])+"    "
    return HttpResponse(str(s))
    # return HttpResponse('You are in container 2!!!')
