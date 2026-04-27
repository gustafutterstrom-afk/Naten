import networkx as nx
import numpy as np
from scipy.io import loadmat

B = np.loadtxt('traffic.mat', delimiter=',')
print(B.shape)
le = np.loadtxt('traveltime.mat', delimiter=',')
print(le.shape)
cap = np.loadtxt('capacities.mat', delimiter=',')
#W = np.zeros((B.shape[0], B.shape[0]))
G = nx.DiGraph()
for i in range(B.shape[1]):  
    a = None
    b = None

    for j in range(B.shape[0]): 
        if B[j, i] == 1:
            a = j
        elif B[j, i] == -1:
            b = j

        if a is not None and b is not None:
            #W[a, b] = le[i]
            G.add_edge(a, b, capacity = cap[i], weight=le[i])

#print(W)
#G = nx.DiGraph(W, capacity=cap)
shortestp = nx.shortest_path(G, source=0, target=16)
shortest = nx.shortest_path_length(G, source=0, target=16)
print(shortest)
print(shortestp)

mflow, dict = nx.maximum_flow(G, 0, 16)
print(mflow)