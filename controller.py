from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from solver import main as solve_vrp
import requests
import json

# Just learned FastAPI :)

app = FastAPI()


class Output(BaseModel):
    total_delivery_duration: int
    routes: dict


class SolverInput(BaseModel):
    datasource: str
    algorithm: str

# uvicorn app:app --reload


def parse_response(data, vehicles):
    data = json.loads(data)
    # print(data)
    result = {}
    result["total_delivery_duration"] = 0
    result["routes"] = {}
    # in case any vehicle is not used add the vehicle as default values
    for v in range(1, len(vehicles)+1):
        result["routes"][v] = {}
        result["routes"][v]["delivery_duration"] = 0
        result["routes"][v]["routes"] = []

    result["total_delivery_duration"] = data["summary"]["cost"]
    result["total_delivery_duration"] += data["summary"]["service"]

    for vdata in data["routes"]:
        vehicle_id = vdata["vehicle"]
        duration = vdata["cost"] + vdata["service"]
        routes = []
        steps = vdata["steps"]
        for step in steps[1:-1]:
            routes.append(step["id"])
        result["routes"][vehicle_id]["delivery_duration"] = duration
        result["routes"][vehicle_id]["routes"] = routes
    return result


def send_to_vroom(data):
    # forward input to vroom server
    URL = "http://localhost:3000"
    response = requests.post(URL, json=data)
    if response.status_code == 200:
        vehicles = data["vehicles"]
        response = parse_response(response.text, vehicles)
        return 200, response
    return response.status_code, response.text


@app.post("/solver")
async def solver(request: SolverInput):
    # Custom Implemented CRP Solver (brute / greedy)
    if request.datasource != "input.json":
        raise HTTPException(status_code=400, detail="Datasource Not Found")

    elif request.algorithm != "brute-force" and request.algorithm != "greedy":
        raise HTTPException(status_code=400, detail="Invalid Algorithm")

    else:
        json_object = solve_vrp([request.datasource, request.algorithm])
        return json_object

# First of all we need to run the vroom-express in our local
# vroom-express guide = https://github.com/VROOM-Project/vroom-express
# After running the vroom-express it will listen "http://localhost:3000"
# Then we can get the request from the client and parse it to vroom likings
# After getting the response from vroom server, parse it to our wanted output style

# POST Req to http://127.0.0.1:8000/vroom with the input.json


@ app.post("/vroom")
async def vroom(request: Request):
    # Assumed the inputs will be as fine as possible
    # Otherwise vroom server will already give the error
    status_code, response = send_to_vroom(await request.json())
    return JSONResponse(response, status_code)
