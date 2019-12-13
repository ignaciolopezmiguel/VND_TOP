"""
Main program

"""

import matplotlib.cm as cm
import ellipse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from init_functions import plot_map, init_sol_greedy_scores, total_score, total_distance
from local_search import loc_search_add
   

path = "D:/Master AEPIA/1er año/2. Resolución de problemas con metaheurísticos/4-Trabajo/Instances/top1/p1.2.c.txt"

head = pd.read_csv(path, delimiter=" ", nrows=3, header=None)
n, P, Tmax = head[1] # n := number of vertices, P := number of paths, Tmax := available time budget per path
n = int(n)
#P = int(P)
P = 3
Tmax = 15
Tmax = int(Tmax)
#
#	- The first point is the starting point.
#	- The last point is the ending point.
#	- The Euclidian distance is used.

plt.figure(0)
data = np.loadtxt(path, delimiter="\t", skiprows=3)

plot_map(data)
f1 = np.array(data[0,0:2])
f2 = np.array(data[-1,0:2])

ellipse.plot_ellipse(f1, f2, Tmax)

best_paths = init_sol_greedy_scores(data, Tmax, n, P)

#Plot the finally selected paths
color=iter(cm.rainbow(np.linspace(0,1,len(best_paths)+1)))
for i in best_paths:
    c=next(color)
    plt.plot(data[i, 0],data[i, 1], linestyle="-", color = c, linewidth=3)
    plt.plot(data[0,0],data[0,1],"*", color = "red")
    plt.plot(data[-1,0],data[-1,1],"*", color = "red")

plt.show()


print(best_paths)

# Local search adding 1 new point and reordering (first neighborhood) #
best_paths = loc_search_add(data, best_paths, n, Tmax)

#Plot the finally selected paths
plt.figure(1)
plot_map(data)
f1 = np.array(data[0,0:2])
f2 = np.array(data[-1,0:2])

ellipse.plot_ellipse(f1, f2, Tmax)
color=iter(cm.rainbow(np.linspace(0,1,len(best_paths)+1)))
for i in best_paths:
    c=next(color)
    plt.plot(data[i, 0],data[i, 1], linestyle="-", color = c, linewidth=3)
    plt.plot(data[0,0],data[0,1],"*", color = "red")
    plt.plot(data[-1,0],data[-1,1],"*", color = "red")

plt.show()

print("Total score = " + str(total_score(data, best_paths)))
print("Distances = " + str([total_distance(data[x]) for x in best_paths]))



