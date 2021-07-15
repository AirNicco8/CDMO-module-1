from z3 import *
from itertools import combinations


import fileinput
import os

# Input the number of the instance from keyboard
num = input("Please enter the number of the instance:")

# Reading the instance
def read_instance(i):
    s= ''
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "../../instances/ins-{}.txt".format(i))
    for line in fileinput.input(files = filename):
        s += line
    return s.splitlines()
        
s = read_instance(num)

# Formatting the file
width = int(s[0])
n_rets = int(s[1])

# Splitting the list and casting the string to int
sizes = [i.split() for i in s[-n_rets:]]
sizes = [[int(sizes[i][j]) for j in range(2)] for i in range(n_rets)]

# Calculating the max height that the model can reach
max_height = 0
for i in range(n_rets):
    max_height = max_height + sizes[i][1]

# Calculation of the area
area = [sizes[i][0]*sizes[i][1] for i in range(n_rets)]
area.append(0)

###############################SAT MODEL########################################

# Functions
def at_least_one(bool_vars):
    return Or(bool_vars)

def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

def exactly_one(solver, bool_vars):
    solver.add(at_most_one(bool_vars))
    solver.add(at_least_one(bool_vars))

def at_least_n(bool_vars, n):
    pa = BoolVector(bool_vars, n)
    return Or(And(pa))

def at_most_n(bool_vars, n):
    pa = BoolVector(bool_vars, n)
    return Not(And(pa))

def exactly_n(solver, bool_vars, n):
    solver.add(at_most_n(bool_vars, n))
    solver.add(at_least_n(bool_vars, n))

totk = n_rets+1
#variables
p = [[[Bool(f"x_{i}_{j}_{k}") for k in range(totk)] for j in range(max_height)] for i in range(width)]

s = Solver()

# A cell has only one value
for i in range(width):
    for j in range(max_height):
        exactly_one(s, p[i][j])

# A rectangle can be placed only once
for i in range(width):
    for j in range(max_height):
        for k in range(0,totk-1):
            exactly_n(s, p[i][j], area[k])

sol = []
if s.check() == sat:
    m = s.model()
    for i in range(width):
        sol.append([])
        for j in range(max_height):
            for k in range(totk):
                if m.evaluate(p[i][j][k]):
                    sol[i].append(k+1)
else:
    print("Failed to solve")

print(len(sol))
print(sol)