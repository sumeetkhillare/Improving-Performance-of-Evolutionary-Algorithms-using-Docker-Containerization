from django.shortcuts import render
from django.http import JsonResponse
import psycopg2
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
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "password",
                                    host = "db",
                                    port = "5432",
                                    database = "postgres")
        postgreSQL_select_Query = "SELECT codeinput FROM codeapp_codeinput where code_type='sorting';"
        cursor = connection.cursor()
        cursor.execute(postgreSQL_select_Query)
        s=cursor.fetchone()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
        
        s=str(s)
        s=s.replace("('","")
        s=s.replace("',)","")
        print(s)
        lisofintnum=s.split(",")
        for i in range(0,len(lisofintnum)):
            lisofintnum[i]=int(lisofintnum[i])
        n=len(lisofintnum)
        quickSort(lisofintnum,0,n-1)
        verify_str=''
        for i in lisofintnum:
            verify_str+=str(i)
            verify_str+=', '
        return JsonResponse({'arr':str(verify_str),'text':'Quick Sort Container'})
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return JsonResponse({'arr':'Error','text':'Quick Sort Container'})
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return JsonResponse({'arr':'Error','text':'Quick Sort Container'}) 
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
