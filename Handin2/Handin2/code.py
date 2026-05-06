import networkx as nx
from scipy.io import loadmat
import numpy as np
import cvxpy as cp
import sympy as sp 
### Excercise a)####
B = np.loadtxt('Handin2/Handin2/traffic.mat',delimiter=',')
l = np.loadtxt('Handin2/Handin2/traveltime.mat', delimiter=',')
cap = np.loadtxt('Handin2/Handin2/capacities.mat')
flow = np.loadtxt('Handin2/Handin2/flow.mat', delimiter=',')
#print(B.shape) # 17,28
#print(cap.shape[0]) # 28 rader
#print(B.shape[0])# 17 rader
#print(B.shape[1]) # 28 colonner
#print(l.shape[0]) #28 lång
#print(flow.shape[0]) # 28

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

shortest = nx.shortest_path_length(G,source=0,target=16, weight='weight')
shortestP = nx.shortest_path(G,source=0,target =16, weight='weight')
print(f"the shortest path:{shortest}")
print(f'The path:{shortestP}') # Nollidexering 

#### Execercise b)#####
maxF, dict = nx.maximum_flow(G, 0,16)
print(f'Maxflow - the sum of the first split:{maxF}')

#### Execercise c)#####
mu = np.matmul(B,flow)
print(mu) # external positivt innebär inflow (-1 i B matrisen är in)

#### Execercise d)######
v = np.zeros(B.shape[0]) # External flow vecotor
v[0] = mu[0]
v[-1] = -mu[0]
fe = cp.Variable(B.shape[1])

# Constraints
constraints = [
    B @ fe == v, # External flow 
    fe >= 0,
    fe <= cap
]
# expression
cost = cp.sum(
    cp.multiply(
        l * cap,
        cp.inv_pos(1 - cp.multiply(fe, 1 / cap)) - 1
    )
)

objective_soc = cp.Minimize(cost)
problem_soc = cp.Problem(objective_soc, constraints)
print("Social optimum")
print(problem_soc.solve())
print("Social optimum flow")
print(fe.value)

### e)######
fe2 = cp.Variable(B.shape[1])
cost_war = cp.sum(cp.multiply(cp.multiply(-cap,l),cp.log(1-fe2/cap)))
objective_war = cp.Minimize(cost_war)
constraints = [
    B @ fe2 == v,
    fe2 >= 0,
    fe2 <= cap
]
problem_war = cp.Problem(objective_war, constraints)
print("Wardop optimum")
print(problem_war.solve())
print("Wardrop flow-values")
print(fe2.value)
fe_star=fe.value

##f)#####
fe3 =cp.Variable(B.shape[1])
cost_war_toll = cp.sum(cp.multiply(cp.multiply(-cap,l),cp.log(1-fe3/cap))+cp.multiply(fe3,cp.multiply(l,fe_star))/cp.multiply(cap,cp.square(1-fe_star/cap)) )
objective_war_toll = cp.Minimize(cost_war_toll)
constraints = [
    B @ fe3 == v,
    fe3 >= 0,
    fe3 <= cap
]
problem_war_toll = cp.Problem(objective_war_toll, constraints)
print("Wardrop with tolls")
print(problem_war_toll.solve())
print("Wardrop flow with tolls")
print(fe3.value)
              
## g###
fe4 =cp.Variable(B.shape[1])
cost_system = cp.sum(
    cp.multiply(
        l * cap,
        cp.inv_pos(1 - cp.multiply(fe4, 1 / cap)) - 1
    )-cp.multiply(fe4,l)
)

objective_soc_2 = cp.Minimize(cost_system)
constraints = [
    B @ fe4 == v,
    fe4 >= 0,
    fe4 <= cap
]
problem_soc_2 = cp.Problem(objective_soc_2, constraints)
print(problem_soc_2.solve())
print("Social optimum:")
print(fe4.value)
fe_star2=fe4.value

fe5 =cp.Variable(B.shape[1])
cost2_war_toll = cp.sum(cp.multiply(cp.multiply(-cap,l),cp.log(1-fe5/cap))+cp.multiply(fe5,cp.multiply(l,fe_star2))/cp.multiply(cap,cp.square(1-fe_star2/cap))-cp.multiply(fe5,l) )
objective_war_toll2 = cp.Minimize(cost2_war_toll)
constraints = [
    B @ fe5 == v,
    fe5 >= 0,
    fe5 <= cap
]
problem_war_toll2 = cp.Problem(objective_war_toll2, constraints)
print("with tolls")
print(problem_war_toll2.solve())
print(fe5.value)