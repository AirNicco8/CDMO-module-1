import fileinput
import matplotlib.pyplot as plt
from minizinc import Instance, Model, Solver

#reading the instance
def read_instance(i):
    s= ''
    for line in fileinput.input(files = "instances/ins-{}.txt".format(i)):
        s += line
    return s.splitlines()
        
s = read_instance(4)


#formatting the file
width = int(s[0])
n_rets = int(s[1])


sizes = [i.split() for i in s[-n_rets:]]

for i in range(n_rets):
    for j in range(2):
        sizes[i][j] = int(sizes[i][j])

#load model from file
model = Model("./CP_base.mzn")

#Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")

#Create an instance of the model
instance = Instance(gecode, model)

#Assignment
instance["width"] = width
instance["n_rets"]= n_rets
instance["sizes"] =  sizes


result = instance.solve()

height = result['objective']
positions = result['positions']

print(height,positions)

fig, ax = plt.subplots()

colors = ['tab:blue','tab:orange', 'tab:green', 'tab:red','tab:grey','tab:purple','tab:brown']
for i in range(n_rets):
    ax.broken_barh([(positions[i][0], sizes[i][0])], (positions[i][1], sizes[i][1]), facecolors=colors[i%len(colors)],edgecolors=("black",),linewidths=(1,),)

ax.set_ylim(0, height)
ax.set_xlim(0, width)
ax.set_xticks(range(width+1))
ax.set_yticks(range(height+1))
ax.set_xlabel('width')
ax.set_ylabel('height')

plt.show()






