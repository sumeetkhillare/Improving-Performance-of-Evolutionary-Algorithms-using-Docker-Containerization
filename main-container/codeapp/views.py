from django.shortcuts import render
import requests
import random
from django.http import HttpResponse
import json
import smtplib  
from smtplib import SMTPRecipientsRefused
import time
import threading
import os
import psycopg2
import numpy as np
import datetime
jaya_container=''
rao_container=''
rao2_container=''
rao3_container=''
jaya_time=0
rao_time=0
rao2_time=0
rao3_time=0
equation="Equation: (x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2)"
message =''

from datetime import datetime
def home(request):
    global equation
    equation_dictionary={"equation":equation}
    return render(request,'codeapp/home.html',equation_dictionary)

def jaya_container_req(opt_pop_size,opt_gen,lb,ub):
    global jaya_container
    global jaya_time
    start = time.time()
    url='http://jaya-algo:8000/check/?ub='+str(ub)+'&lb='+str(lb)+'&popsize='+str(opt_pop_size)+'&gen='+str(opt_gen)
    jaya_container=requests.get(url).json()
    end=time.time()
    jaya_time=str(end-start)
    return jaya_container

def rao_container_req(opt_pop_size,opt_gen,lb,ub):
    global rao_container
    global rao_time
    start = time.time()
    url='http://rao-algo:8000/check/?ub='+str(ub)+'&lb='+str(lb)+'&popsize='+str(opt_pop_size)+'&gen='+str(opt_gen)
    rao_container=requests.get(url).json()
    end = time.time()
    rao_time = end-start
    return rao_container

def rao2_container_req(opt_pop_size,opt_gen,lb,ub):
    global rao2_container
    global rao2_time
    start=time.time()
    url='http://rao2-algo:8000/check/?ub='+str(ub)+'&lb='+str(lb)+'&popsize='+str(opt_pop_size)+'&gen='+str(opt_gen)
    rao2_container=requests.get(url).json()
    end=time.time()
    rao2_time=end-start
    return rao2_container

def rao3_container_req():
    global rao3_container
    global rao3_time
    start=time.time()
    rao3_container=requests.get('http://rao3-algo:8000/check/').json()
    end=time.time()
    rao3_time=end-start
    return rao3_container


def rao3Algo(Max_iter,SearchAgents_no,lower_val,upper_val,received_position):
    start = time.time()
    global message
    
    
    lenvar=4#changelenvar
    # SearchAgents_no = 10 #Population size
    # Max_iter = math.floor(maxfes/SearchAgents_no) #Maximum number of iterations
    lb = lower_val*np.ones(lenvar) #lower bound
    ub = upper_val*np.ones(lenvar) #upper bound
    var1=[]
    
    
    
    def fitness(x):
        eq=(x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2)
        return eq#changeequation
    Positions=received_position
    best_pos = np.zeros(lenvar) # search agent's best position
    worst_pos = np.zeros(lenvar) # search agent's worst position

    finval = np.zeros(Max_iter) # best score of each iteration
    f1 = np.zeros(SearchAgents_no) # function value of current population
    f2 = np.zeros(SearchAgents_no) # function value of updated population

    for i in range(lenvar):
        Positions[:, i] = np.random.uniform(0,1, SearchAgents_no) * (ub[i] - lb[i]) + lb[i]
    for k in range(0,Max_iter):
        best_score = float("inf")
        worst_score = float("-inf")
        for i in range(0,SearchAgents_no):

            # Return back the search agents that go beyond the boundaries of the search space
            for j in range(lenvar):
                Positions[i,j]=np.clip(Positions[i,j], lb[j], ub[j])

            f1[i]= fitness(Positions[i,:])
            if f1[i] < best_score :
                best_score=f1[i].copy(); # Update best
                best_pos=Positions[i,:].copy()
                var1.clear()
                for val in range(0,lenvar):
                    var1.append(Positions[i,:][val])
            if f1[i] > worst_score :
                worst_score=f1[i].copy(); # Update worst
                worst_pos=Positions[i,:].copy()
            # Update the Position of search agents including omegas
            finval[k] = best_score
            Positioncopy = Positions.copy()
            r = np.random.randint(SearchAgents_no, size=1)
            
            for i in range(0,SearchAgents_no):
                if (f1[i] < f1[r]):
                    for j in range (0,lenvar):
                        r1=random.random() # r1 is a random number in [0,1]
                        r2=random.random() # r1 is a random number in [0,1]
                        Positions[i,j]= Positions[i,j] + r1*(best_pos[j]-np.abs(worst_pos[j])) + r2*(np.abs(Positions[i,j])-Positions[i
                        ,j])#change in position
                        Positions[i,j]=np.clip(Positions[i,j], lb[j], ub[j])
                else :
                    for j in range (0,lenvar):
                        r1=random.random() # r1 is a random number in [0,1]
                        r2=random.random() # r1 is a random number in [0,1]
                        Positions[i,j]= Positions[i,j] + r1*(best_pos[j]-np.abs(worst_pos[j])) + r2*(np.abs(Positions[r,j])-Positions[i,j]) #change in position
                        Positions[i,j]=np.clip(Positions[i,j], lb[j], ub[j])
                        f2[i] = fitness(Positions[i,:])

            for i in range(0,SearchAgents_no):
                if (f1[i] < f2[i]):
                    Positions[i,:] = Positioncopy[i,:]
        message+="The best solution is: "+str(best_score) + " in iteration number: "+str(k+1)+"\n"
    
    best_score = np.amin(finval)
    message+="The best solution is: "+str(best_score)+" pos "+str(best_pos[0])+" "+str(worst_pos[-1])
    
    end=time.time()
    calculated_time=str(end-start)
    return best_score,var1,calculated_time


