"""
General functions that will be used across different parts of the project.
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_map(data):
    """
    Plots the map of points given an array data where the first column is
    the coordinate x, the second one is the coordinate y, and the third one
    is the score linked to that point.
    """
    plt.scatter(data[:,0], data[:,1], 
            s=(data[:,2])*25)
    
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

def distance(array_points,x):
    """
    Returns the euclidean distance for each point of an array (array_points) 
    to a given point (x).
    Example:
        distance(np.array([[3,4]]),[4,5])
    """
    return np.array([np.linalg.norm(x) for x in array_points - x])

def distance_no_start_exit(data, path, n):
    """
    Returns the distance of a path where the start and ending point are not
    included in the list of points.
    Inputs:
        data: array with the coordinates of all the points
        path: list with the points of the path, where each point is referred
              to the data array with the index
        n: integer with index of the end point of the path (last index of data)
    """
    path.insert(0,0)
    path.append(n-1)
    tot_dist = total_distance(data[path])
    path.pop(0)
    path.pop(-1)
    return tot_dist


def total_distance(points):
    """
    Returns the total distance of a path given a list of points (coordinates
    x and y).
    Inputs:
        points: list with the points of the path, where each point is a list of
                two elements (x,y)
    Example:
        total_distance(np.array([[1,2],[3,4],[5,5]])) #=np.sqrt(4+4)+np.sqrt(4+1)
    """
    return sum(distance(points[0:-1,0:2], points[1:,0:2]))

def total_score(data, path):
    """
    Returns the total score of a path (start and end point should be given).
    Inputs:
        data: array with the coordinates of all the points
        path: list with the points of the path, where each point is referred
              to the data array with the index
    """
    score = 0
    for i in path:
        score += sum(data[i,2])
    return score