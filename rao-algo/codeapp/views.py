from django.shortcuts import render
from django.http import JsonResponse
import psycopg2
from django.http import HttpResponse




# Python code of Rao-1 Algorithm
# Unconstrained optimization
# Sphere function
import random
import math
import numpy as np
def raoAlgo(Max_iter,SearchAgents_no):
    maxfes = 500000  # Maximum functions evaluation
    dim = 4  # Number of design variables
    # SearchAgents_no = 10  # Population size
    # Max_iter = math.floor(maxfes / SearchAgents_no)  # Maximum number of iterations
    # Max_iter = 100
    lb = -20 * np.ones(dim)  # lower bound
    ub = 20 * np.ones(dim)  # upper bound


    def fitness(particle):
        y = 0
        for i in range(dim):
            y = y*y - particle[i] ** 2  # sphere function
        return y



    Positions = np.zeros((SearchAgents_no, dim))  # search agent position
    best_pos = np.zeros(dim)  # search agent's best position
    worst_pos = np.zeros(dim)  # search agent's worst position

    finval = np.zeros(Max_iter)  # best score of each iteration
    f1 = np.zeros(SearchAgents_no)  # function value of current population
    f2 = np.zeros(SearchAgents_no)  # function value of updated population

    for i in range(dim):
        Positions[:, i] = np.random.uniform(0, 1, SearchAgents_no) * (ub[i] - lb[i]) + lb[i]
    for k in range(0, Max_iter):
        best_score = float("inf")
        worst_score = float("-inf")
        for i in range(0, SearchAgents_no):

            # Return back the search agents that go beyond the boundaries of the search space
            for j in range(dim):
                Positions[i, j] = np.clip(Positions[i, j], lb[j], ub[j])

            f1[i] = fitness(Positions[i, :])
            if f1[i] < best_score:
                best_score = f1[i].copy();  # Update best
                best_pos = Positions[i, :].copy()
            if f1[i] > worst_score:
                worst_score = f1[i].copy();  # Update worst
                worst_pos = Positions[i, :].copy()

            # Update the Position of search agents including omegas
            finval[k] = best_score
            # print("The best solution is: ", best_score, " in iteration number: ", k + 1)
            Positioncopy = Positions.copy()
            for i in range(0, SearchAgents_no):
                for j in range(0, dim):
                    r1 = random.random()  # r1 is a random number in [0,1]
                    Positions[i, j] = Positions[i, j] + r1 * (best_pos[j] - worst_pos[j])  # change in position
                    Positions[i, j] = np.clip(Positions[i, j], lb[j], ub[j])
                f2[i] = fitness(Positions[i, :])
            for i in range(0, SearchAgents_no):
                if (f1[i] < f2[i]):
                    Positions[i, :] = Positioncopy[i, :]
    best_score = np.amin(finval)
    return best_score,[best_pos[0],worst_pos[-1]]



def home(request):
    return render(request,'codeapp/home.html')
def code(request):
    if request.method=="POST":
        query=request.POST['array']
        # listofnum=query.split(',')
        # lisofintnum=[]
        returnstring='rao algo'
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
        # Print PostgreSQL Connection properties
        # x=str(main(int(opt_pop_size),int(opt_gen)))+str(' ')+str(opt_gen)+' '+str(opt_pop_size)
        # returnstring=str(x)
        x,y=raoAlgo(int(opt_pop_size),int(opt_gen))
        print('rao algo container'+str(' ')+str(opt_gen)+' '+str(opt_pop_size))
        return JsonResponse({'best':str(x),'algo-coordi':str(y),'text':'Rao1 Container'})
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return JsonResponse({'best':'Error','algo-coordi':'Error','text':'Rao1 Container'})
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return JsonResponse({'best':'Error','algo-coordi':'Error','text':'Rao1 Container'})
    # return HttpResponse('You are in container 1!!! + Result : '+str(arr))
