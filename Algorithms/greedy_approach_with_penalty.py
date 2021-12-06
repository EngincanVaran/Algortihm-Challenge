import numpy as np


def calculate_time_for_vehicle(matrix, vehicle_pos, job_pos, penalty):
    if matrix[vehicle_pos][job_pos] == 0:
        return -1
    return matrix[vehicle_pos][job_pos] + penalty


def set_up_v_j_matrix(matrix, vehicles, jobs, number_jobs, visited_jobs):
    vehicle_job_matrix = []
    for vehicle in vehicles:
        temp = [-1 for _ in range(number_jobs)]
        for job in jobs:
            if job["id"] not in visited_jobs:
                temp[job["id"]-1] = calculate_time_for_vehicle(
                    matrix, vehicle["start_index"], job["location_index"], job["service"])
        vehicle_job_matrix.append(temp)
    return np.array(vehicle_job_matrix)


def find_min_time_job(matrix, jobs):
    min_time = 100000000000
    index_v = 0
    index_j = 0
    for v in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[v][j] < min_time and matrix[v][j] > 0:
                min_time = matrix[v][j]
                index_v = v
                index_j = j
    # print("MIN JOB:", jobs[index_j], "Vehicle ID:", index_v+1)
    return index_v, index_j+1, min_time


def change_vehicle_position(vehicles, position, job_position):
    vehicles[position]["start_index"] = job_position
    return vehicles


def print_locations(vehicles, jobs, number_jobs, number_vehicles, visited_jobs):
    line = ["" for _ in range(number_jobs+number_vehicles)]
    for v in vehicles:
        line[v["start_index"]] = "v" + str(v["id"])
    for j in jobs:
        if j["id"] not in visited_jobs:
            line[j["location_index"]] = "j" + str(j["id"])
    print(line)


def greedy_penalty(matrix, jobs, vehicles):
    number_jobs = len(jobs)
    number_vehicle = len(vehicles)

    time_list = [0 for _ in range(number_vehicle)]
    total_time = 0
    partition = [[] for _ in range(number_vehicle)]
    visited_jobs = []

    count = 0
    print("Step:", count)
    print_locations(vehicles, jobs, number_jobs,
                    number_vehicle, visited_jobs)

    vehicle_job_matrix = set_up_v_j_matrix(
        matrix, vehicles, jobs, number_jobs, visited_jobs)
    # print(vehicle_job_matrix)
    while(len(visited_jobs) < number_jobs):
        count += 1
        print("Step:", count)
        vehicle, job, temp_time = find_min_time_job(
            vehicle_job_matrix, jobs)
        total_time += temp_time
        partition[vehicle].append(job)
        time_list[vehicle] += temp_time
        visited_jobs.append(job)
        # print("Visited Jobs:", visited_jobs)

        vehicles = change_vehicle_position(
            vehicles, vehicle, jobs[job-1]["location_index"])
        print_locations(vehicles, jobs, number_jobs,
                        number_vehicle, visited_jobs)

        vehicle_job_matrix = set_up_v_j_matrix(
            matrix, vehicles, jobs, number_jobs, visited_jobs)
        # print(vehicle_job_matrix)

    return total_time, partition, time_list
