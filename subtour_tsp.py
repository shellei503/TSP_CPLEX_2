import pandas as pd
from subtour_checker import SubtourChecker
from solve_model import CreateModel

# Data
df = pd.read_csv('data_cities_numbered.csv')
edges = list((t.origin, t.destination) for t in df.itertuples())
cities = set(df['destination'])
distance = dict([((t.origin, t.destination),t.distance) for t in df.itertuples()])
remove_nodes = None
to_be_forced_to_zero =[]

m = CreateModel(edges, cities, distance, remove_nodes)
m.define_constraints()
m.solve_model()
print('lb lst = ',m.lower_bound_lst)
print('soln = ',m.lst)
print()


s = SubtourChecker(m.lst)
while s.subtour_checker() is False:
    print('lst = ',s.lst) # this is the unupdated list
    print('_temp_lst=',s._temp_lst)
    print('_temp_lst2=',s._temp_lst2)
    print('subtours exists')
    print()

    to_be_branched = list(s.branches_to_set_to_zero())
    if len(to_be_branched)>0:
        print("to_be_branched = ",to_be_branched)
        m.remove_nodes = []
        m.remove_nodes.append(to_be_branched.pop(0))
        print("force to zero = ", m.remove_nodes)
        to_be_forced_to_zero.append(to_be_branched)
        # print("to be branched (do later) = ", to_be_branched)
        print("to be branched (do later) = ", to_be_forced_to_zero)
        print()
        m.define_subtour_constraints()
        m.solve_model()
        print(m.lower_bound_lst)
        soln_lst = m.lst
        print(soln_lst)
        s = SubtourChecker(soln_lst)
    else:
        break
