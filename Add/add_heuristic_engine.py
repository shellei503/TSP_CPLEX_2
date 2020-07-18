import pandas as pd

__author__ = 'slei'


class AddHeuristicTSP:
    """ Finds the shortest path using a heuristic method """

    def __init__(self, cities_df):
        self.df = cities_df
        self.edges = list((t.origin, t.destination) for t in df.itertuples())
        self.distance = dict([((t.origin, t.destination), t.distance) for t in df.itertuples()])
        self.cities = list(set(df['destination']))
        self.cities_lst = []
        self.tour_lst = []
        self.distance_lst = []
        self.tour_leg_distances_lst = []
        self._final_df = None
        self._shortest_distance = None
        self._shortest_tour = None

    def find_subtour(self, starting_city):
        """ Given a starting city, finds a tour by selecting next shortest distance from list of unvisited cities """
        tour = []
        tour_distance_lst = [0]
        cities_unvisited = list(set(self.df['destination']))
        initial_city = starting_city
        current_city = initial_city
        tour.append(current_city)
        cities_unvisited.pop(0)
        total_distance = 0
        count = 0

        while len(cities_unvisited) > 0:
            # remove any city that has already been visited from consideration
            df_unvisited = self.df[self.df['destination'].isin(cities_unvisited)]

            # filter for rows based on first criterion
            is_current = df_unvisited['origin'] == current_city
            df2 = df_unvisited[is_current]

            # find the nearest city
            index_min = df2['distance'].idxmin()
            min_row = df2.loc[index_min]
            d = min_row.distance
            destination = min_row.destination

            # update next city and tour and total distance
            current_city = destination
            total_distance = total_distance + d
            tour_distance_lst.append(d)

            # update city tracker lists
            tour.append(current_city)
            index_i = cities_unvisited.index(current_city)
            cities_unvisited.pop(index_i)
            count = count + 1

            # check
            print("next destination: ", destination)
            print("distance: ", d)
            print("total_distance: ", total_distance)
            print("tour: ", tour)
            print("tour_distance_lst: ", tour_distance_lst)
            print("cities_unvisited: ", cities_unvisited)
            print()

        # adding the distance from last city back to initial city
        last_city = tour[-1]
        last_mile = (initial_city, last_city)
        last_mile_distance = self.distance[last_mile]
        tour.append(initial_city)
        total_distance = total_distance + last_mile_distance
        tour_distance_lst.append(last_mile_distance)

        # check
        print("last_mile: ", last_mile)
        print("last_mile_distance: ", last_mile_distance)
        print("tour: ", tour)
        print("total_distance: ", total_distance)
        print("tour_leg_distances_lst: ", tour_distance_lst)

        # update lists
        self.tour_lst.append(tour)
        self.distance_lst.append(total_distance)
        self.tour_leg_distances_lst.append(tour_distance_lst)

    @property
    def final_df(self):
        """ Add description here"""
        if self._final_df is None:
            self._final_df = self._generate_final_df()
        return self._final_df

    def _generate_final_df(self):
        for c in self.cities:  # for every city in the dataset
            print("city: ", c)  # generate a tour for each
            print("--------------------------------------------------------------------------------")
            self.find_subtour(c)
            print('********************************************************************************')
            print()

        soln_dict = {'city': self.cities, 'tour': self.tour_lst, 'tour_leg_distances': self.tour_leg_distances_lst,
                     'distance': self.distance_lst}
        return pd.DataFrame(soln_dict)

    @property
    def shortest_distance(self):
        """ Add description here"""
        if self._shortest_distance is None:
            return self._calculate_shortest_distance()

    def _calculate_shortest_distance(self):  # find the tour with the lowest distance
        index_min_final = self.final_df['distance'].idxmin()  # returns the index location of min value
        min_row_final = self.final_df.loc[index_min_final]
        return min_row_final.distance

    @property
    def shortest_tour(self):
        """ Add description here"""
        if self._shortest_tour is None:
            return self._generate_shortest_tour()

    def _generate_shortest_tour(self):
        index_min_final = self.final_df['distance'].idxmin()  # returns the index location of min value
        min_row_final = self.final_df.loc[index_min_final]
        return min_row_final.tour


# ********************************************************************************
# ********************************************************************************

if __name__ == '__main__':
    df = pd.read_csv('city_data_add.csv')
    tsp = AddHeuristicTSP(df)

    tsp.final_df
    print("final_df")
    print(tsp.final_df)
    print()

    print("shortest_distance_final", tsp.shortest_distance)
    print("shortest_tour_final", tsp.shortest_tour)
