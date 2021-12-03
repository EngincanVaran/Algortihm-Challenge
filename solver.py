import json
import sys
import numpy as np
from itertools import permutations


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


def calculate_time_for_vehicle(time_matrix, vehicle_sp, job_route, jobs):
    time = 0
    for job in job_route:
        id = jobs[job-1]["id"]
        job_index = jobs[job-1]["location_index"]
        elapsed_time = time_matrix[vehicle_sp][job_index]
        # print("For Job#" + str(id), ":", vehicle_sp,
        #      "-->", job_index, "Time:", elapsed_time)
        vehicle_sp = job_index
        time += elapsed_time
    # print("Total Time", time)
    return time


def parse_perm(perm, number_vehicle):
    partitions = [[] for _ in range(number_vehicle)]

    index = 0
    for i in perm:
        if i == "|":
            index += 1
        else:
            partitions[index].append(i)
    return partitions


def main(argv):
    json_file_name = argv[0]
    try:
        file = open(json_file_name)
    except IOError:
        print("Could not open file!")

    json_data = json.load(file)
    vehicles = json_data["vehicles"]
    jobs = json_data["jobs"]
    time_matrix = np.array(json_data["matrix"])

    number_jobs = len(jobs)
    number_vehicle = len(vehicles)

    temp_jobs = [i for i in range(1, number_jobs+1)]
    delimiter = ["|" for _ in range(number_vehicle-1)]

    perm = list(permutations(temp_jobs + delimiter))

    first_time = True
    min_time = 0
    min_partition = []
    min_time_list = []

    for p in perm:
        partitions = parse_perm(p, number_vehicle)
        totalTime = 0
        time_list = []
        for vehicle_index, partition in enumerate(partitions):
            temp = calculate_time_for_vehicle(
                time_matrix, vehicles[vehicle_index]["start_index"], partition, jobs)
            time_list.append(temp)
            totalTime += temp

        if first_time:
            min_time = totalTime
            first_time = False

        if totalTime < min_time:
            min_time = totalTime
            min_partition = partitions
            min_time_list = time_list

    output = prepare_output(min_time, min_partition, min_time_list)
    json_object = json.dumps(output, indent=4)

    with open("output.json", "w") as outfile:
        outfile.write(json_object)
    outfile.close()


# if __name__ == "__main__":
#     main(sys.argv[1:])

main(["input.json"])
