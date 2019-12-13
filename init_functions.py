# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 17:04:24 2019

@author: Ignacio David López Miguel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# run "%matplotlib qt" to interact with the graphs

def plot_map(data):
    plt.scatter(data[:,0], data[:,1], 
            s=(data[:,2])*25)
    ax = plt.gca()
    
    plt.xlabel("x")
    plt.ylabel("y")
    
    
    #make a legend:
    pws = [0, 5, 10, 15]
    for pw in pws:
        plt.scatter([], [], s=pw*25, c="k",label=str(pw))
    
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(h[1:], l[1:], labelspacing=1, title="value", borderpad=1, 
                frameon=True, framealpha=1, edgecolor="k", facecolor="w")
    
    plt.show()

def distance(x1,x2):
    return np.array([np.linalg.norm(x) for x in x1 - x2])

def distance_no_start_exit(data, path, n):
    path.insert(0,0)
    path.append(n-1)
    tot_dist = total_distance(data[path])
    path.pop(0)
    path.pop(-1)
    return tot_dist


def total_distance(points):
    return sum(distance(points[0:-1,0:2], points[1:,0:2]))

def total_score(data, x):
    score = 0
    for i in x:
        score += sum(data[i,2])
    return score

def init_sol_greedy_scores(data, Tmax, n, P):
    """
    1. select points inside of the ellipse.
    2. order the points according to their score
    3. take the node with the best score and assign it to the 
       first path (in case of same score, the closest node is taken)
    4. take the next best node and assign it to the next path, ...
    5. the following nodes are assigned to the first path where it is possible,
       i.e. the distance of the path is smaller than Tmax
    6. if one node cannot be assigned, it is stored for later
    7. once all the first P paths are completed, i.e. by adding one node to any
       of the paths, the distance is bigger than Tmax, we proceed to assign the
       rest of the nodes
    8. take the best node and add it to a new path
    9. take the next best node and try to assign it to this new path. If it is
       not possible, create a new path and assign this node to this new path
    10.take the next best node and proceed similarly
    11.take the P best paths according to their score among the new paths and
       the first paths
    12.plot in dashed line the paths created the last, in continuos, small
       line the created paths in the beginning, in continuos, thick line the
       selected ones
    """
    f1 = np.array(data[0,0:2])
    f2 = np.array(data[-1,0:2])
    
    dist_st = distance(data[1:-1, 0:2], f1)
    dist_fin = distance(data[1:-1, 0:2], f2)
    
    pd_Tot_Dist = pd.DataFrame({"TotDist": dist_st + dist_fin, 
                                "Score": data[1:-1, 2]})
    
    #Select points inside of the ellipse and order by score
    pd_Tot_Dist = pd_Tot_Dist[pd_Tot_Dist["TotDist"]<Tmax].sort_values(
        by=["Score","TotDist"], ascending=[False,True])
    
    # Fill in the first P paths
    init_points = [[] for i in range(0,P)]
    not_assigned = []
    while not pd_Tot_Dist.empty:
        # Select the next best new point
        new_point = pd_Tot_Dist.index[0] + 1
        pd_Tot_Dist = pd_Tot_Dist.drop(pd_Tot_Dist.index[0])
        
        #Try to find a path where this point can be included
        for j in range(0,P):
            init_points[j].append(new_point)
            
            if distance_no_start_exit(data, init_points[j], n) <= Tmax: # path found
                break
            else: # try with the next path
                init_points[j].pop(-1)
            if j == P-1: # path not found
                not_assigned.append(new_point)
    
    #Include the first and last node to all the paths
    for j in range(0,P):
        init_points[j].insert(0,0)
        init_points[j].append(n-1)
        
    #Assign the rest of the nodes to new paths
    other_paths = [[]]
    if len(not_assigned) != 0:
        #Assign the first node to a new path
        new_point = not_assigned[0]
        other_paths[0] = [new_point]
        not_assigned.pop(0)
    
        while len(not_assigned) != 0:
            #Try to assign the new point to any of the new paths
            new_point = not_assigned[0]
            not_assigned.pop(0)
            for i in range(0,len(other_paths)):
                
                if distance_no_start_exit(data, other_paths[i], n) > Tmax: #not possible in this path
                    other_paths[i].pop(-1)
                    if i == len(other_paths)-1: #path not found, create new one
                        other_paths.append([new_point])
                else: #path found
                    break
            
        #Include the first and last node to all the paths        
        for j in range(0,len(other_paths)):
            other_paths[j].insert(0,0)
            other_paths[j].append(n-1)
           
     
        # Select the P best scores
        scores = []
        scores = [[sum(data[i,2]),i] for i in init_points]
        scores_notass = [[sum(data[i,2]),i] for i in other_paths]
        scores.extend(scores_notass)
        scores.sort(reverse=True)
        # If the number of created paths is smaller than the number of necessary
        # paths, P, create new paths that go from the start to the end node
        # directly
        if len(scores)<P:
            final_points = [i[1] for i in scores[0:len(scores)]]
            for i in range(len(scores),P):
                final_points.append([0, n-1])
        else:
            final_points = [i[1] for i in scores[0:int(P)]]
    else:
        final_points = init_points
        
    return final_points