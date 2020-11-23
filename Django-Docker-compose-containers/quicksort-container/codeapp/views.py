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
        arr = lisofintnum
        n = len(arr)
        quickSort(arr, 0, n-1)
        returnstring=''
        cnt=0
        for i in arr:
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
    arr = lisofintnum
    n = len(arr)
    quickSort(arr, 0, n-1)
    return JsonResponse({'arr':arr,'text':'this sorted array comes from QuickSort-Container!!!'})
 
def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
 
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)
 
def quickSort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)
