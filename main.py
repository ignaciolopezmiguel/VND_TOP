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
from VND import b_vnd, p_vnd, c_vnd
from os import listdir
from os.path import isfile, join
import time
   
# run "%matplotlib qt" to interact with the graphs

def solve_TOP(path, plot=False, verbose=0):
    """
    Runs the three algorithms B-VND, P-VND, and C-VND in a given instance.
    Inputs:
        path: where the instance is located
        plot: True if plots want to be displayed
        verbose: 0 if no messages during execution, 1 if a few messages,
                 and 2 or more for all the message
    Outputs:
        list with the following components:
            list_solutions: list of lists with the points for each path for
                    each algorithm (ordered by B-VND, P-VND and C-VND)
            total_scores: list with the scores for each algorithm 
                    (ordered by B-VND, P-VND and C-VND)
            total_distances: list with the distances of each path for each 
                    algorithm (ordered by B-VND, P-VND and C-VND)
            n: number of points of the instance
            Tmax: time budget or maximum distance
            times: list with the times of execution for each algorithm
                    (ordered by B-VND, P-VND and C-VND)
    """
    ############################# Load data #############################
    
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
    if plot:
        plt.figure(0)
        plot_map(data)
    
    # only the points inside of the ellipse with focis starting point and 
    # ending point and a major axis = Tmax can be reached by the paths
    if plot:
        f1 = np.array(data[0,0:2])
        f2 = np.array(data[-1,0:2])
        ellipse.plot_ellipse(f1, f2, Tmax)
    
    # calculate the initial solution by a greedy method (best score first)
    best_paths = init_sol_greedy_scores(data, Tmax, n, P)
    
    #Plot the initalpaths
    if plot:
        color=iter(cm.rainbow(np.linspace(0,1,len(best_paths)+1)))
        for i in best_paths:
            c=next(color)
            plt.plot(data[i, 0],data[i, 1], linestyle="-", color = c, linewidth=3)
            plt.plot(data[0,0],data[0,1],"*", color = "red")
            plt.plot(data[-1,0],data[-1,1],"*", color = "red")
        
        plt.title("Initial score = " + str(total_score(data, best_paths)))
        
        plt.show()
    
    #####################################################################
    
    ######################### Get solutions #############################

    start_time = time.time()    
    best_bvnd = b_vnd(data, best_paths.copy(), Tmax, n, verbose)
    time_bvnd = time.time() - start_time
    
    
    start_time = time.time()     
    best_pvnd = p_vnd(data, best_paths.copy(), Tmax, n, verbose)    
    time_pvnd = time.time() - start_time
    
    
    start_time = time.time()
    best_cvnd = c_vnd(data, best_paths.copy(), Tmax, n, verbose)
    time_cvnd = time.time() - start_time
    
    #####################################################################
    
    
    ######################## Plot final paths ###########################
    
    list_solutions = [best_bvnd, best_pvnd, best_cvnd]
    list_methods = ["B-VND", "P-VND", "C-VND"]
    times = [time_bvnd, time_pvnd, time_cvnd]
    
    if plot:
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
            print("Distances " + list_methods[count-1] + " = " + str([total_distance(data, x) for x in solution]))
            
            count += 1
            
    total_scores = [total_score(data, solution) for solution in list_solutions]
    total_distances = [[total_distance(data, x) for x in solution] for solution in list_solutions]
        
    return list_solutions, total_scores, total_distances, n, Tmax, times
    #####################################################################
    

# Path to the 7 TOP instances downloaded from https://www.mech.kuleuven.be/en/cib/op
path_instances = "D:/Master AEPIA/1er año/2. Resolución de problemas con metaheurísticos/4-Trabajo/Instances/"


# Create a DataFrame with a summary of all the tests. It is divided into
# different loops so that each loop can be run in a different kernel
summary = pd.DataFrame(columns=["File",
                        "n",
                        "Tmax",
                        "Score B-VND",
                        "Time B-VND",
                        "Score P-VND",
                        "Time P-VND",
                        "Score C-VND",
                        "Time C-VND"])

verbose = 2  #to get information during the execution
plots = False #no plots during the execution
    
path_top1 = path_instances + "TOP1"
files_top1 = [f for f in listdir(path_top1) if isfile(join(path_top1, f))]

for file in files_top1:
    temp = solve_TOP(path_top1 + "/" + file, plot=False, verbose=verbose)
    summary = summary.append({'File': file, 'n': temp[3], 'Tmax': temp[4], 
                    "Score B-VND": temp[1][0], "Time B-VND": temp[5][0], 
                    "Score P-VND": temp[1][1], "Time P-VND": temp[5][1], 
                    "Score C-VND": temp[1][2], "Time C-VND": temp[5][2]},
                    ignore_index=True)
    print(summary)
    print("-------------------------------------------------------------")



