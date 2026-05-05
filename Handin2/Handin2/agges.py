import networkx as nx
import numpy as np
from scipy.io import loadmat
import cvxpy as cv

B = np.loadtxt('traffic.mat', delimiter=',')
print(B.shape)
le = np.loadtxt('traveltime.mat', delimiter=',')
print(le.shape)
cap = np.loadtxt('capacities.mat', delimiter=',')
flo = np.loadtxt('flow.mat', delimiter=',')
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
shortest = nx.shortest_path_length(G, source=0, target=16) #a
#print(shortest)
#print(shortestp)

mflow, dict = nx.maximum_flow(G, 0, 16) #b
print(mflow)

mu = B@flo
print(mu) #c


v = np.zeros(B.shape[0])
v[0] = 22447
v[-1] = -22447
fe = cv.Variable(B.shape[1])
# 2. Define Constraints
constraints = [
    B @ fe == v,
    fe >= 0,
    fe <= cap
]

# SAFE convex expression
cost = cv.sum(
    cv.multiply(
        le * cap,
        cv.inv_pos(1 - cv.multiply(fe, 1 / cap)) - 1
    )
)

objective = cv.Minimize(cost)

problem = cv.Problem(objective, constraints)

print(problem.solve())
print(problem.status)


