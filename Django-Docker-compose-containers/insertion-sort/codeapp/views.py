from django.shortcuts import render
from django.http import JsonResponse

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


def check(request):
    query=request.GET.get('arr')
    print(query)
    #getting full url of requesting website
    arr=query.split(',')
    print(arr)
    listofnum=arr
    lisofintnum=[]
    for i in listofnum:
        lisofintnum.append(int(i))
    x = lisofintnum
    insertionSort(x)
    print(x)

    return JsonResponse({'arr':x,'text':'this sorted array comes from InsertionSort-container!!!'})
    # return HttpResponse('You are in container 1!!! + Result : '+str(arr))

def insertionSort(arr): 
    for i in range(1, len(arr)): 
        key = arr[i] 
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key 
