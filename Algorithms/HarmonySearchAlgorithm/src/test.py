import time
from src.tsp import Tsp, generate_tsp_xls, convert_txt_to_xls
from src.kp import Kp, generate_kp_xls
from src.outputData import OutputData
from src.harmonySearchAlgorithm import harmony_search_algorithm

filename = 'kp29'
expected_value = None

hm_considering_rate = 0.95
hm_pitch_adjusting_rate = 0.45
hm_bandwidth = 0.1

num_of_iterations = 1000000

num_of_rows_hm = 10

# generate_tsp_xls(number_of_places=20, max_coordinate=5000)
optimization_problem = Kp(filename)
# optimization_problem.use_intercity_txt_data(filename)
# optimization_problem.use_tsp_data(filename)

# optimization_problem.use_txt_data(filename)

output_data = OutputData(filename)
parameters = []
obj_functions = []
best_obj_fun = 1000000

start = time.time()
x = harmony_search_algorithm(
    num_of_rows_hm=num_of_rows_hm,
    num_of_iterations=num_of_iterations,
    hm_considering_rate=hm_considering_rate,
    hm_pitch_adjusting_rate=hm_pitch_adjusting_rate,
    hm_bandwidth=hm_bandwidth,
    opt_problem=optimization_problem,
    out_data=output_data,
    expected_value=expected_value
)
print("execution time: " + str(time.time() - start))

output_data.plot_data(filename + 'N = ' + str(num_of_rows_hm) + 'PAR = ' + str(hm_pitch_adjusting_rate) + 'BW = ' + str(hm_bandwidth))
output_data.data_to_xls()
print(str(filename) + ' N = ' + str(num_of_rows_hm) + ' PAR = ' + str(hm_pitch_adjusting_rate), 'BW = ' + str(hm_bandwidth), ' iteration = ' + str(num_of_iterations))
print(x)
print('Difference: ' + str(int(x[0].val_of_object_fun-expected_value)))
print('Error: ' + str(float((x[0].val_of_object_fun-expected_value)/expected_value)*100) + '%')

try:
    optimization_problem.visualise_solution(x[0])
except Exception as e:
    print(e)
