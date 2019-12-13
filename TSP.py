# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 21:53:19 2019

"""

import mlrose
import numpy as np



def find_best_way(data, path):
    
    coords_list = data[path,0:2]
    dist_list = []
    for i in range(0,len(coords_list)):
        for j in range(i+1,len(coords_list)):
            if (i == 0) and (j == len(coords_list)-1):
                dist_list.append([i, j, 1e-10]) # para que se una el punto de salida con el de llegada
            else:
                dist_list.append([i, j, np.linalg.norm(coords_list[i]-coords_list[j])])
    
            
    # Initialize fitness function object using distances
    fitness_dists = mlrose.TravellingSales(distances = dist_list)
    
    problem_fit = mlrose.TSPOpt(length = len(coords_list), fitness_fn = fitness_dists,
                                maximize=False)
    
    # Solve problem using the genetic algorithm
    best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob = 0.2, 
    					      max_attempts = 50, random_state = 2)
    
    
    path_reord = path.copy()
    j = 0
    best_state = best_state.tolist()
    if best_state[best_state.index(0)-1] != len(best_state)-1:
        best_state = [best_state[x] for x in range(len(best_state)-1,-1,-1)]
        
    for i in range(best_state.index(0),best_state.index(0)+len(best_state)):
        path_reord[j] = path[best_state[i%len(best_state)]]
        j += 1

    return path_reord


