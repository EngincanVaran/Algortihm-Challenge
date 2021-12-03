import json
import sys
import numpy as np


class Vehicle:
    def __init__(self, id, start_index, capacity):
        self.id = id
        self.start_index = start_index
        self.capacity = capacity

    def __repr__(self):
        capacity_list = []
        for cap in self.capacity:
            capacity_list.append(cap)
        return "Vehicle ID: " + str(self.id) + " Start Index: " + str(self.start_index) + \
            " Capacity: " + str(capacity_list)


class Job:
    def __init__(self, id, location_index, delivery, service):
        self.id = id
        self.location_index = location_index
        self.delivery = delivery
        self.service = service

    def __repr__(self):
        delivery_list = []
        for delivery in self.delivery:
            delivery_list.append(delivery)
        return "Job ID: " + str(self.id) + " Location Index: " + str(self.location_index) \
            + " Service: " + str(self.service) + \
            " Delivery:" + str(delivery_list)


def read_json(file_name):
    vehicles = []
    matrix = []
    jobs = []
    road = []
    try:
        file = open(file_name)
    except IOError:
        print("Could not open file!")
        return True, matrix, vehicles, jobs, road
    else:
        json_data = json.load(file)

        for vehicle in json_data["vehicles"]:
            vehicles.append(
                Vehicle(
                    vehicle["id"],
                    vehicle["start_index"],
                    vehicle["capacity"]))

        for job in json_data["jobs"]:
            jobs.append(
                Job(
                    job["id"],
                    job["location_index"],
                    job["delivery"],
                    job["service"]))

        for row in json_data["matrix"]:
            matrix.append(row)

        road = ["*" for _ in range(len(matrix[0]))]
        for vehicle in vehicles:
            road[vehicle.start_index] = "V" + str(vehicle.id)

        for job in jobs:
            road[job.location_index] = "J" + str(job.id)

        return False, np.array(matrix), vehicles, jobs, road


def main(argv):
    json_file_name = argv[0]
    is_failed, time_matrix, vehicles, jobs, road = read_json(
        json_file_name)
    if is_failed:
        print("Invalid File! Exiting...")

    print("Time Matrix:\n", time_matrix)
    print("Vehicles:\n", vehicles)
    print("Jobs\n", jobs)
    print("Road\n", road)


if __name__ == "__main__":
    main(sys.argv[1:])
