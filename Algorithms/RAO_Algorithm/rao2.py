# Python code of Rao-2 Algorithm
# Unconstrained optimization
# Sphere function
import random
import math
import numpy as np
maxfes = 1000 #Maximum functions evaluation
dim = 30 #Number of design variables
SearchAgents_no = 10 #Population size
Max_iter = math.floor(maxfes/SearchAgents_no) #Maximum number of iterations
lb = -100*np.ones(dim) #lower bound
ub = 100*np.ones(dim) #upper bound
def fitness(particle):
    y = 0
    for i in range(dim):
        y= y + particle[i]**2 # sphere function
    return y

Positions = np.zeros((SearchAgents_no, dim)) # search agent position
best_pos = np.zeros(dim) # search agent's best position
worst_pos = np.zeros(dim) # search agent's worst position

finval = np.zeros(Max_iter) # best score of each iteration
f1 = np.zeros(SearchAgents_no) # function value of current population
f2 = np.zeros(SearchAgents_no) # function value of updated population

for i in range(dim):
    Positions[:, i] = np.random.uniform(0,1, SearchAgents_no) * (ub[i] - lb[i]) + lb[i]
for k in range(0,Max_iter):
    best_score = float("inf")
    worst_score = float("-inf")
    for i in range(0,SearchAgents_no):

        # Return back the search agents that go beyond the boundaries of the search space
        for j in range(dim):
            Positions[i,j]=np.clip(Positions[i,j], lb[j], ub[j])

        f1[i]= fitness(Positions[i,:])
        if f1[i] < best_score :
            best_score=f1[i].copy(); # Update best
            best_pos=Positions[i,:].copy()
        if f1[i] > worst_score :
            worst_score=f1[i].copy(); # Update worst
            worst_pos=Positions[i,:].copy()
    # Update the Position of search agents including omegas
    finval[k] = best_score
    print("The best solution is: ",best_score , " in iteration number: ",k+1)
    Positioncopy = Positions.copy()
    r = np.random.randint(SearchAgents_no, size=1)
    for i in range(0,SearchAgents_no):
        if (f1[i] < f1[r]):
            for j in range (0,dim):
                r1=random.random() # r1 is a random number in [0,1]
                r2=random.random() # r1 is a random number in [0,1]
                Positions[i,j]= Positions[i,j] + r1*(best_pos[j]-worst_pos[j]) + r2*(np.abs(Positions[i,j])-np.abs(Positions[r,j]))#change in position
                Positions[i,j]=np.clip(Positions[i,j], lb[j], ub[j])
        else :
            for j in range (0,dim):
                r1=random.random() # r1 is a random number in [0,1]
                r2=random.random() # r1 is a random number in [0,1]
                Positions[i,j]= Positions[i,j] + r1*(best_pos[j]-worst_pos[j]) + r2*(np.abs(Positions[r,j])-np.abs(Positions[i,j]))#change in position
                Positions[i,j]=np.clip(Positions[i,j], lb[j], ub[j])
            f2[i] = fitness(Positions[i,:])
        for i in range(0,SearchAgents_no):
            if (f1[i] < f2[i]):
                Positions[i,:] = Positioncopy[i,:]
best_score = np.amin(finval)
print("The best solution is: ",best_score)