from z3 import *
import matplotlib.pyplot as plt
from itertools import combinations

import time
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

    ax.set_ylim(0, height+1)
    ax.set_xlim(0, width)
    ax.set_xticks(range(width+1))
    ax.set_yticks(range(height+1))
    ax.set_xlabel('width')
    ax.set_ylabel('height')

    plt.show()

# Output the result in txt file
def write_solution(num, width, height, n_rets, sizes, positions):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "../out/out−{}.txt".format(num))
    f= open(filename,"w+")
    f.write("{} {}\n".format(width, height))
    f.write("{}\n".format(n_rets))
    for i in range(len(sizes)):
        f.write("{} {} {} {}\n".format(sizes[i][0], sizes[i][1], positions[i][0], positions[i][1]))
    f.close()

# Formatting the file
width = int(s[0])
n_rets = int(s[1])

# Splitting the list and casting the string to int
sizes = [i.split() for i in s[-n_rets:]]
sizes = [[int(sizes[i][j]) for j in range(2)] for i in range(n_rets)]

# Calculating the max height that the model can reach
max_h = 0
for i in range(n_rets):
    max_h = max_h + sizes[i][1]

min_h = max([sizes[i][1] for i in range(n_rets)])

############################### SAT MODEL ######################################

# Functions
def at_least_one(bool_vars):
    return Or(bool_vars)

def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

def exactly_one(solver, bool_vars):
    solver.add(at_most_one(bool_vars))
    solver.add(at_least_one(bool_vars))
    
def vlsi(s, height):
    # Variables
    p = [[[Bool(f"x_{i}_{j}_{n}") for n in range((2*n_rets)+1)] for j in range(height)] for i in range(width)]

    # A cell has only one value
    for i in range(width):
        for j in range(height):
            exactly_one(s, p[i][j])

    for n in range(n_rets):
        # A rectangle has only one position
        exactly_one(s, [p[i][j][n] for i in range(width) for j in range(height)])

        # Position should respect width and the height
        s.add(at_least_one([p[i][j][n] for i in range(width-sizes[n][0]+1) for j in range(height-sizes[n][1]+1)]))

    # Solving overlapping
    for n in range(n_rets):
        for i in range(width-sizes[n][0]+1):
            for j in range(height-sizes[n][1]+1):
                for k in range(i, i + sizes[n][0]):
                    for u in range(j, j + sizes[n][1]):
                        if(k != i or u != j):
                            s.add(Implies(p[i][j][n], p[k][u][n+n_rets]))

    sol = []

    if s.check() == sat:
        m = s.model()
        for i in range(width):
            sol.append([])
            for j in range(height):
                for k in range((2*n_rets)+1):
                    if m.evaluate(p[i][j][k]):
                        sol[i].append(k)
    elif s.reason_unknown() == "timeout":
        print("Solver timeout")
    else:
        print("Failed to solve at height {}".format(height))
    return sol


start = time.time()
for i in range(min_h, max_h):
    # Solver
    s = Solver()

    # Time limit 5 minutes
    times = 300000 # in milliseconds
    s.set(timeout=times)

    m = vlsi(s, i)

    
    if m :
        positions = []
        for n in range(n_rets):
            for i in range(len(m)):
                for j in range(len(m[0])):
                    if m[i][j] == n:
                        positions.append([i,j])
        plot_solution(width, n_rets, sizes, positions, i)
        write_solution(num, width, i+1, n_rets, sizes, positions)
        break
end = time.time()
print("Time elapsed: {} seconds".format(end - start))

