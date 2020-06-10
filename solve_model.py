from docplex.mp.model import Model

__author__ = 'slei'


class CreateModel:

    def __init__(self, edges, cities, distance, remove_nodes):
        self.edges = edges
        self.cities = cities
        self.distance = distance
        self.remove_nodes = remove_nodes
        self.m = Model('TSP_subtour_elimination')
        self.lst = []
        self.starting_city = None
        self.m.parameters.timelimit = 120
        self.m.parameters.mip.strategy.branch = 1
        self.m.parameters.mip.tolerances.mipgap = 0.15
        self.x = self.m.binary_var_dict(self.edges, name='x')
        self.u = self.m.continuous_var_dict(self.cities, name='u')
        self.lower_bound_lst = []




    def define_constraints(self):
        for c in self.cities:
            self.m.add_constraint(self.m.sum(self.x[(i, j)] for i, j in self.edges if i == c) == 1, ctname='city_out_%d' % c)

        for c in self.cities:
            self.m.add_constraint(self.m.sum(self.x[(i, j)] for i, j in self.edges if j == c) == 1, ctname='city_in_%d' % c)

    def define_subtour_constraints(self):
        for c in self.cities:
            self.m.add_constraint(self.m.sum(self.x[(i, j)] for i, j in self.remove_nodes if i == c) == 0,
                                  ctname='city_out_%d' % c)
        # print(self.m.export_to_string())

    def solve_model(self):
        self.m.minimize(self.m.sum(self.distance[e] * self.x[e] for e in self.edges))
        solution = self.m.solve(log_output=False)
        # self.m.get_solve_status()
        solution.display()
        self.lower_bound_lst.append(solution.objective_value)

        # format solution
        self.lst = []
        for i in self.x:
            if solution.get_var_value(self.x[i]) > 0:
                soln = (i[0], i[1], solution.get_var_value(self.x[i]))
                self.lst.append(soln)

