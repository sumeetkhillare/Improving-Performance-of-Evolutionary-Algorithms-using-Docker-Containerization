from random import randint, choice
from pandas import DataFrame, read_excel
from src.harmonyMemory import HarmonyMemory, Harmony
from src.optimizationProblem import OptimizationProblem, DoNotUseLastReturnedValue


def generate_kp_xls(
        filename='DataKp',
        number_of_objects=100,
        max_weight=100,
        max_value=100) -> None:
    objects = []
    weights = []
    values = []
    for i in range(1, number_of_objects + 1):
        objects.append(i)
        weights.append(randint(0, max_weight))
        values.append(randint(0, max_value))

    df = DataFrame({
        'object_id': objects,
        'weight': weights,
        'value': values
    })
    df.to_excel('../testcases/' + filename + '.xlsx', index=False)


class Kp(OptimizationProblem):
    def __init__(self, filename: str = 'DataKp', capacity: int = 1000):
        super().__init__()
        df = read_excel('C:/Users/Artur/PycharmProjects/Harmony Search Algorithm/testcases/' + filename + '.xlsx')
        # data are saved as 'object_id': (weight, value)
        self.data = {str(df.index[i]): (df.loc[i][1], df.loc[i][2]) for i in range(df.index[-1] + 1)}
        self.capacity = capacity
        self.available_cap = self.capacity
        self.complete = False
        self.gain = 0

    def use_txt_data(self, file_name):
        with open('C:/Users/Artur/PycharmProjects/Harmony Search Algorithm/datasets/kp/' + file_name + '_c.txt') as file:
            for line in file:
                if line == '\n':
                    break
                else:
                    self.capacity = int(line)
                    self.available_cap = self.capacity
        weight = []
        profits = []
        object_id = []
        i = 0
        with open('C:/Users/Artur/PycharmProjects/Harmony Search Algorithm/datasets/kp/' + file_name + '_w.txt') as file:
            for line in file:
                weight.append(line)
                object_id.append(i)
                i += 1
        with open('C:/Users/Artur/PycharmProjects/Harmony Search Algorithm/datasets/kp/' + file_name + '_p.txt') as file:
            for line in file:
                profits.append(line)

        self.data = {str(object_id[ind]): (int(weight[ind]), int(profits[ind])) for ind in range(len(weight))}

    def calculate_obj_fun(self, harmony):
        worth: int = 0
        for elem in harmony:
            worth += self.data[elem][1]
        return worth

    def generate_dec_variable(self, new_harmony: list) -> str:
        temp_data = list(set(self.data) - set(new_harmony))
        while True:
            if len(temp_data) == 0 or self.available_cap == 0:
                self.complete = True
                raise DoNotUseLastReturnedValue
            obj = temp_data.pop(temp_data.index(choice(temp_data)))
            weight = self.data[obj][0]
            if weight <= self.available_cap:
                self.available_cap -= weight
                return obj

    def take_dec_variable_hm(self, harmony_memory, new_harmony: list, note_index: int) -> str:
        self.gain = 0
        if self.available_cap == 0:
            self.complete = True
            raise DoNotUseLastReturnedValue
        # If exist any harmony with index bigger then note_index+gain
        while harmony_memory.max_note_index() > note_index + self.gain:
            [new_note, is_ok] = self.rand_note_for_note_index(harmony_memory, new_harmony, note_index + self.gain)
            if is_ok:
                return new_note
            else:
                self.gain += 1

        return self.generate_dec_variable(new_harmony)

    def rand_note_for_note_index(self, harmony_memory: HarmonyMemory, new_harmony: list, note_index: int) -> [str,
                                                                                                              bool]:
        dec_variables: list = []
        # Take all available dec_variables for note_index
        for elem in harmony_memory:
            if len(elem.notes) > note_index:  # Check is elem[note_index] exist
                dec_variables.append(elem[note_index])
        dec_variable_to_rand = list(set(dec_variables) - set(new_harmony))
        # Check is specific dec_variable is acceptable
        while len(dec_variable_to_rand) != 0:
            new_note = dec_variable_to_rand.pop(dec_variable_to_rand.index(choice(dec_variable_to_rand)))
            cap = self.data[new_note][0]
            if self.data[new_note][0] <= self.available_cap:
                self.available_cap -= cap
                return [new_note, True]
        else:
            return [-1, False]

    def pitch_adj_mechanism(self, harmony_memory, new_harmony: list, new_note: str, hm_bandwidth: float,
                            note_index: int) -> str:

        # If max_ind is to small adjust note_index and gain
        max_ind = harmony_memory.max_note_index()
        if max_ind < note_index + self.gain:
            note_index = max_ind
            self.gain = 0
        try:
            [harmony_index, self.gain] = harmony_memory.index(new_note, note_index, self.gain)
        except ValueError:  # If new_note not in harmony memory PAM is unnecessary
            return new_note

        notes_to_rand = []
        for note in harmony_memory[harmony_index]:
            if (note not in new_harmony and self.data[note][0] <= (self.available_cap + self.data[harmony_memory[harmony_index][note_index + self.gain]][0])) or note == new_note:
                notes_to_rand.append(note)
        index = notes_to_rand.index(new_note)
        index = int(index + hm_bandwidth * randint(-index, len(notes_to_rand) - index))
        self.available_cap += self.data[harmony_memory[harmony_index][note_index + self.gain]][0] - self.data[notes_to_rand[index]][0]
        return notes_to_rand[index]

    def complete_harmony(self):
        self.complete = False
        self.available_cap = self.capacity

    def visualise_solution(self, solution: Harmony):
        raise NotImplementedError("Visualization is not implemented")

    def is_harmony_complete(self):
        return self.complete

    def reverse_sort(self):
        return True

    def is_first_better_obj_fun(self, first, second):
        return first > second
