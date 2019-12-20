"""
Functions needed to perform local searches.
"""

from TSP import find_best_way
import numpy as np
from general import distance, distance_no_start_exit, total_score
import pandas as pd


def exchange(list1, list2, el1, el2):
    """
    Exchange elements from list1 to list2. The elements from list1 that go
    to list2 are the ones in the positions listed in the list el1. Viceversa
    for the elements of list2 going to list1 with el2.
    """
    return [list1[i] for i in range(0,len(list1)) if i not in el1] + \
    [list2[i] for i in range(0,len(list2)) if i in el2]

def combinations(list1, list2, num):
    """
    Returns a list with all the possible combinations of num elements that can
    be exchanged from list1 to list2. If the length of list1 is less than num,
    all the elements from list1 are exchanged by num elements of list2.
    num is ranged from 1 to 3.
    """
    output = []
    if num == 1:
      for i in range(0,len(list1)):
          for j in range(0,len(list2)):
              output.append([[i],[j]])
            
    elif num == 2:
        if len(list1)>=2:
            for i in range(0,len(list1)):
                for j in range(i+1, len(list1)):
                    for k in range(0, len(list2)):
                        for m in range(k+1, len(list2)):
                            output.append([[i,j],[k,m]])
        else:
            for k in range(0, len(list2)):
                for m in range(k+1, len(list2)):
                    output.append([[0],[k,m]])
                        
    elif num == 3:
        if len(list1)>=3:
            for i in range(0,len(list1)):
                for j in range(i+1, len(list1)):
                    for k in range(j+1, len(list1)):
                        for m in range(0, len(list2)):
                            for n in range(m+1, len(list2)):
                                for p in range(n+1, len(list2)):
                                    output.append([[i,j,k],[m,n,p]])
        else:
            if len(list1)==2:
                temp = [0,1]
            else:
                temp = [0]
            for m in range(0, len(list2)):
                for n in range(m+1, len(list2)):
                    for p in range(n+1, len(list2)):
                        output.append([temp,[m,n,p]])
    return output

def loc_search_add(data, paths, n, Tmax, first=True, distances=None):
    """
    Local search adding 1 new point and reordering.
    Returns a list of paths after trying to insert one new element into one
    path. 
    Inputs:
        data: array with the coordinates of all the points
        paths: list of the paths, where each path is a list of points
        n: integer with index of the end point of the path (last index of data)
        Tmax: integer with the maximum distance for each path
        first=True: If first==False, if there is a possible improvement, the 
             algorithm includes this improvement into the solution and 
             continues searching again in the path where the improvement was 
             made and goes on with the next paths.
    """    
    
    # Calculate distance to the start and end points

    if distances is not None:
        dist_st = np.array([x[2] for x in distances if (x[0]==0) and (x[1]!=n-1)])
        dist_fin = np.array([x[2] for x in distances if (x[1]==n-1) and (x[0]!=0)])
        df_Tot_Dist = pd.DataFrame({"TotDist": dist_st + dist_fin, 
                                    "Score": data[1:-1, 2].tolist()})
    else:
        f1 = np.array(data[0,0:2])
        f2 = np.array(data[-1,0:2])
        
        dist_st = distance(data[1:-1, 0:2], f1)
        dist_fin = distance(data[1:-1, 0:2], f2)
        
        df_Tot_Dist = pd.DataFrame({"TotDist": dist_st + dist_fin, 
                                    "Score": data[1:-1, 2]})
    
    # Select points inside of the ellipse and order by score
    df_Tot_Dist = df_Tot_Dist[df_Tot_Dist["TotDist"]<Tmax].sort_values(
            by=["Score","TotDist"], ascending=[False,True])
    
    # Filter by non-assigned points
    flat_list = [item for sublist in paths for item in sublist]
    not_assigned = [x for x in df_Tot_Dist.index+1 if x not in flat_list]
    
    df_Tot_Dist = df_Tot_Dist[df_Tot_Dist.index.isin([x-1 for x in not_assigned])]
    
    k = 0
    while k < len(paths): # loop over paths
        path = paths[k]
        path = path[1:-1] # remove the first and last element

        for i in range(0,len(df_Tot_Dist)): # loop over all the non-assigned points
            path.insert(0,df_Tot_Dist.index[i]+1)

            path_best = find_best_way(data,[0]+path+[n-1],distances)

            if distance_no_start_exit(data, path_best[1:-1], n, distances) <= Tmax:
                # remove newly assigned point from the list of non-asssigned points
                df_Tot_Dist = df_Tot_Dist[df_Tot_Dist.index != df_Tot_Dist.index[i]]
                paths[k] = path_best

                if first:
                    return paths        
                else: # useful for P-VND
                    # continue search in the same path but with the new values.
                    # The previous paths are not touched and it will also go on
                    # with the next paths.
                    # k is not modified to stay in the same path
                    print("Improvement found adding 1 point. Continue searching")
                    print("Best paths = " + str(paths))
                    path = path_best[1:-1]
                    k -= 1

                    break
            else:
                path.remove(df_Tot_Dist.index[i]+1)
        k += 1
            
    return paths

 
