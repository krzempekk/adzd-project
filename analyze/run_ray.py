import ray
import os
import numpy as np
import time
from processing_fun import process_file

# ray.init(num_cpus=8)
ray.init()

@ray.remote
def processing_task(file_name):
    return process_file(file_name, aggregate='heatmap')


input_folder = "processed_input_1"
output_folder = "output_1"
file_list = os.listdir(input_folder)
time_start = time.time()

# Launch four parallel square tasks.
futures = [processing_task.remote(f"{input_folder}/{file}") for file in file_list]

results = ray.get(futures)

print(f"time elapsed {time.time() - time_start}")
np.savetxt(f"{output_folder}/heatmap_1.txt", np.sum(results, axis=0))

