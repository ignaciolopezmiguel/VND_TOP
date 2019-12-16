"""
Main program

"""

import matplotlib.cm as cm
import ellipse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from initialization import init_sol_greedy_scores
from general import plot_map, total_score, total_distance
from local_search import loc_search_add, loc_search_exch
   
# run "%matplotlib qt" to interact with the graphs

############################# Load data #############################

path = "D:/Master AEPIA/1er año/2. Resolución de problemas con metaheurísticos/4-Trabajo/Instances/top1/p1.4.r.txt"

head = pd.read_csv(path, delimiter=" ", nrows=3, header=None)
# n := number of vertices, P := number of paths, Tmax := available time budget per path
n, P, Tmax = head[1] 
n = int(n)
P = int(P)

#	- The first point is the starting point.
#	- The last point is the ending point.
#	- The Euclidian distance is used.

data = np.loadtxt(path, delimiter="\t", skiprows=3)

#####################################################################


######################### Initial solution ##########################

# plot map with all the points and their values
plt.figure(0)
plot_map(data)

# only the points inside of the ellipse with focis starting point and 
# ending point and a major axis = Tmax can be reached by the paths
f1 = np.array(data[0,0:2])
f2 = np.array(data[-1,0:2])
ellipse.plot_ellipse(f1, f2, Tmax)

# calculate the initial solution by a greedy method (best score first)
best_paths = init_sol_greedy_scores(data, Tmax, n, P)

#Plot the initalpaths
color=iter(cm.rainbow(np.linspace(0,1,len(best_paths)+1)))
for i in best_paths:
    c=next(color)
    plt.plot(data[i, 0],data[i, 1], linestyle="-", color = c, linewidth=3)
    plt.plot(data[0,0],data[0,1],"*", color = "red")
    plt.plot(data[-1,0],data[-1,1],"*", color = "red")

plt.title("Initial score = " + str(total_score(data, best_paths)))

plt.show()

#####################################################################

copy_best_paths = best_paths.copy()

# First improvement strategy is used - the first improvement for each
# neighborhood is taken into account to modify the current solution.

# First neighborhood: one non-assigned point is included into one of
# the paths
# Second to fourth neighborhoods: one, two, or three points from a 
# path are exchanged with one, two, or three, respectively, points
# which are not assigned. In case the path has less points than the
# number of points which should be exchanged, all the points from that
# path are exchanged with the total number of points non-assigned
# (if one path has two points without taking into account the
# first and the last point, and the neighborhood would exchange three
# points, then those two points are exchanged with three non-assigned
# points)

############################ Basic VND ##############################

# Basic VND (B-VND)—return to the first neighborhood on the list when
# an improvement is found.

end = False
temp = best_paths.copy()

while not end:
    end = True
    print("Best paths = " + str(best_paths))
    print("Adding 1 point")
    # local search adding 1 new point and reordering (first neighborhood)
    best_paths = loc_search_add(data, best_paths, n, Tmax)
    if temp != best_paths:
        print("Improvement found adding 1 point")
        end = False
        temp = best_paths.copy()
    else:
        print("No improvement adding 1 point")
        # local search exchanging i new points and reordering (2-4th neighborhoods)
        for i in range(1,4):
            print("Exchanging " + str(i) + " points.")
            best_paths = loc_search_exch(data, best_paths, Tmax, n, i)
            if temp != best_paths:
                print("Improvement found exchanging " + str(i) + " points")
                end = False
                temp = best_paths.copy()
                break # come back to the first neighborhood
            else:
                print("No improvement exchanging " + str(i) + " points")

print("No more possible improvements")
print("Final best paths B-VND = " + str(best_paths))
     
best_bvnd = best_paths.copy()

#####################################################################

best_paths = copy_best_paths.copy()


############################ Pipe VND ###############################

# First improvement strategy
# Pipe VND (P-VND)—continue the search within the same neighborhood.                    
print("Best paths = " + str(best_paths))
end = False
temp = best_paths.copy()

while not end:
    end = True
    # local search adding 1 new point and reordering (first neighborhood)
    print("Adding 1 point")
    best_paths = loc_search_add(data, best_paths, n, Tmax, False)
    if temp != best_paths:
        end = False
        temp = best_paths.copy()
    else:
        print("No improvement adding 1 point")
        # local search exchanging i new points and reordering (2-4th neighborhoods)
        i = 1
        while i < 4:
            print("Exchanging " + str(i) + " points.")
            best_paths = loc_search_exch(data, best_paths, Tmax, n, i, False)
            if temp != best_paths:
                end = False
                temp = best_paths.copy()
            else:
                print("No improvement exchanging " + str(i) + " points")
                i += 1

print("No more possible improvements")
print("Final best paths P-VND = " + str(best_paths))

best_pvnd = best_paths.copy()

#####################################################################

best_paths = copy_best_paths.copy()

############################ Cyclic VND ###############################

# First improvement strategy
# Cyclic VND (C-VND)—resume the search on the next neighborhood from the list.
end = False
while not end:
    end = True
    print("Best paths = " + str(best_paths))
    temp = best_paths.copy()
    
    print("Adding 1 point")
    # local search adding 1 new point and reordering (first neighborhood)
    best_paths = loc_search_add(data, best_paths, n, Tmax)
    if temp != best_paths:
        print("Improvement found adding 1 point")
        end = False
        temp = best_paths.copy()
    else:
        print("No improvement adding 1 point")
    
    # local search exchanging i new points and reordering (2-4th neighborhoods)
    for i in range(1,4):
        print("Exchanging " + str(i) + " points.")
        best_paths = loc_search_exch(data, best_paths, Tmax, n, i)
        if temp != best_paths:
            print("Improvement found exchanging " + str(i) + " points")
            print("Best paths = " + str(best_paths))
            end = False
            temp = best_paths.copy()
        else:
            print("No improvement exchanging " + str(i) + " points")

print("No more possible improvements")
print("Final best paths C-VND = " + str(best_paths))
                    
best_cvnd = best_paths.copy()

#####################################################################


######################## Plot final paths ###########################

list_solutions = [best_bvnd, best_pvnd, best_cvnd]
list_methods = ["B-VND", "P-VND", "C-VND"]

plt.figure(1)
count = 1
for solution in list_solutions:
    
    plt.subplot(1,3,count)
    plot_map(data)
    f1 = np.array(data[0,0:2])
    f2 = np.array(data[-1,0:2])
    
    ellipse.plot_ellipse(f1, f2, Tmax)
    color=iter(cm.rainbow(np.linspace(0,1,len(solution)+1)))
    for i in solution:
        c=next(color)
        plt.plot(data[i, 0],data[i, 1], linestyle="-", color = c, linewidth=3)
        plt.plot(data[0,0],data[0,1],"*", color = "red")
        plt.plot(data[-1,0],data[-1,1],"*", color = "red")
    
    plt.title("Total score " + list_methods[count-1] + " = " + str(total_score(data, solution)))
    
    plt.show()
    
    print("Total score " + list_methods[count-1] + " = " + str(total_score(data, solution)))
    print("Distances " + list_methods[count-1] + " = " + str([total_distance(data[x]) for x in solution]))
    print([(data[x]) for x in solution])
    
    count += 1

#####################################################################