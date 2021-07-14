from z3 import *

import fileinput
import os

#input from keyboard
num = input("Please enter the number of the instance:")

#reading the instance
def read_instance(i):
    s= ''
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "../../instances/ins-{}.txt".format(i))
    for line in fileinput.input(files = filename):
        s += line
    return s.splitlines()
        
s = read_instance(num)

#formatting the file
width = int(s[0])
n_rets = int(s[1])

#splitting the list and casting the string to int
sizes = [i.split() for i in s[-n_rets:]]
sizes = [[int(sizes[i][j]) for j in range(2)] for i in range(n_rets)]

max_height = sum(sizes[:][1])

#variables
p = [[[Bool(f"x_{i}_{j}_{k}") for k in range(n_rets)] for j in range(max_height)] for i in range(width)]

# Create the solver instance
s = Solver()