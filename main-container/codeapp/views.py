from django.shortcuts import render
import requests
from django.http import HttpResponse
import json
from .models import CodeInput,OptimizationCodeInput
import smtplib


def home(request):
    # c1=requests.get('http://python-container:8000')
    # print(c1)
    return render(request,'codeapp/home.html')
def code(request):
    return render(request,'codeapp/home.html')
    # if request.method=="POST":
    #     query=request.POST['array']
    #     print(query)
    #     code_inp=CodeInput()
    #     code_inp.code_type='sorting'
    #     code_inp.codeinput=query
    #     code_inp.save()
    #     c1=requests.get('http://insertion-sort:8000/check/?arr='+query).json() #Add ip address of your pc
    #     c2=requests.get('http://quicksort-container:8000/check/?arr='+query).json()
    #     c3=requests.get('http://bubble-sort:8000/check/?arr='+query).json() #Add ip address of your pc
    #     c4=requests.get('http://selection-sort:8000/check/?arr='+query).json()
    #     code_inp.delete()
    #
    # # return HttpResponse(str(c1['text'])+' : '+str(c1['arr'])+str(c2['text'])+' : '+str(c2['arr'])+"Quik sort "+str(c3['text'])+str(c3['arr'])+str(c4['text'])+' : '+str(c4['arr']))
    # dic1={'sortname':str(c1['text']),'sortoutput':str(c1['arr'])}
    # dic2={'sortname':str(c2['text']),'sortoutput':str(c2['arr'])}
    # dic3={'sortname':str(c3['text']),'sortoutput':str(c3['arr'])}
    # dic4={'sortname':str(c4['text']),'sortoutput':str(c4['arr'])}
    # alldic=[dic1,dic2,dic3,dic4]
    # alldic={'alldic':alldic}
    # return render(request,'codeapp/output.html',alldic)
def test(request):
    code_input =list( CodeInput.objects.values('codeinput','code_type'))
    print(code_input)
    s=''
    for i in code_input:
        s+=str(i['codeinput'])+"    "+str(i['code_type'])+"    "
    return HttpResponse(str(s))
    # return HttpResponse('You are in container 2!!!')
def optimizationcode(request):
    if request.method=="POST":
        opt_pop_size=request.POST['pop_size']
        opt_gen=request.POST['gen']
        lb=request.POST['lb']
        ub=request.POST['ub']
        opt_inp=OptimizationCodeInput()
        opt_inp.code_type='optimization'
        opt_inp.opt_pop_size=opt_pop_size
        opt_inp.opt_gen=opt_gen
        opt_inp.code_lb=lb
        opt_inp.code_ub=ub
        opt_inp.save()
        jaya_container=requests.get('http://jaya-algo:8000/check/').json()
        rao_container=requests.get('http://rao-algo:8000/check/').json()
        rao2_container=requests.get('http://rao2-algo:8000/check/').json()
        rao3_container=requests.get('http://rao3-algo:8000/check/').json()
        opt_inp.delete()
        dic_jaya={'algoname':str(jaya_container['text']),'algobest':str(jaya_container['best']),'algocoordi':str(jaya_container['algo-coordi'])}
        dic_rao={'algoname':str(rao_container['text']),'algobest':str(rao_container['best']),'algocoordi':str(rao_container['algo-coordi'])}
        dic_rao2={'algoname':str(rao2_container['text']),'algobest':str(rao2_container['best']),'algocoordi':str(rao2_container['algo-coordi'])}
        dic_rao3={'algoname':str(rao3_container['text']),'algobest':str(rao3_container['best']),'algocoordi':str(rao3_container['algo-coordi'])}
        alldic=[dic_jaya,dic_rao,dic_rao2,dic_rao3] #,dic_rao,dic_rao2
        alldic={'alldic':alldic}
        
        #Send mail
        email='lastyearproj123@gmail.com'
        email2='cur53onu@gmail.com'
        password='Lastyearproj@123'
        message='Mail From Main Container\n'+str(dic_jaya['algoname'])+'     '+str(dic_jaya['algobest'])+'     '+str(dic_jaya['algocoordi'])+'\n'+str(dic_rao['algoname'])+'     '+str(dic_rao['algobest'])+'     '+str(dic_rao['algocoordi'])+'\n'+str(dic_rao2['algoname'])+'     '+str(dic_rao2['algobest'])+'     '+str(dic_rao2['algocoordi'])+'\n'+str(dic_rao3['algoname'])+'     '+str(dic_rao3['algobest'])+'     '+str(dic_rao3['algocoordi'])        
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email2,message)
        server.quit()

        return render(request,'codeapp/output_optimization_containers.html',alldic)
