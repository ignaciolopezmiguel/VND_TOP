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


from local_search import loc_search_add, loc_search_exch


############################ Basic VND ##############################

# Basic VND (B-VND)—return to the first neighborhood on the list when
# an improvement is found.

def b_vnd(data, best_paths, Tmax, n, verbose=0, first=True):
    """
    
    """
    if verbose >1:
        print("Best paths = " + str(best_paths))
        
    end = False
    temp = best_paths.copy()
        
    while not end:
        end = True
        if verbose > 1:
            print("Adding 1 point")
        # local search adding 1 new point and reordering (first neighborhood)
        best_paths = loc_search_add(data, best_paths, n, Tmax, first=first)
        if temp != best_paths:
            if verbose > 1:
                print("Improvement found adding 1 point")
                print("Best paths = " + str(best_paths))
            end = False
            temp = best_paths.copy()
        else:
            if verbose > 1:
                print("No improvement adding 1 point")
            # local search exchanging i new points and reordering (2-4th neighborhoods)
            for i in range(1,4):
                if verbose > 1:
                    print("Exchanging " + str(i) + " points.")
                best_paths = loc_search_exch(data, best_paths, Tmax, n, i, first=first)
                if temp != best_paths:
                    if verbose > 1:
                        print("Improvement found exchanging " + str(i) + " points")
                        print("Best paths = " + str(best_paths))
                    end = False
                    temp = best_paths.copy()
                    break # come back to the first neighborhood
                else:
                    if verbose > 1:
                        print("No improvement exchanging " + str(i) + " points")
    if verbose > 0:
        print("No more possible improvements")
        print("Final best paths B-VND = " + str(best_paths))    
    
    return best_paths


#####################################################################



############################ Pipe VND ###############################

# First improvement strategy
# Pipe VND (P-VND)—continue the search within the same neighborhood.         
    
def p_vnd(data, best_paths, Tmax, n, verbose=0, first=True):
    """
    
    """
    if verbose > 1:
        print("Best paths = " + str(best_paths))
        
    end = False
    temp = best_paths.copy()
    
    while not end:

        end = True
        # local search adding 1 new point and reordering (first neighborhood)
        if verbose > 1:
            print("Adding 1 point")
        best_paths = loc_search_add(data, best_paths, n, Tmax, first=first)
        if temp != best_paths:
            if verbose > 1:
                print("Improvement found adding 1 point")
                print("Best paths = " + str(best_paths))
            end = False
            temp = best_paths.copy()
        else:
            if verbose > 1:
                print("No improvement adding 1 point")
            # local search exchanging i new points and reordering (2-4th neighborhoods)
            i = 1
            while i < 4:
                if verbose > 1:
                    print("Exchanging " + str(i) + " points.")
                best_paths = loc_search_exch(data, best_paths, Tmax, n, i, first=first)
                if temp != best_paths:
                    end = False
                    temp = best_paths.copy()
                    if verbose > 1:
                        print("Improvement found exchanging " + str(i) + " points")
                        print("Best paths = " + str(best_paths))
                    # no change of i to continue in the same neighborhood
                else:
                    if verbose > 1:
                        print("No improvement exchanging " + str(i) + " points")
                    i += 1
    if verbose > 0:
        print("No more possible improvements")
        print("Final best paths P-VND = " + str(best_paths))

    return best_paths

#####################################################################



############################ Cyclic VND ###############################

# First improvement strategy
# Cyclic VND (C-VND)—resume the search on the next neighborhood from the list.
    
def c_vnd(data, best_paths, Tmax, n, verbose=0, first=True):
    """
    
    """
    if verbose > 1:
        print("Best paths = " + str(best_paths))
        
    end = False
    while not end:

        end = True
        temp = best_paths.copy()
        
        if verbose > 1:
            print("Adding 1 point")
        # local search adding 1 new point and reordering (first neighborhood)
        best_paths = loc_search_add(data, best_paths, n, Tmax, first=first)
        if temp != best_paths:
            if verbose > 1:
                print("Improvement found adding 1 point")
                print("Best paths = " + str(best_paths))
            end = False
            temp = best_paths.copy()
        else:
            if verbose > 1:
                print("No improvement adding 1 point")
        
        # local search exchanging i new points and reordering (2-4th neighborhoods)
        for i in range(1,4):
            if verbose > 1:
                print("Exchanging " + str(i) + " points.")
            best_paths = loc_search_exch(data, best_paths, Tmax, n, i, first=first)
            if temp != best_paths:
                if verbose > 1:
                    print("Improvement found exchanging " + str(i) + " points")
                    print("Best paths = " + str(best_paths))
                end = False
                temp = best_paths.copy()
            else:
                if verbose > 1:
                    print("No improvement exchanging " + str(i) + " points")
    if verbose > 0:
        print("No more possible improvements")
        print("Final best paths C-VND = " + str(best_paths))
    
    return best_paths