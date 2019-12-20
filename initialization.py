"""
Find an initialization for the problem.
"""

import pandas as pd
import numpy as np

from general import distance, distance_no_start_exit

def init_sol_greedy_scores(data, Tmax, n, P, distances=None):
    """
    Returns an initial solution (list of paths) following this logic:
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
    
    Inputs:
        data: array with the coordinates of all the points
        Tmax: integer with the maximum distance for each path
        n: index of the end point of the path (last index of data)
        P: integer with the number of paths
    
    """

    if distances is not None:
        dist_st = np.array([x[2] for x in distances if (x[0]==0) and (x[1]!=n-1)])
        dist_fin = np.array([x[2] for x in distances if (x[1]==n-1) and (x[0]!=0)])
        pd_Tot_Dist = pd.DataFrame({"TotDist": dist_st + dist_fin, 
                                    "Score": data[1:-1, 2][0]})
    else:
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
            
            if distance_no_start_exit(data, init_points[j], n, distances) <= Tmax: # path found
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
                other_paths[i].append(new_point)
                if distance_no_start_exit(data, other_paths[i], n, distances) > Tmax: #not possible in this path
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