import json
import sys
import numpy as np
from timeit import default_timer as timer
from brute_force import brute_force_it
from greedy_approach import greedy


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
    return result


def main(argv):
    if(len(argv) != 2):
        print("Invalid Arguments")
        return
    json_file_name = argv[0]
    algorithm = argv[1]
    try:
        file = open(json_file_name)
    except IOError:
        print("Could not open file!")
        return

    if algorithm != "brute-force" and algorithm != "greedy":
        print("Invalid Algorithm")
        return

    json_data = json.load(file)
    vehicles = json_data["vehicles"]
    jobs = json_data["jobs"]
    time_matrix = np.array(json_data["matrix"])

    print("Time Matrix")
    print(time_matrix)
    print(2*"\n")

    if algorithm == "brute-force":
        start = timer()
        min_time, min_partition, min_time_list = brute_force_it(
            matrix=time_matrix,
            jobs=jobs,
            vehicles=vehicles)
        output = prepare_output(min_time, min_partition, min_time_list)
        end = timer()
        print("Elapsed Time (Brute-Force):", end-start, "seconds.")

    elif algorithm == "greedy":
        start = timer()
        # min_time, min_partition, min_time_list =
        min_time, min_partition, min_time_list = greedy(
            matrix=time_matrix,
            jobs=jobs,
            vehicles=vehicles)
        output = prepare_output(min_time, min_partition, min_time_list)
        end = timer()
        print("Elapsed Time (Greedy Approach):", end-start, "seconds.")

    json_object = json.dumps(output, indent=4)
    with open(algorithm + "_output.json", "w") as outfile:
        outfile.write(json_object)
    outfile.close()
    return output


if __name__ == "__main__":
    main(sys.argv[1:])

# main(["input.json", "greedy"])
