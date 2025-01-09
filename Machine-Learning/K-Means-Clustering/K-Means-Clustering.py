import pandas as pd
import numpy as np
from collections import Counter

output_file_name = "K-Means-Clustering-Output.txt"
output_file_handler = open(output_file_name, 'w')

US = pd.read_csv("USArrests.csv").to_numpy()
# murder per 100K
# asssult per 100K
# percent urban population
# rape per 100K

USm = np.array(US[:,1:5]).astype(float) # scaling requires a matrix

USsc = (USm - np.mean(USm, axis=0))/np.std(USm, axis=0)
# scale each attribute to have mean 0 and std dev 1

# a function to compute the sqaured euclidean distance between
# two vectors x and y.
def distance(x, y):
    return np.linalg.norm(x-y)
    # to be completed


# a function to compute the centroid of a cluster.
# X is a matrix that contains the cluster,
# with rows as observations and (numeric) columns as attributes.
def centroid(X):
    return np.mean(X, axis=0)
    # to be completed


# a single iteration of kmeans.
# X is a matrix of observations with m rows and n columns
# k is the number of clusters
def kmeans1(X, k):
    m = X.shape[0]
    n = X.shape[1]
    if k > m:
        print("number of clusters ", k, " > number of observations ", m, sep='')


    clusters0 = np.random.randint(0,k, size=m)  # random initial assignment
    clusters = np.zeros(m) # will hold the cluster assignments
    
    ii = 0
    while True:
        # compute the cluster centroids
        c = np.zeros((k, n))
        for i in range(k):
            c[i,:] = centroid(X[clusters0 == i,:])

        # assign each observation to the nearest centroid
        for i in range(m):
            clusters[i] = 0  # initially assign observation to cluster 0
            best = distance(X[i,:], c[0,:])
            for j in range(1, k):
                candidate = distance(X[i,:], c[j,:])
                if candidate < best:  # assign to cluster j if closer
                    best = candidate
                    clusters[i] = j
                
            
        if all(clusters == clusters0):
            break # when the clusters stop changing
        
        for index, number in enumerate(clusters):
            clusters0[index] = number

        ii += 1
        if ii % 10 == 0:
            print("iteration ", ii, file=output_file_handler)
        
    
    ncl = len(Counter(clusters))
    if ncl != k:
        # it's possible that k-means will produce a solution with less than k clusters.
        print("clustering solution contains ", str(ncl), " < ", str(k), " clusters.")
    return clusters


# a function compute the value of the kmeans objective
# function, the sum of the within-cluster distances.
# X is the matrix of observations.
# k is the number of clusters.
# cl is the clustering solution.
def objective(X, k, cl):
    c = np.zeros((k, X.shape[1]))
    for i in range(k):
        c[i,:] = centroid(X[cl == i,:])
    sum = 0
    for i in range(cl.shape[0]):
        sum += distance(X[i,:], cl[i])
    return sum

# driver function for kmeans.
# X is the (scaled) matrix of observations.
# k is the number of clusters.
# niter is the number of times to run the k-means algorithm.
# the best of the niter candidate solutions is returned.
def kmeans(X, k, niter=50):
    curr_cl = kmeans1(X, k)
    min = float(objective(X, k, curr_cl))
    final_cl = curr_cl
    for i in range(niter-1):
        curr_cl = kmeans1(X, k)
        curr_obj = float(objective(X, k, curr_cl))
        if min > curr_obj:
            min = curr_obj
            final_cl = curr_cl
    return final_cl

k = 4
cl = kmeans(USsc, k);    # call kmeans driver function
score = objective(USsc, k, cl)   # the objective function of the best solution found
cldict = Counter(cl)    # use countmap() to see the number of obs in each cluster
print(cldict, file=output_file_handler)
c = np.zeros((k, USsc.shape[1]))
for i in range(k):
    c[i,:] = centroid(USsc[cl == i,:])
print(c, file=output_file_handler)
print(score, file=output_file_handler)


# obtain information from the clustering to solution to provide
# a qualitative description of each of the four clusters of states.

output_file_handler.close()