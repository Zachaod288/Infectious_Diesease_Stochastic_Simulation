import matplotlib
matplotlib.use('TKAgg')
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D

def SIRS_lat(size):  # Initialise a random lattice of S, I, and R 
    lat = np.zeros((size,size), dtype = float)
    for i in range(size):
        for j in range(size):
            r=random.random()
            if(r<0.333): lat[i,j] = 0    #  0 = Susceptable
            if(r >= 0.333 and r <=0.666): 
                lat[i,j] = 1    #  1 = Infected  
            if (r> 0.666): lat[i,j] = 2    #2 = Recovered
    return lat

def SIRS_probs(lat, size, p1, p2, p3, a, b): # Update rules for the SIRS model
    infected = 0
    swap = 0
    if lat[a][b] == 0 and swap == 0:   #If point is Susceptable    (Purple)
        if lat[(a+1)%size][b] == 1 or lat[(a-1)%size][b] == 1 or lat[a][(b+1)%size] == 1 or lat[a][(b-1)%size] == 1: #If a point next to S is I periodically 
            if np.random.rand() < p1:
                lat[a][b] = 1
                swap+=1
                #latnew[i,j] = 1
                #IF ISSUES WITH THE INFECTED NUMBER, INFECTED +=1 HERE POTENTIALLY

    if lat[a][b] == 1 and swap == 0:    # If point is Infected (Blue)
        infected += 1
        if np.random.rand() < p2:
            lat[a][b] = 2
            #latnew[i,j] = 2
            swap+=1
    if lat[a][b] == 2 and swap == 0:  #If point is recoverd   (yellow)
        if np.random.rand() < p3:
            lat[a][b] = 0
            #latnew[i,j] = 0 
            #infected -= 1
            swap+=1
    return lat, infected       # CHANGE TO LAT OR LATNEW ACCORDINGLY 



def main():

    # Take the initial inputs from the user
    size = int(input("Give the size of the square lattice: "))
    sweep = size**2

    p1 = float(input("p1 = "))
    p2 = float(input("p2 = "))
    p3 = float(input("p3 = "))

    lat = SIRS_lat(size) #Initialise lattice to fill randomly with S, I, and R
    for k in range(sweep*100):   #100 sweeps
        ran = np.linspace(0,size-1, size) 
        a = int(random.choice(ran))   
        b = int(random.choice(ran))

        info = SIRS_probs(lat, size, p1, p2, p3, a, b) # Return the new lattice after looking at one point
        lat = info[0]  
        
        if(k%sweep == 0 ):
            f=open('SIRS.dat','w')
            for i in range(size):
                for j in range(size):
                    f.write('%d %d %lf\n'%(i,j,lat[i,j]))
            f.close()
            #      show animation
            plt.cla()
            im=plt.imshow(lat, animated=True)
            plt.draw()
            plt.pause(0.0001)
    
    return

main()