import networkx as nx
from scipy.io import loadmat
import numpy as np
import cvxpy as cp
### Excercise a)####
B = np.loadtxt('Handin2/Handin2/traffic.mat',delimiter=',')
l = np.loadtxt('Handin2/Handin2/traveltime.mat', delimiter=',')
cap = np.loadtxt('Handin2/Handin2/capacities.mat')
flow = l = np.loadtxt('Handin2/Handin2/flow.mat', delimiter=',')
#print(B.shape) # 17,28
#print(cap.shape[0]) # 28 rader
print(B.shape[0])# 17 rader
#print(B.shape[1]) # 28 colonner
#print(l.shape[0]) #28 lång
print(flow.shape[0]) # 28

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
shortestP = nx.shortest_path(G,source=0,target =16, weight='weight')
print(f"the shortest path:{shortest}")
print(f'The path:{shortestP}') # Nollidexering 
#### Execercise b)
maxF, dict = nx.maximum_flow(G, 0,16)

print(f'Maxflow - the sum of the first split:{maxF}')

#### Execercise c)###
v = np.matmul(B,flow)
print(v) # external positivt innebär inflow (-1 i B matrisen är in)

#### Execercise d)###
v = np.zeros(B.shape[0])
v[0]=20000
v[-1]=-20000
print(v)


f = cp.Variable(B.shape[1])


# --- model ---
x = cp.multiply(f, 1 / cap)
lc= cp.multiply(l,cap)
print(x)
print(lc)
inv_term = cp.inv_pos(1 - x)

# FIXED objective (DCP valid)
objective = cp.Minimize(
    cp.sum(cp.multiply(lc,inv_term)-lc)
)
constraints = [
    B @ f == v,
    f >= 0,
    f <= 0.99 * cap
]

prob = cp.Problem(objective, constraints)

print(prob.solve(solver="SCS"))
print("f =", f.value)
