import numpy as np
import random

generations = 10
population_size = 5
vector_length = 2
vector_upperlimit = 5
vector_lowerlimit = -5


def initlize_population(population_size, vector_length):
    #empty numpy array for popuation.
    population = []
    #print(population)
    for i in range(0,population_size):
        temp = np.random.randint(vector_lowerlimit, vector_upperlimit, size = vector_length, dtype = np.int64)
        temp = np.append(temp, None)
        #print(str(temp))
        population.append(temp)
    population = np.asarray(population)
    #print(population)
    return population


def fitness(population):
    #print(population)
    fit = 0
    for data in population:
        for i in data:
            if i != None:
            #print(type(i))
                fit = fit + (i * i)

        data[-1] = (float("{0:.2f}".format(fit)))
        fit = 0
    #print(population)
    return population

def best_worst(population):
    #print(population)
    worst = np.argmax(population[:,-1])
    best = np.argmin(population[:,-1])
    #print("Best = "+ str(best) + " worst = " + str(worst))
    return population, best, worst

def updated_population(data):
    a = np.asarray(data[0])
    best_index = data[1]
    best_data = data[0][best_index]
    worst_index = data[2]
    worst_data = data[0][worst_index]
    new_data = []
    for data in a[:,range(0,len(a[0])-1)]:
        #print(data)
        temp = np.array([])
        for i in data:
            count = 0
            rand_1 = 0
            rand_2 = 0

            if count != len(a[0])+1:
                rand_1 = (float("{0:.2f}".format(random.uniform(0,1))))
                rand_2 = (float("{0:.2f}".format(random.uniform(0,1))))
                #print("rand 1 = "  + str(rand_1) + " rand_2 = " + str(rand_2))
                #print("best_data = " + str(best_data[count]) + " worst_data = " + str(worst_data[count]))
                #print("i = " + str(i))
                part1 = rand_1 * (best_data[count] - (abs(i)))
                part2 = rand_2 * (worst_data[count] - (abs(i)))
                #print("part 1 = "+ str(part1) + " part 2 = "+ str(part2))
                res = (float("{0:.2f}".format(i + (part1 - part2))))
                #print(str(res))

                count = count + 1
                temp = np.append(temp, res)
                #print(temp)
        temp = np.append(temp, None)
        new_data.append(temp)
    final_new_data = np.asarray(new_data)

    #print(final_new_data)
    final_new_data = fitness(final_new_data)
    #print("old population = " + str(a))
    #print("new populatio = " + str(final_new_data))
    return a,final_new_data

def compare(data):
    #compare both the new and cureent populations and update the best_data
    old_pop = data[0]
    new_pop = data[1]
    #print("old = " + str(old_pop) + "\nnew = " + str(new_pop))
    #print("old dim = " + str(old_pop.ndim))

    all_data = np.concatenate((old_pop, new_pop),0)
    print("\nall_data = " + str(all_data))
    all_data = all_data[all_data[:,-1].argsort(kind='quicksort')]
    print("\nall_data sorted = " + str(all_data))
    new_best_data = all_data[0:population_size]
    #print("sorted data = " + str(new_best_data))

    return new_best_data

def repeat(no_of_generations, data):
    print(" no of generations : " + str(generations) + "\ndata = " + str(data))
    for i in range(0, generations):
        data = compare(updated_population(best_worst(data)))

        print("final data = " + str(data))

if __name__ == "__main__":
    repeat(generations, compare(updated_population(best_worst(fitness(initlize_population(population_size, vector_length))))))
