import networkx as nx
from scipy.io import loadmat
import numpy as np
### Excercise a)####
B = np.loadtxt('traffic.mat',delimiter=',')
l = np.loadtxt('traveltime.mat', delimiter=',')
cap = np.loadtxt('capacities.mat')
#print(B.shape) # 17,28
#print(cap.shape[0]) # 28 rader
#print(B.shape[0])# 17 rader
#print(B.shape[1]) # 28 colonner
#print(l.shape[0]) #28 lång

G = nx.Graph()
for j in range (B.shape[1]):
    a = None
    b= None
    for i in range (B.shape[0]):
        if B[i][j] == 1:
           a=i
        if B[i][j] == -1:
            b=i
        if a is not None and b is not None:
            G.add_edge(a,b,weight=l[j], capacity = cap[j])


shortest = nx.shortest_path_length(G,source=0,target=16)
shortestP = nx.shortest_path(G,source=0,target =16)
print(f"the shortest path:{shortest}")
print(f'The path:{shortestP}') # Nollidexering 
#### Execercise b)
maxF, dict = nx.maximum_flow(G, 0,16)

print(f'Maxflow - the sum of the first split:{maxF}')





