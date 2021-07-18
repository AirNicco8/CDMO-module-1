from z3 import *
import matplotlib.pyplot as plt
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

# Method used to plot the solution
def plot_solution(width, n_rets, sizes, positions, height):
    print("Sizes: ",sizes)
    print("Positions: ", positions)

    fig, ax = plt.subplots()

    colors = ['tab:blue','tab:orange', 'tab:green', 'tab:red','tab:grey','tab:purple','tab:brown', 'black', 'yellow', 'gold']
    for i in range(n_rets):
        ax.broken_barh([(positions[i][0], sizes[i][0])], (positions[i][1], sizes[i][1]), facecolors=colors[i%len(colors)],edgecolors=("black",),linewidths=(1,),)

    ax.set_ylim(0, height)
    ax.set_xlim(0, width)
    ax.set_xticks(range(width+1))
    ax.set_yticks(range(height+1))
    ax.set_xlabel('width')
    ax.set_ylabel('height')

    plt.show()

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

###############################SAT MODEL########################################

# Functions
def at_least_one(bool_vars):
    return Or(bool_vars)

def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

def exactly_one(solver, bool_vars):
    solver.add(at_most_one(bool_vars))
    solver.add(at_least_one(bool_vars))

# Variables
p = [[[Bool(f"x_{i}_{j}_{n}") for n in range(n_rets+1)] for j in range(max_height)] for i in range(width)]

s = Solver()

# A cell has only one value
for i in range(width):
    for j in range(max_height):
        exactly_one(s, p[i][j])

# Position should respect width
for n in range(n_rets):
    s.add(at_least_one([p[i][j][n] for i in range(width-sizes[n][0]+1) for j in range(max_height)]))

# Position should respect height
for n in range(n_rets):
    s.add(at_least_one([p[i][j][n] for i in range(width) for j in range(max_height-sizes[n][1]+1)]))

# A rectangle has only one position
for n in range(n_rets):
     exactly_one(s, [p[i][j][n] for i in range(width) for j in range(max_height)])

# Solving overlapping


# 5 minutes time limit
time = 300000 # in milliseconds
s.set(timeout=time)

sol = []
if s.check() == sat:
    m = s.model()
    for i in range(width):
        sol.append([])
        for j in range(max_height):
            for k in range(n_rets+1):
                if m.evaluate(p[i][j][k]):
                    sol[i].append(k)
elif s.reason_unknown() == "timeout":
    print("Solver timeout")
else:
    print("Failed to solve")
    exit(0)

positions = []
for i in range(len(sol)):
    for j in range(len(sol[0])):
        if sol[i][j] != n_rets:
            positions.append([i,j])


plot_solution(width, n_rets, sizes, positions, max_height)



