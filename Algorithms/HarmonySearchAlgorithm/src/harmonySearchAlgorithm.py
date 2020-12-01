from numpy.random import uniform as random
from src.harmonyMemory import HarmonyMemory
from src.optimizationProblem import OptimizationProblem, DoNotUseLastReturnedValue
from src.outputData import OutputData


def harmony_search_algorithm(
        num_of_rows_hm: int,
        num_of_iterations,
        hm_considering_rate,
        hm_pitch_adjusting_rate,
        hm_bandwidth,
        opt_problem: OptimizationProblem,
        out_data: OutputData,
        expected_value=None
) -> HarmonyMemory:
    # initialize the harmony memory randomly and calculate object function
    harmony_memory = HarmonyMemory(num_of_rows_hm, opt_problem)
    iteration = 1

    # main algorithm loop
    while iteration < num_of_iterations:
        new_harmony = []
        # iterating by notes in new harmony
        note_index = 0
        while not opt_problem.is_harmony_complete():
            try:
                # deciding if the next note should be generated or taken from memory
                if hm_considering_rate > random(0, 1):
                    new_note = opt_problem.take_dec_variable_hm(harmony_memory, new_harmony, note_index)
                    # deciding if the pitch adjusting mechanism should be used
                    if hm_pitch_adjusting_rate > random(0, 1):
                        new_note = opt_problem.pitch_adj_mechanism(harmony_memory, new_harmony, new_note, hm_bandwidth,
                                                                   note_index)
                else:
                    new_note = opt_problem.generate_dec_variable(new_harmony)

                new_harmony.append(new_note)
                note_index += 1
            except DoNotUseLastReturnedValue:  # If harmony is completed do not use last returned value
                pass
        else:
            opt_problem.complete_harmony()

        harmony_memory.harmonies.sort(key=lambda harmony: harmony.val_of_object_fun, reverse=opt_problem.reverse_sort())
        # calculating new harmony objective function value
        val_of_object_fun = opt_problem.calculate_obj_fun(new_harmony)

        # comparing new harmony with the worst from the memory by the objective function and exchanging solutions
        if opt_problem.is_first_better_obj_fun(val_of_object_fun, harmony_memory[-1].val_of_object_fun):
            if (new_harmony, val_of_object_fun) not in harmony_memory:
                # saving new_harmony obj. function in output data
                out_data.add_data(iteration, val_of_object_fun)

                harmony_memory[len(harmony_memory) - 1].notes = new_harmony
                harmony_memory[len(harmony_memory) - 1].val_of_object_fun = val_of_object_fun
        iteration = iteration + 1
        if expected_value and opt_problem.is_first_better_obj_fun(harmony_memory[0].val_of_object_fun, int(expected_value)):
            return harmony_memory
    return harmony_memory
