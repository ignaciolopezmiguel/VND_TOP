"""
Find solution to the TSP problem using mlrose.
"""

import mlrose
import numpy as np


def find_best_way(data, path):
    """"
    Reorders a path trying to find the shortest path starting and ending in
    two specific points, which are the first one and the last one of the input
    data.
    Inputs:
        data: array with the coordinates of all the points
        path: list with the points of the path, where each point is referred
              to the data array with the index        
    """
    # Calculate distances between pairs of nodes
    coords_list = data[path,0:2]
    dist_list = []
    for i in range(0,len(coords_list)):
        for j in range(i+1,len(coords_list)):
            dist_list.append([i, j, np.linalg.norm(coords_list[i]-coords_list[j])])
    
    # add dummy node with null distance to the start and end nodes and large
    # distance to the rest of nodes
    max_dist = max([x[2] for x in dist_list])
    dist_list.append([0, len(coords_list), 1e-5])
    dist_list.append([len(coords_list)-1, len(coords_list), 1e-5])
    for i in range(1,len(coords_list)-1):
        dist_list.append([i, len(coords_list), max_dist*1000])
        
    
    # Initialize fitness function object using distances
    fitness_dists = mlrose.TravellingSales(distances = dist_list)
    
    problem_fit = mlrose.TSPOpt(length = len(coords_list)+1, fitness_fn = fitness_dists,
                                maximize=False)
    
    # Solve problem using the simulated annealing algorithm (good and fast solution)
    best_state, best_fitness = \
              mlrose.simulated_annealing(problem_fit, max_attempts=50, 
              init_state = np.array([x for x in range(0,len(coords_list)+1)]),
              random_state = 2)
              
    path_reord = path.copy()
    j = 0
    best_state = best_state.tolist()
    best_state.remove(len(coords_list)) # remove dummy node

    # Reorder the solution so that the first node is the first specified node
    if best_state[best_state.index(0)-1] != len(best_state)-1:
        best_state = [best_state[x] for x in range(len(best_state)-1,-1,-1)]
        
    for i in range(best_state.index(0),best_state.index(0)+len(best_state)):
        path_reord[j] = path[best_state[i%len(best_state)]]
        j += 1
    
    return path_reord
