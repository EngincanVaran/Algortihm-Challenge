from itertools import permutations


def calculate_time_for_vehicle(time_matrix, vehicle_sp, job_route, jobs):
    time = 0
    for job in job_route:
        job_index = jobs[job-1]["location_index"]
        elapsed_time = time_matrix[vehicle_sp][job_index] + \
            jobs[job-1]["service"]
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


def brute_force_it_penalty(matrix, jobs, vehicles):
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
            temp = calculate_time_for_vehicle(
                matrix, vehicles[vehicle_index]["start_index"], partition, jobs)
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
