from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return render(request,'codeapp/home.html')
def code(request):
    if request.method=="POST":
        query=request.POST['array']
        listofnum=query.split(',')
        lisofintnum=[]
        for i in listofnum:
            lisofintnum.append(int(i))
        inp = lisofintnum
        inp.sort()
        returnstring=''
        cnt=1
        for i in inp:
            returnstring+=str(i)
            if cnt<len(listofnum):
                returnstring+=", "
            cnt=cnt+1
        return HttpResponse('Sorted Array : '+returnstring)
        
    return HttpResponse('Please give input')


