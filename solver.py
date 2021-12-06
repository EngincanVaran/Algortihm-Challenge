import json
import sys
import numpy as np
from timeit import default_timer as timer
from Algorithms.brute_force import brute_force_it
from Algorithms.brute_force_with_penalty import brute_force_it_penalty
from Algorithms.greedy_approach import greedy
from Algorithms.greedy_approach_with_penalty import greedy_penalty
from Algorithms.brute_force_with_penalty_capacity import brute_force_it_capacity
from Algorithms.greedy_approach_with_capacity import greedy_capacity

POSSIBLE_ALGORITHMS = ["brute-force", "greedy",
                       "greedy-penalty", "brute-force-penalty",
                       "brute-force-capacity", "greedy-capacity"]


def prepare_output(min_time, min_partition, min_time_list):
    result = {}
    result["total_delivery_duration"] = int(min_time)
    result["routes"] = {}
    for index in range(len(min_time_list)):
        result["routes"][str(index+1)] = {}
        result["routes"][str(
            index+1)]["delivery_duration"] = int(min_time_list[index])
        result["routes"][str(
            index+1)]["jobs"] = str(min_partition[index])
    print("Total Delivery Time:", str(min_time))
    return result


def main(argv):
    if(len(argv) != 2):
        print("Invalid Arguments")
        return
    json_file_name = argv[0]
    algorithm = argv[1]
    try:
        file = open("Inputs/" + json_file_name)
    except IOError:
        print("Could not open file!")
        return

    if algorithm not in POSSIBLE_ALGORITHMS:
        print("Invalid Algorithm")
        return

    json_data = json.load(file)
    vehicles = json_data["vehicles"]
    jobs = json_data["jobs"]
    time_matrix = np.array(json_data["matrix"])

    if algorithm == "brute-force":
        start = timer()
        min_time, min_partition, min_time_list = brute_force_it(
            matrix=time_matrix,
            jobs=jobs,
            vehicles=vehicles)
        output = prepare_output(min_time, min_partition, min_time_list)
        end = timer()
        print("Elapsed Time (Brute-Force):", end-start, "seconds.")

    elif algorithm == "brute-force-penalty":
        start = timer()
        min_time, min_partition, min_time_list = brute_force_it_penalty(
            matrix=time_matrix,
            jobs=jobs,
            vehicles=vehicles)
        output = prepare_output(min_time, min_partition, min_time_list)
        end = timer()
        print("Elapsed Time (Brute-Force-Penalty):", end-start, "seconds.")

    elif algorithm == "brute-force-capacity":
        start = timer()
        min_time, min_partition, min_time_list = brute_force_it_capacity(
            matrix=time_matrix,
            jobs=jobs,
            vehicles=vehicles)
        output = prepare_output(min_time, min_partition, min_time_list)
        end = timer()
        print("Elapsed Time (Brute-Force-Capacity):", end-start, "seconds.")

    elif algorithm == "greedy":
        start = timer()
        # min_time, min_partition, min_time_list =
        min_time, min_partition, min_time_list = greedy(
            matrix=time_matrix,
            jobs=jobs,
            vehicles=vehicles)
        output = prepare_output(min_time, min_partition, min_time_list)
        end = timer()
        print("Elapsed Time (Greedy):", end-start, "seconds.")

    elif algorithm == "greedy-penalty":
        start = timer()
        # min_time, min_partition, min_time_list =
        min_time, min_partition, min_time_list = greedy_penalty(
            matrix=time_matrix,
            jobs=jobs,
            vehicles=vehicles)
        output = prepare_output(min_time, min_partition, min_time_list)
        end = timer()
        print("Elapsed Time (Greedy-Penalty):",
              end-start, "seconds.")

    elif algorithm == "greedy-capacity":
        start = timer()
        # min_time, min_partition, min_time_list =
        min_time, min_partition, min_time_list = greedy_capacity(
            matrix=time_matrix,
            jobs=jobs,
            vehicles=vehicles)
        output = prepare_output(min_time, min_partition, min_time_list)
        end = timer()
        print("Elapsed Time (Greedy-Capacity):",
              end-start, "seconds.")

    json_object = json.dumps(output, indent=5)
    with open("Outputs/" + algorithm + "_output.json", "w") as outfile:
        outfile.write(json_object)
    outfile.close()
    return output


if __name__ == "__main__":
    main(sys.argv[1:])

# UNCOMMENT TO SEE ALL ALGORITHMS IN ACTION
# for algo in POSSIBLE_ALGORITHMS:
#     main(["input.json", algo])

# UNCOMMENT TO SEE SELECTED ALGORITHM IN ACTION
# main(["input.json", "brute-force-capacity"])
