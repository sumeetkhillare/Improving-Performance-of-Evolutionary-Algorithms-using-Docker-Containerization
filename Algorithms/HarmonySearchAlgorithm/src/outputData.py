from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
from typing import List


class OutputData:
    def __init__(self, filename: str = 'obj_fun_data'):
        self.obj_functions: List[int] = []
        self.iterations: List[int] = []
        self.path_of_data = str('C:/Users/Artur/PycharmProjects/Harmony Search Algorithm/data/' + filename + '.xlsx')

    def add_data(self, iteration, obj_function):
        self.obj_functions.append(obj_function)
        self.iterations.append(iteration)

    def data_to_xls(self):
        df1 = DataFrame({
            'obj_function': self.obj_functions,
            'iterations': self.iterations})

        df1.to_excel(self.path_of_data, index=False)


    def plot_data(self, title):
        plt.plot(self.iterations, self.obj_functions)
        plt.title(title)
        plt.xlabel('Iterations')
        plt.ylabel('Objective function')
        plt.show()
