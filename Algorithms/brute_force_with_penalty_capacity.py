from itertools import permutations
import copy as copy

BIG_NUMBER = 9999999999999999


def calculate_time_for_vehicle(time_matrix, vehicle, job_route, jobs):
    time = 0
    for job in job_route:
        if vehicle["capacity"][0] >= jobs[job-1]["delivery"][0]:
            vehicle_sp = vehicle["start_index"]
            job_index = jobs[job-1]["location_index"]
            elapsed_time = time_matrix[vehicle_sp][job_index] + \
                jobs[job-1]["service"]
            # print("For Job#" + str(id), ":", vehicle_sp,
            #      "-->", job_index, "Time:", elapsed_time)
            vehicle["start_index"] = job_index
            vehicle["capacity"][0] -= jobs[job-1]["delivery"][0]
            time += elapsed_time
        else:
            return BIG_NUMBER
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


def brute_force_it_capacity(matrix, jobs, vehicles):
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
        total_time = 0
        time_list = []
        for vehicle_index, partition in enumerate(partitions):
            temp_vehicle = copy.deepcopy(vehicles[vehicle_index])
            temp = calculate_time_for_vehicle(
                matrix, temp_vehicle, partition, jobs)
            time_list.append(temp)
            total_time += temp

        if first_time:
            min_time = total_time
            first_time = False

        if total_time < min_time:
            min_time = total_time
            min_partition = partitions
            min_time_list = time_list

    return min_time, min_partition, min_time_list
