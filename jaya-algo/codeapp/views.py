from django.shortcuts import render
from django.http import JsonResponse
import psycopg2
from django.http import HttpResponse




import math
import numpy as np
import random
import pandas as pd

#for reference https://medium.com/@dhiraj.p.rai/jaya-optimization-algorithm-16da8708691b
def myobj(p1):
    F=[]
    for i in range (len(p1)):
        x = p1.loc[i]
        f=(x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2)#changeequation
        F.append(f)
    return F


# pop_size = 50
# Gen = 10
lb=[-20,-20]
ub=[20,20]
message=''

def initialpopulation(mini,maxi,pop_size):
    pop=[]

    for i in range(pop_size):
        p=[]        
        for a,b in zip(mini,maxi):
            p.append(a + (b-a) * random.random())
        pop.append(p)    
    ini_pop=pd.DataFrame(pop)        
    return ini_pop


def updatepopulation(p1,dim):      
    best_x=np.array(p1.loc[p1['f'].idxmin][0:dim])    
    worst_x=np.array(p1.loc[p1['f'].idxmax][0:dim])
    new_x=[]
    for i in range(len(p1)):
        old_x=np.array(p1.loc[i][0:dim])           
        r1=np.random.random(dim)
        r2=np.random.random(dim)
        new_x.append(old_x+r1*(best_x-abs(old_x))-r2*(worst_x-abs(old_x)))    
    new_p1=pd.DataFrame(new_x)    
    return new_p1

def greedyselector(p1,new_p1):    
    for i in range(len(p1)):        
        if p1.loc[i]['f']>new_p1.loc[i]['f']:                 
            p1.loc[i]=new_p1.loc[i]    
    return p1

def trimr(new_p1,lb,ub):    
    col=new_p1.columns.values    
    for i in range(len(new_p1)):        
        for j in range(len(col)):            
            if new_p1.loc[i][j]>ub[j]:                
                  new_p1.loc[i][j]=ub[j]            
            elif new_p1.loc[i][j]<lb[j]:                          
                  new_p1.loc[i][j]=lb[j]    
    return new_p1

def jaya(*argv):
    pop_size, Gen, mini, maxi= argv
    lb=np.array(mini)
    ub=np.array(maxi)
    p1=initialpopulation(lb,ub,pop_size)
    p1['f']=myobj(p1)
    
    dim=len(lb)
    gen=0
    best=[]
    global message
    while (gen<Gen):
        new_p1=updatepopulation(p1,dim)
        new_p1=trimr(new_p1,lb,ub)
        new_p1['f']=myobj(new_p1)
        p1=greedyselector(p1,new_p1)
        gen=gen+1
        best=p1['f'].min()
        xbest=p1.loc[p1['f'].idxmin()][0:dim].tolist()
        message+="Generation "+str(gen)+" best "+str(best)+" "+str(xbest)+"\n"
    pop=[]        
    for row in (p1.values):
        pop.append(row[:-1])
    population_final=np.array(pop)
    return best,xbest,population_final.tolist()


def main(pop_size1,Gen1,lower_val,upper_val):

    global lb
    global ub 
    lb=[lower_val,lower_val,lower_val,lower_val]#changelb
    ub=[upper_val,upper_val,upper_val,upper_val]#changeub
    best,xbest,population_received = jaya(pop_size1, Gen1, lb, ub)
    print('The objective function value = {}'.format(best))
    print('The optimum values of variables = {}'.format(xbest))
    return best,xbest,population_received


def home(request):
    return render(request,'codeapp/home.html')
def code(request):
    if request.method=="POST":
        query=request.POST['array']
        returnstring='jaya algo'
        return HttpResponse('Sorted Array : '+returnstring)
        
    return HttpResponse('Please give input')


def check(request):
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "password",
                                    host = "db",
                                    port = "5432",
                                    database = "postgres")
        postgreSQL_select_Query = "SELECT opt_gen FROM codeapp_optimizationcodeinput where code_type='optimization';"
        cursor = connection.cursor()
        cursor.execute(postgreSQL_select_Query)
        opt_gen=cursor.fetchone()
        opt_gen=str(opt_gen)
        opt_gen=opt_gen.replace("('","")
        opt_gen=opt_gen.replace("',)","")
        postgreSQL_select_Query2 = "SELECT opt_pop_size FROM codeapp_optimizationcodeinput where code_type='optimization';"
        # cursor = connection.cursor()
        cursor.execute(postgreSQL_select_Query2)
        opt_pop_size=cursor.fetchone()
        opt_pop_size=str(opt_pop_size)
        opt_pop_size=opt_pop_size.replace("('","")
        opt_pop_size=opt_pop_size.replace("',)","")
        
        postgreSQL_select_Query3 = "SELECT code_lb FROM codeapp_optimizationcodeinput where code_type='optimization';"
        cursor.execute(postgreSQL_select_Query3)
        code_lb=cursor.fetchone()
        code_lb=str(code_lb)
        code_lb=code_lb.replace("('","")
        code_lb=code_lb.replace("',)","")
        
        postgreSQL_select_Query4 = "SELECT code_ub FROM codeapp_optimizationcodeinput where code_type='optimization';"
        cursor.execute(postgreSQL_select_Query4)
        code_ub=cursor.fetchone()
        code_ub=str(code_ub)
        code_ub=code_ub.replace("('","")
        code_ub=code_ub.replace("',)","")
        
        print(code_lb,code_ub)

        # Print PostgreSQL Connection properties
        # x=str(main(int(opt_pop_size),int(opt_gen)))+str(' ')+str(opt_gen)+' '+str(opt_pop_size)
        # returnstring=str(x)
        x,y,population_received=main(int(opt_pop_size),int(opt_gen),int(code_lb),int(code_ub))
        print('jaya algo container'+str(' ')+str(opt_gen)+' '+str(opt_pop_size))
        return JsonResponse({'best':str(x),'algo-coordi':str(y),'text':'Jaya Container','Lines':population_received})
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return JsonResponse({'best':'Error','algo-coordi':'Error','text':'Jaya Container','Lines':'error'})
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return JsonResponse({'best':'Error','algo-coordi':'Error','text':'Jaya Container','Lines':'error'})

