from data import Benchmark
from point import Point
from ant import Ant
from math import sqrt
from random import uniform
import numpy as np
import matplotlib.pyplot as plt


class TSP:
    def __init__(self, file: str, population: int = 5, start_pheromone: int = 1, evaporation: float = 0.3, beta: int = 5):
        self.data: Benchmark = Benchmark(file)
        self.num_of_points = self.data.length
        self.population_number = population
        self.start_pheromone = start_pheromone
        self.evaporation_coefficient = evaporation
        self.beta = beta
        self.cost = self._calculate_cost_matrix()
        self.pheromone = self._create_pheromone_matrix()
        self.population = self._create_population()

    def find_optimal_path(self):
        min_distance = 1000000000
        min_path = []
        for i in range(50):
            self.population = self._create_population()
            for ant in self.population:
                while ant.not_visited:
                    new_point = self._get_new_point_by_roulette_wheel(ant)
                    ant.go_to_next_point(new_point, self.cost[ant.current_point, new_point])
                ant.last_point(self.cost[ant.current_point, ant.start_point])
                if ant.distance_sum < min_distance:
                    min_distance = ant.distance_sum
                    min_path = ant.visited
            self._update_pheromones()
            print(i, sum([ant.distance_sum for ant in self.population]) / self.population_number)
        #self._plot_path()
        self._plot_min_path(min_path, min_distance)

    def _plot_path(self):
        colors = ['b', 'g', 'm', 'y', 'c']
        plt.plot([point.x for point in self.data.points], [point.y for point in self.data.points], 'ro')
        for idx, ant in enumerate(self.population):
            print(ant.distance_sum)
            x = [self.data.points[node].x for node in ant.visited]
            y = [self.data.points[node].y for node in ant.visited]
            plt.plot(x, y, colors[idx])
        plt.show()

    def _plot_min_path(self, min_path, min_distance):
        print(min_distance)
        x = [self.data.points[node].x for node in min_path]
        y = [self.data.points[node].y for node in min_path]
        plt.plot(x, y, 'g')
        plt.show()

    def _update_pheromones(self):
        for iy, ix in np.ndindex(self.pheromone.shape):
            self.pheromone[iy, ix] = (1 - self.evaporation_coefficient) * self.pheromone[iy, ix]
            self.pheromone[ix, iy] = (1 - self.evaporation_coefficient) * self.pheromone[ix, iy]
        for ant in self.population:
            for idx, point in enumerate(ant.visited[:-1]):
                self.pheromone[point, ant.visited[idx+1]] += 1 / ant.distance_sum
                self.pheromone[ant.visited[idx+1], point] += 1 / ant.distance_sum

    def _get_new_point_by_roulette_wheel(self, ant: Ant):
        cumulative_sum = self._calculate_cumulative_sum(ant)
        #print(cumulative_sum)
        random_number = uniform(0, next(iter(cumulative_sum.values())))
        for point, sum in list(reversed(list(cumulative_sum.items()))):
            if random_number < sum:
                return point
    
    def _calculate_cumulative_sum(self, ant):
        probabilities = self._calculate_probabilities(ant)
        return {point : sum(list(probabilities.values())[idx:]) for idx, point in enumerate(probabilities.keys())}

    def _calculate_probabilities(self, ant: Ant):
        denominator = self._calculate_denominator(ant)
        return {point : self._calculate_edge_probability(ant, point, denominator) for point in ant.not_visited}

    def _calculate_denominator(self, ant: Ant):
        denominator = 0
        for point in ant.not_visited:
            if point != ant.current_point:
                denominator += self._pheromone_mul_inverted_cost(ant, point)
        return denominator

    def _pheromone_mul_inverted_cost(self, ant: Ant, point: int):
        return self.pheromone[ant.current_point, point] * (1 / self.cost[ant.current_point, point])**self.beta

    def _calculate_edge_probability(self, ant: Ant, point: int, denominator: float):
        return self._pheromone_mul_inverted_cost(ant, point) / denominator

    def _calculate_cost_matrix(self):
        point: Point; next_point: Point
        cost = np.zeros((self.num_of_points, self.num_of_points))
        for idx, point in enumerate(self.data.points[:-1]):
            for _, next_point in enumerate(self.data.points[idx+1:]):
                cost[point.point_idx, next_point.point_idx] = self._calculate_cost_between_two_nodes(point, next_point)
                cost[next_point.point_idx, point.point_idx] = self._calculate_cost_between_two_nodes(point, next_point)
        return cost

    def _calculate_cost_between_two_nodes(self, p1: Point, p2: Point):
        return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def _create_pheromone_matrix(self):
        pheromone = np.ones((self.num_of_points, self.num_of_points)) * self.start_pheromone
        np.fill_diagonal(pheromone, 0)
        return pheromone

    def _create_population(self):
        return [Ant(self.num_of_points) for _ in range(self.population_number)]
        

if __name__ == '__main__':
    tsp = TSP('pbl395') 
    tsp.find_optimal_path() 
        
