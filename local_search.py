# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 00:22:13 2019

@author: Ignacio David lópez Miguel
"""

from TSP import find_best_way
import numpy as np
from init_functions import distance, distance_no_start_exit
import pandas as pd


def loc_search_add(data, paths, n, Tmax):
    """
    Local search adding 1 new point and reordering (first neighborhood)
    """    
    fin=False
    while not fin:
        f1 = np.array(data[0,0:2])
        f2 = np.array(data[-1,0:2])
        
        dist_st = distance(data[1:-1, 0:2], f1)
        dist_fin = distance(data[1:-1, 0:2], f2)
        
        df_Tot_Dist = pd.DataFrame({"TotDist": dist_st + dist_fin, 
                                    "Score": data[1:-1, 2]})
        
        #Select points inside of the ellipse and order by score
        df_Tot_Dist = df_Tot_Dist[df_Tot_Dist["TotDist"]<Tmax].sort_values(
                by=["Score","TotDist"], ascending=[False,True])
        
        flat_list = [item for sublist in paths for item in sublist]
        not_assigned = [x for x in df_Tot_Dist.index+1 if x not in flat_list]
        
        df_Tot_Dist = df_Tot_Dist[df_Tot_Dist.index.isin([x-1 for x in not_assigned])]
        
        found = False
        for k in range(0,len(paths)): # loop over paths
            path = paths[k]
            path = path[1:-1] # remove the first and last element
            for i in range(0,len(df_Tot_Dist)): # loop over all the non-assigned points
                path.insert(0,df_Tot_Dist.index[i]+1)

                path_best = find_best_way(data,[0]+path+[n-1])

                if distance_no_start_exit(data, path_best[1:-1], n) <= Tmax:
                    print("Improvement found")
                    df_Tot_Dist = df_Tot_Dist[df_Tot_Dist.index != i]
                    paths[k] = path_best
                    found = True
                    break            
                else:
                    path.remove(df_Tot_Dist.index[i]+1)
                
                if found:
                    break
            if found:
                break
            if k == len(paths)-1:
                fin = True
                print("No improvement")
    return paths