def optimizationcode(request):
    if request.method=="POST":
        global equation
        opt_pop_size=request.POST['pop_size']
        opt_gen=request.POST['gen']
        lb=request.POST['lb']
        ub=request.POST['ub']
        user_input_data="Population Size: "+str(opt_pop_size)+"\n"+"Generations: "+str(opt_gen)+"\n"+"Lower bound: "+str(lb)+"\n"+"Upper bound: "+str(ub)+"\n"
        
        global jaya_container
        global rao_container
        global rao2_container
        global rao3_container
        global jaya_time
        global rao_time
        global rao2_time
        global rao3_time
                
        t1 = threading.Thread(target=jaya_container_req,args=(opt_pop_size,opt_gen,lb,ub))
        t2 = threading.Thread(target=rao_container_req,args=(opt_pop_size,opt_gen,lb,ub))
        t3 = threading.Thread(target=rao2_container_req,args=(opt_pop_size,opt_gen,lb,ub))
        
        t1.start()
        t2.start()
        t3.start()
        
        t1.join()
        t2.join()
        t3.join()
        end = time.time()
        
        jaya_algo_data={'algoname':str(jaya_container['text']),'algobest':str(jaya_container['best']),'algocoordi':str(jaya_container['algo-coordi']),'algotime':str(jaya_time)}
        rao_algo_data={'algoname':str(rao_container['text']),'algobest':str(rao_container['best']),'algocoordi':str(rao_container['algo-coordi']),'algotime':str(rao_time)}
        rao2_algo_data={'algoname':str(rao2_container['text']),'algobest':str(rao2_container['best']),'algocoordi':str(rao2_container['algo-coordi']),'algotime':str(rao2_time)}
        
        concat=np.concatenate((np.array(jaya_container['Lines']),np.array(rao_container['Lines']),np.array(rao2_container['Lines'])),axis=0)
        best_score,coordinate,calc_time=rao3Algo(int(opt_gen), 3*(int(opt_pop_size)), int(lb), int(ub), concat)
        rao3_algo_data={'algoname':str("Rao3 Final Output"),'algobest':str(best_score),'algocoordi':str(coordinate),'algotime':str(calc_time)}
        alldata=[jaya_algo_data,rao_algo_data,rao2_algo_data
        ,rao3_algo_data]
        alldata={'alldata':alldata,'equation':equation}
        
        return render(request,'codeapp/output_optimization_containers.html',alldata)


def search(request):
    popsize=request.GET['popsize']
    lb=request.GET['lb']
    ub=request.GET['ub']
    gen=request.GET['gen']
    print(popsize,gen,lb,ub)
    return HttpResponse("hii")


'http://localhost:4012/check/?ub=10&lb=-10&popsize=10&gen=10'