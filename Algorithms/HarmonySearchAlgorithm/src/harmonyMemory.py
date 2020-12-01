from typing import List
from src.optimizationProblem import OptimizationProblem, DoNotUseLastReturnedValue


class Harmony:
    def __init__(self, opt_problem: OptimizationProblem) -> None:
        self.notes = []
        self.val_of_object_fun = 0

        while not opt_problem.is_harmony_complete():
            try:
                new_note = opt_problem.generate_dec_variable(self.notes)
                self.notes.append(new_note)
            except DoNotUseLastReturnedValue:  # If harmony is completed do not use last returned value
                pass
        else:
            opt_problem.complete_harmony()
        self.val_of_object_fun = opt_problem.calculate_obj_fun(self.notes)

    def __getitem__(self, item):
        return self.notes[item]

    def __setitem__(self, key, value):
        self.notes[key] = value

    def __str__(self):
        return str([self.val_of_object_fun] + self.notes)

    def __len__(self):
        return len(self.notes)

    def __eq__(self, other: (list, float)):
        if self.val_of_object_fun != other[1]:
            return False
        for self_note, other_note in zip(self.notes, other[0]):
            if self_note != other_note:
                return False
        return True


class HarmonyMemory:
    def __init__(self, num_of_rows: int, opt_problem: OptimizationProblem) -> None:
        self.harmonies: List[Harmony] = []

        for row in range(0, num_of_rows):
            self.harmonies.append(Harmony(opt_problem))

    def __getitem__(self, item):
        return self.harmonies[item]

    def __setitem__(self, key, value):
        self.harmonies[key] = value

    def __str__(self):
        x: str = ''
        for elem in self.harmonies:
            x = x + str(elem) + '\n'
        return x

    def __len__(self):
        return len(self.harmonies)

    def index(self, value_to_find: str, note_index, gain: int):
        for index in range(0, len(self.harmonies)):
            try:
                if self.harmonies[index][note_index+gain] == value_to_find:
                    return [index, gain]
            except IndexError:  # If harmony doesn't exist try for next index
                pass
        for elem in self.harmonies:
            try:
                index = elem.notes.index(value_to_find)
                gain = index - note_index  # correct gain
                index = self.harmonies.index(elem)
                return [index, gain]
            except ValueError:  # If elem[value to find] doesn't exist try for next elem
                pass
        raise ValueError

    def max_note_index(self):
        ans = 0
        for elem in self.harmonies:
            tmp = len(elem.notes)
            if tmp > ans:
                ans = tmp
        return ans
