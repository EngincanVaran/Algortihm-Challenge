# Project

The codes inside this repo serve 2 things:
- Solving a VRP (and CVRP) problem with Brute-Force & Greedy Approach
- REST Service with FASTAPI in order to solve the VRP and CVRP by utilizing VROOM

## Usage

There are 2 main questions:

#### ALGORITHM Question

solver.py has 6 algorithms to approach the VRP.
- Brute-Force (Basic, Penalty Only, Capacity & Penalty)
- Greedy (Basic, Penalty Only, Capacity & Penalty)

#### REST Question
Please take a look at the guide for [vroom-express](https://github.com/VROOM-Project/vroom-express) to run the vroom in your machine.
- VROOM-express listen http://localhost:3000

Use following command to start the application
```bash
uvicorn controller:app --reload 
```

## Test
In order to run the test please install [pytest](https://docs.pytest.org/en/6.2.x/)
```bash
pip install pytest
```
and run the command
```bash
pip install pytest
```

OR

install [coverage.py](https://coverage.readthedocs.io/en/6.2/) with
```bash
pip install coverage
```
and run the command
```bash
coverage run -m pytest
```

## Authors
Engincan Varan 
For contact:
- engincanvaran@gmail.com
- evaran@sabanciuniv.edu