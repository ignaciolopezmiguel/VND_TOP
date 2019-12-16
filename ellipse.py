"""
Plot ellipse of feasible points.
"""

import matplotlib.pyplot as plt
import numpy as np
import math

def plot_ellipse(f1, f2, Tmax):
    """
    Plots the ellipse of foci f1 and f2 where each points verify:
        distance(f1,x) + distance(f2,x) = Tmax
    
    Inputs:
    f1 and f2 := arrays with the coordinates of the foci
    Tmax      := number with the major axis
    
    Example: 
    plot_ellipse(np.array([2,4]),np.array([3,3]),3)
    """
    #Distance between the two foci
    d = np.linalg.norm(f2-f1)  
    
    if Tmax < d:
        raise ValueError("Tmax = " + str(Tmax) + " < d(f1, f2) = " + str(d))
        
    #Angle between the two foci
    theta = math.atan2(f2[1]-f1[1], f2[0]-f1[0])
        
    #Translation matrix
    T = np.array([[1., 0., -(f1[0]+f2[0])/2],
                  [0., 1., -(f1[1]+f2[1])/2],
                  [0., 0.,               1.]])
    #Rotation matrix
    R = np.array([[math.cos(-theta), -math.sin(-theta), 0.],
                  [math.sin(-theta),  math.cos(-theta), 0.],
                  [              0.,                0., 1.]])

    #Points of an ellipse centered in the origin
    x = np.linspace(-Tmax/2, Tmax/2, 1000)
    y_pos = np.sqrt((1/4)*(Tmax**2-d**2) * (1-x**2/((Tmax/2)**2)))
    y_neg = -y_pos
    
    #Transformed the points
    R_inv = np.linalg.inv(R)
    T_inv = np.linalg.inv(T)
    pos_backs = np.array([np.matmul(T_inv,np.matmul(R_inv,np.array([[i[0]],[i[1]],[1.]]))) for i in  zip(x, y_pos)]).reshape(1000,3)
    neg_backs = np.array([np.matmul(T_inv,np.matmul(R_inv,np.array([[i[0]],[i[1]],[1.]]))) for i in  zip(x, y_neg)]).reshape(1000,3)
    
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot(f1[0], f1[1], "*", color="blue")
    plt.plot(f2[0], f2[1], "*", color="blue")
    plt.plot(pos_backs[:,0],pos_backs[:,1], color="blue")
    plt.plot(neg_backs[:,0],neg_backs[:,1], color="blue")
    