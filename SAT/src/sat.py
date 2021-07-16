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
# area = [sizes[i][0]*sizes[i][1] for i in range(n_rets)]
# space_occupied = sum(area)
# free_space = (max_height*width) - space_occupied
# area.append(free_space)
# print(area)
rangesx, rangesy = [], []
rangesx = [(width-sizes[i][0]+1) for n in range(n_rets)]
ragnesy = [(width-sizes[i][1]+1) for n in range(n_rets)]
###############################SAT MODEL########################################

# Functions
def at_least_one(bool_vars):
    return Or(bool_vars)

def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

def exactly_one(solver, bool_vars):
    solver.add(at_most_one(bool_vars))
    solver.add(at_least_one(bool_vars))

# def exactly_n(literals, n):
#     c = []
#     for pairs in combinations(literals, n+1):
#         c += [Not(And(pairs))]
#     # At least
#     for pairs in combinations(literals, n):
#         c += [Or(pairs)]
#     return And(c)


#variables
px = [[Bool(f"x_{n}_{i}") for i in range(len(rangesx))] for n in range(n_rets)]
py = [[Bool(f"y_{n}_{i}") for i in range(len(rangesy))] for n in range(n_rets)]

s = Solver()

# Order Constraint 
# For the x
for i in range(n_rets):
    ord = []
    for j in range(len(rangesx)-1):
        ord += [Or(Not(px[i][j]), px[i][j+1])]
    s.add(ord)

# For the y
for i in range(n_rets):
    ordi = []
    for j in range(len(rangesy)-1):
        ordi += [Or(Not(py[i][j]), py[i][j+1])]
    s.add(ordi)

# A cell has only one value
# for i in range(width):
#     for j in range(max_height):
#         exactly_one(s, p[i][j])

# there can be only a number of variables true for each rectangle
# This number is equal to the area of each rectangle
# for k in range(totk):
#     g = []
#     for i in range(width):
#         for j in range(max_height):
#             g += [p[i][j][k]]
#     s.add(exactly_n(g, area[k]))

# sol = []
# if s.check() == sat:
#     m = s.model()
#     for i in range(width):
#         sol.append([])
#         for j in range(max_height):
#             for k in range(totk):
#                 if m.evaluate(p[i][j][k]):
#                     sol[i].append(k)
# else:
#     print("Failed to solve")

sol = []
if s.check() == sat:
    m = s.model()
    print(m)
else:
    print("Failed to solve")

