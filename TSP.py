"""
Problem Definition:
The traveling salesman problem (TSP) consists of a salesman and a set of cities. The salesman has to
visit each one of the cities starting from a certain one (e.g. the hometown) and returning to the
same city. The challenge of the problem ius that the traveling salesman wants to minimize the total
length of the trip. (https://www.csd.uoc.gr/~hy583/papers/ch11.pdf)

This problem uses the network example from problem 9.3-1 of the Introduction to Operations Research, 7th edition
textbook by Hillier and Lieberman. The table below summarizes the distances between cities, where a dash indicates
that there is no road directly connecting these two towns without going through any other towns. The starting city
(hometown) is "O".

        Town    O   A   B   C   D   E   T
        O       --  40  60  50  --  --  --
        A       40  --  10  --  70  --  --
        B       60  10  --  20  55  40  --
        C       50  --  20  --  --  50  --
        D       --  70  55  --  --  10  60
        E       --  40  --  50  10  --  80
        T       --  --  --  --  60  80  --

Copyright @author: S. Lei
"""

import pandas as pd
from docplex.mp.model import Model

# Initialize the problem data
from util import export_soln_to_csv

# User defined parameters
input_file_name = 'data_arc.csv'
model_name = 'TSP'
output_file_name1 = model_name+'_arc'
output_file_name2 = model_name+'_city'

df = pd.read_csv(input_file_name)
cities = set(df['destination'])
edges = list((t.origin, t.destination) for t in df.itertuples())
distance = dict([((t.origin, t.destination), t.distance) for t in df.itertuples()])

m = Model(model_name)

x = m.binary_var_dict(edges, name='x')
u = m.continuous_var_dict(cities, name='u')

# objective function
m.minimize(m.sum(distance[e] * x[e] for e in edges))

# Constraint 1: each city must be entered once
for c in cities:
    if c != 'T':
        m.add_constraint(m.sum(x[(i, j)] for i, j in edges if i == c) == 1, ctname='city_out_' + c)

# Constraint 2: each city must be exited once
for c in cities:
    if c != 'O':
        m.add_constraint(m.sum(x[(i, j)] for i, j in edges if j == c) == 1, ctname='city_in_' + c)

# Constraint 3: ensures that u_j = u_i + 1 if and only if x_ij = 1
for i, j in edges:
    if j != 'O':
        m.add_indicator(x[(i, j)], u[(i)] + 1 == u[(j)], name='order_' + i + '_' + j)

print('**************************************************************')
print(m.export_to_string())
print('**************************************************************')

m.parameters.timelimit = 120
m.parameters.mip.strategy.branch = 1
m.parameters.mip.tolerances.mipgap = 0.15

solution = m.solve(log_output=True)

m.get_solve_status()
solution.display()

# create df for decision variable, x
lst_x = []
for i in x:
    if solution.get_var_value(x[i]) > 0:
        soln_x = (i[0], i[1], solution.get_var_value(x[i]))
        lst_x.append(soln_x)
df_x = pd.DataFrame.from_records(lst_x, columns=['starting city', 'destination city', 'solution'])
print(df_x)

# create df for decision variable, u
lst_u = []
for c in u:
    soln_c = (c[0],solution.get_var_value(u[c]))
    lst_u.append(soln_c)
df_u = pd.DataFrame.from_records(lst_u, columns = ['city', 'visit order'])
df_u.sort_values(by=['visit order'], inplace = True)
print(df_u)

export_soln_to_csv(df_x, output_file_name1)
export_soln_to_csv(df_u, output_file_name2)