def loc_search_exch(data, paths, Tmax, n, num, first=True, distances=None):
    """
    Local search exchanging num new points with num points of one path and 
    reordering.
    Returns a list of paths after trying to exchange k elements from a path
    with k non-assigned nodes. k ranges from 1 to 3. If the length of one path
    is less than k (excluding start and end point), all the elements from that 
    path are exchanged by k non-assigned nodes.
    Inputs:
        data: array with the coordinates of all the points
        paths: list of the paths, where each path is a list of points
        n: integer with index of the end point of the path (last index of data)
        Tmax: integer with the maximum distance for each path
        first=True: If first==False, if there is a possible improvement, the 
             algorithm includes this improvement into the solution and 
             continues searching again in the path where the improvement was 
             made and goes on with the next paths.
    """  
    
    # Calculate distance to the start and end points
    if distances is not None:
        dist_st = np.array([x[2] for x in distances if (x[0]==0) and (x[1]!=n-1)])
        dist_fin = np.array([x[2] for x in distances if (x[1]==n-1) and (x[0]!=0)])
        df_Tot_Dist_all = pd.DataFrame({"TotDist": dist_st + dist_fin, 
                                    "Score": data[1:-1, 2].tolist()})
    else:
        f1 = np.array(data[0,0:2])
        f2 = np.array(data[-1,0:2])
        
        dist_st = distance(data[1:-1, 0:2], f1)
        dist_fin = distance(data[1:-1, 0:2], f2)
        
        df_Tot_Dist_all = pd.DataFrame({"TotDist": dist_st + dist_fin, 
                                    "Score": data[1:-1, 2]})
    
    #Select points inside of the ellipse and order by score
    df_Tot_Dist = df_Tot_Dist_all[df_Tot_Dist_all["TotDist"]<Tmax].sort_values(
            by=["Score","TotDist"], ascending=[False,True])
    
    # create DataFrame with non-assigned points
    flat_list = [item for sublist in paths for item in sublist]
    not_assigned = [x for x in df_Tot_Dist.index+1 if x not in flat_list]
    df_Tot_Dist = df_Tot_Dist[df_Tot_Dist.index.isin([x-1 for x in not_assigned])]
    
    # algorithm to find possible exchanges
    k = 0
    improved = False
    while k < len(paths): # loop over paths
        path = paths[k]
        orig_score = total_score(data, [path])
        path = path[1:-1] # remove the first and last element
        combs = combinations(path,df_Tot_Dist.index,num)

        for comb in combs:

            # exchange elements if the new path has a higher score
            newpath = [0]+exchange(path, df_Tot_Dist.index+1,comb[0],comb[1])+[n-1]

            if orig_score >= total_score(data, [newpath]):
                continue
            # re-order the path
            newpath = find_best_way(data,newpath,distances)

            if (newpath[0] != 0) or (newpath[-1] != n-1): # in case the TSP does not work properly
                newpath = [0]+exchange(path, df_Tot_Dist.index+1,comb[0],comb[1])+[n-1]
            
            if (distance_no_start_exit(data, newpath[1:-1], n, distances) <= Tmax):
                # assign new path and leave all the loops
                paths[k] = newpath
                
                if first:
                    return paths
                else:
                    print("Improvement found exchanging " + str(num) + " points. Continue searching")
                    print("Best paths = " + str(paths))
                    path = newpath[1:-1]
                    
                    # update lists
                    df_Tot_Dist_all = pd.DataFrame({"TotDist": dist_st + dist_fin, 
                                "Score": data[1:-1, 2]})
                    df_Tot_Dist = df_Tot_Dist_all[df_Tot_Dist_all["TotDist"]<Tmax].sort_values(
                            by=["Score","TotDist"], ascending=[False,True])
                    flat_list = [item for sublist in paths for item in sublist]
                    not_assigned = [x for x in df_Tot_Dist.index+1 if x not in flat_list]
                    df_Tot_Dist = df_Tot_Dist[df_Tot_Dist.index.isin([x-1 for x in not_assigned])]
                    
                    # we start searching in the same path so we need to keep
                    # k equal to its previous value
                    k -= 1
                    improved = True
                    break
        k += 1
        if k == len(paths):
            if (not first) and improved:
                print("No more improvement exchanging " + str(num) + " points.")
            break
    return paths
    