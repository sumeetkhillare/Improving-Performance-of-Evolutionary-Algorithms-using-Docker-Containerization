from random import randint, choice
from pandas import DataFrame, read_excel
from math import sqrt
from src.harmonyMemory import HarmonyMemory, Harmony
from src.optimizationProblem import OptimizationProblem
import matplotlib.pyplot as plt


def generate_tsp_xls(
        filename='DataTsp',
        number_of_places=100,
        max_coordinate=50) -> None:
    x_coordinate = []
    y_coordinate = []
    coordinates = []
    places = []
    i = 1
    while len(places) < number_of_places:
        x = randint(0, max_coordinate)
        y = randint(0, max_coordinate)
        pair = (x, y)
        if pair not in coordinates:
            coordinates.append(pair)
            x_coordinate.append(x)
            y_coordinate.append(y)
            places.append(i)
            i += 1
    df = DataFrame({
        'place_id': places,
        'x_coordinate': x_coordinate,
        'y_coordinate': y_coordinate
    })
    df.to_excel('../testcases/' + filename + '.xlsx', index=False)


def convert_txt_to_xls(original_file_name, new_file_name):
    places = []
    x_coordinates = []
    y_coordinates = []
    with open('../datasets/' + original_file_name + '.txt') as file:
        place_id = 1
        for line in file:
            (x, y) = line.split()
            places.append(place_id)
            x_coordinates.append(x)
            y_coordinates.append(y)
            place_id += 1

    df = DataFrame({
        'place_id': places,
        'x_coordinate': x_coordinates,
        'y_coordinate': y_coordinates
    })
    df.to_excel('../testcases/' + new_file_name + '.xlsx', index=False)


class Tsp(OptimizationProblem):
    def __init__(self, filename: str = 'DataTsp'):
        super().__init__()
        df = read_excel('C:/Users/Artur/PycharmProjects/Harmony Search Algorithm/testcases/' + filename + '.xlsx')
        # data are saved as 'place_id': (x_coordinate, y_coordinate)
        self.data = {str(df.loc[i][0]): (df.loc[i][1], df.loc[i][2]) for i in range(df.index[-1] + 1)}
        self.distance = count_distance(self.data)
        self.complete = False
        self.gain = 0
        self.visualization = True

    def use_intercity_txt_data(self, file_name):
        self.visualization = False
        distance = {}
        with open('../datasets/' + file_name + '.txt') as file:
            first_place_id = 1
            for line in file:
                if line == '\n':
                    break
                temp_dict = {}
                second_place_id = 1
                for elem in line.split():
                    temp_dict[str(second_place_id)] = float(elem)
                    second_place_id += 1
                distance[str(first_place_id)] = temp_dict
                first_place_id += 1

        self.data = {key: value for (key, value) in zip(distance.keys(), [(0, 0)]*len(distance.keys()))}
        self.distance = distance

    def use_tsp_data(self, file_name):
        self.visualization = True
        with open('C:/Users/Artur/PycharmProjects/Harmony Search Algorithm/datasets/tsp/' + file_name + '.tsp') as file:
            data = {}
            i = 0
            for line in file:
                if i < 1:
                    i += 1
                    continue
                if line == 'EOF\n':
                    break
                line_list = line.split()
                data[str(line_list[0])] = (int(float(line_list[1])), int(float(line_list[2])))

        self.data = data
        self.distance = count_distance(self.data)

    def calculate_obj_fun(self, harmony: list):
        distance: float = 0
        last_place = False
        for place in harmony:
            if last_place:
                distance += self.distance[str(last_place)][str(place)]
            last_place = place
        return distance

    def generate_dec_variable(self, new_harmony: list) -> str:
        if len(new_harmony) == 0:  # If solution is empty
            return '1'
        temp_data = list(set(self.data.keys()) - set(new_harmony))

        if len(temp_data) == 0:  # If solution is full
            self.complete = True
            return new_harmony[0]
        return choice(temp_data)  # Else

    def take_dec_variable_hm(self, harmony_memory: HarmonyMemory, new_harmony: list, note_index: int) -> str:
        self.gain = 0
        # If solution is empty
        if len(new_harmony) == 0:
            return '1'

        # If solution is full
        if len(new_harmony) == len(self.data):
            self.complete = True
            return new_harmony[0]

        while (note_index + self.gain) < len(harmony_memory[0])-1:
            # Try to find dec variable in note_index column of harmony memory
            [new_note, is_ok] = rand_note_for_note_index(harmony_memory, new_harmony, note_index + self.gain)
            if is_ok:
                return new_note
            else:
                # If it doesn't work try with next column
                self.gain += 1
        # If no method worked
        return self.generate_dec_variable(new_harmony)

    def pitch_adj_mechanism(self, harmony_memory: HarmonyMemory, new_harmony: list, new_note: str, hm_bandwidth: float,
                            note_index: int) -> str:
        # If solution is empty
        if len(new_harmony) == 0:
            return '1'
        # If solution is full
        if len(new_harmony) == len(self.data):
            self.complete = True
            return new_harmony[0]

        [harmony_index, self.gain] = harmony_memory.index(new_note, note_index, self.gain)

        notes_to_rand = []
        for note in harmony_memory[harmony_index]:
            if note not in new_harmony:
                notes_to_rand.append(note)
        index = notes_to_rand.index(new_note)
        index = int(index + hm_bandwidth * randint(-index, len(notes_to_rand) - index))
        return notes_to_rand[index]

    def complete_harmony(self):
        self.complete = False

    def visualise_solution(self, solution: Harmony):
        if self.visualization:
            x_coordinate = []
            y_coordinate = []
            for note in solution:
                x_coordinate.append(self.data[note][0])
                y_coordinate.append(self.data[note][1])
                plt.plot(x_coordinate, y_coordinate)
            plt.show()
        else:
            raise NotImplementedError("Visualization is not implemented")

    def is_harmony_complete(self):
        return self.complete

    def reverse_sort(self):
        return False

    def is_first_better_obj_fun(self, first, second):
        return first < second

def count_distance(data: dict) -> dict:
    t_displacements = {}
    for start in data:
        temp_dict = {}
        for finish in data:
            if finish != start:
                x_displacement = data[finish][0] - data[start][0]
                y_displacement = data[finish][1] - data[start][1]
                displacement = sqrt(pow(x_displacement, 2) + pow(y_displacement, 2))
                temp_dict[finish] = displacement
        t_displacements[start] = temp_dict
    return t_displacements


def rand_note_for_note_index(harmony_memory: HarmonyMemory, new_harmony: list, note_index: int) -> [str, bool]:
    dec_variables: list = []
    for elem in harmony_memory:
        dec_variables.append(elem[note_index])
    dec_variable_to_rand = list(set(dec_variables) - set(new_harmony))
    if len(dec_variable_to_rand) != 0:
        new_note = choice(dec_variable_to_rand)
        return [new_note, True]
    else:
        return [-1, False]
