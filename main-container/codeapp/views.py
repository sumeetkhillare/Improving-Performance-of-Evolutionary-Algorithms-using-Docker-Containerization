from django.shortcuts import render
import requests
from django.http import HttpResponse
import json
from .models import CodeInput,OptimizationCodeInput
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from smtplib import SMTPRecipientsRefused

import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


from datetime import datetime
def home(request):
    return render(request,'codeapp/home.html')
def code(request):
    return render(request,'codeapp/home.html')

def test(request):
    code_input =list( CodeInput.objects.values('codeinput','code_type'))
    print(code_input)
    s=''
    for i in code_input:
        s+=str(i['codeinput'])+"    "+str(i['code_type'])+"    "
    return HttpResponse(str(s))
def optimizationcode(request):
    if request.method=="POST":
        opt_pop_size=request.POST['pop_size']
        opt_gen=request.POST['gen']
        lb=request.POST['lb']
        ub=request.POST['ub']
        recipient_email=request.POST['email']
        user_input_data="Population Size: "+str(opt_pop_size)+"\n"+"Generations: "+str(opt_gen)+"\n"+"Lower bound: "+str(lb)+"\n"+"Upper bound: "+str(ub)+"\n"
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
        

        fromaddr = "lastyearproj123@gmail.com"
        toaddr = recipient_email
        msg = MIMEMultipart() 
        msg['From'] = fromaddr 
        msg['To'] = toaddr 
        msg['Subject'] = "Optimization Results"
        now = datetime.now()
        message='Mail From Main Container\n'+str(dic_jaya['algoname'])+'     '+str(dic_jaya['algobest'])+'     '+str(dic_jaya['algocoordi'])+'\n'+str(dic_rao['algoname'])+'     '+str(dic_rao['algobest'])+'     '+str(dic_rao['algocoordi'])+'\n'+str(dic_rao2['algoname'])+'     '+str(dic_rao2['algobest'])+'     '+str(dic_rao2['algocoordi'])+'\n'+str(dic_rao3['algoname'])+'     '+str(dic_rao3['algobest'])+'     '+str(dic_rao3['algocoordi'])+'\n'+str(now)        
        
        body = str(user_input_data+message)
        msg.attach(MIMEText(body, 'plain')) 

        file1 = open("Optimization_Result.txt", "a")  # append mode 
        file1.write(user_input_data+message) 
        file1.close() 

        opfiles=["jaya.txt","rao-1.txt","rao-2.txt","rao-3.txt"]
        data_from_containers=[jaya_container['Lines'],rao_container['Lines'],rao2_container['Lines'],rao3_container['Lines']]
        for i in range(0,len(data_from_containers)):
            data_to_write=data_from_containers[i]
            file_path="/userapp/"+str(opfiles[i])
            file1=open(file_path,'a')
            for j in data_to_write:
                file1.write(j)
            file1.close()

        allfiles=["Optimization_Result.txt","jaya.txt","rao-1.txt","rao-2.txt","rao-3.txt"]
        dir_path="/userapp"
        for f in allfiles:
            file_path = os.path.join(dir_path, f)
            attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
            attachment.add_header('Content-Disposition','attachment', filename=f)
            msg.attach(attachment)
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login(fromaddr, "Lastyearproj@123") 
        text = msg.as_string() 
        try:
            s.sendmail(fromaddr, toaddr, text) 
        except SMTPRecipientsRefused:
            pass
        s.quit() 

        return render(request,'codeapp/output_optimization_containers.html',alldic)