path_top2 = path_instances + "TOP2"
files_top2 = [f for f in listdir(path_top2) if isfile(join(path_top2, f))]
    
for file in files_top2:
    temp = solve_TOP(path_top2 + "/" + file, plot=False, verbose=verbose)
    summary = summary.append({'File': file, 'n': temp[3], 'Tmax': temp[4], 
                    "Score B-VND": temp[1][0], "Time B-VND": temp[5][0], 
                    "Score P-VND": temp[1][1], "Time P-VND": temp[5][1], 
                    "Score C-VND": temp[1][2], "Time C-VND": temp[5][2]},
                    ignore_index=True)
    print(summary)
    print("-------------------------------------------------------------")



path_top3 = path_instances + "TOP3"
files_top3 = [f for f in listdir(path_top3) if isfile(join(path_top3, f))]

for file in files_top3:
    temp = solve_TOP(path_top3 + "/" + file, plot=False, verbose=verbose)
    summary = summary.append({'File': file, 'n': temp[3], 'Tmax': temp[4], 
                    "Score B-VND": temp[1][0], "Time B-VND": temp[5][0], 
                    "Score P-VND": temp[1][1], "Time P-VND": temp[5][1], 
                    "Score C-VND": temp[1][2], "Time C-VND": temp[5][2]},
                    ignore_index=True)
    print(summary)
    print("-------------------------------------------------------------")
    
    

path_top4 = path_instances + "TOP4"
files_top4 = [f for f in listdir(path_top4) if isfile(join(path_top4, f))]

for file in files_top4:
    temp = solve_TOP(path_top4 + "/" + file, plot=False, verbose=verbose)
    summary = summary.append({'File': file, 'n': temp[3], 'Tmax': temp[4], 
                    "Score B-VND": temp[1][0], "Time B-VND": temp[5][0], 
                    "Score P-VND": temp[1][1], "Time P-VND": temp[5][1], 
                    "Score C-VND": temp[1][2], "Time C-VND": temp[5][2]},
                    ignore_index=True)
    print(summary)
    print("-------------------------------------------------------------")
    
    
path_top5 = path_instances + "TOP5"
files_top5 = [f for f in listdir(path_top5) if isfile(join(path_top5, f))]

for file in files_top5:
    temp = solve_TOP(path_top5 + "/" + file, plot=False, verbose=verbose)
    summary = summary.append({'File': file, 'n': temp[3], 'Tmax': temp[4], 
                    "Score B-VND": temp[1][0], "Time B-VND": temp[5][0], 
                    "Score P-VND": temp[1][1], "Time P-VND": temp[5][1], 
                    "Score C-VND": temp[1][2], "Time C-VND": temp[5][2]},
                    ignore_index=True)
    print(summary)
    print("-------------------------------------------------------------")
    
    
path_top6 = path_instances + "TOP6"
files_top6 = [f for f in listdir(path_top6) if isfile(join(path_top6, f))]

for file in files_top6:
    temp = solve_TOP(path_top6 + "/" + file, plot=False, verbose=verbose)
    summary = summary.append({'File': file, 'n': temp[3], 'Tmax': temp[4], 
                    "Score B-VND": temp[1][0], "Time B-VND": temp[5][0], 
                    "Score P-VND": temp[1][1], "Time P-VND": temp[5][1], 
                    "Score C-VND": temp[1][2], "Time C-VND": temp[5][2]},
                    ignore_index=True)
    print(summary)
    print("-------------------------------------------------------------")


path_top7 = path_instances + "TOP7"
files_top7 = [f for f in listdir(path_top7) if isfile(join(path_top7, f))]

for file in files_top7:
    temp = solve_TOP(path_top7 + "/" + file, plot=False, verbose=verbose)
    summary = summary.append({'File': file, 'n': temp[3], 'Tmax': temp[4], 
                    "Score B-VND": temp[1][0], "Time B-VND": temp[5][0], 
                    "Score P-VND": temp[1][1], "Time P-VND": temp[5][1], 
                    "Score C-VND": temp[1][2], "Time C-VND": temp[5][2]},
                    ignore_index=True)
    print(summary)
    print("-------------------------------------------------------------")
    



summary = summary.round({"Time B-VND":2, "Time P-VND":2, "Time C-VND":2})
summary[["Score B-VND", "Score P-VND", "Score C-VND"]] = summary[["Score B-VND", "Score P-VND", "Score C-VND"]].astype(int)
