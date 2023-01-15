from data import Benchmark
from point import Point
from ant import Ant
from update_pheromone import Pheromone
from math import sqrt
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
        for i in range(5):
            self.population = self._create_population()
            for ant in self.population:
                update = Pheromone(ant, self.pheromone, self.cost, self.beta)
                while ant.not_visited:
                    new_point = update.get_new_point_by_roulette_wheel()
                    ant.go_to_next_point(new_point, self.cost[ant.current_point, new_point])
                ant.last_point(self.cost[ant.current_point, ant.start_point])
                if ant.distance_sum < min_distance:
                    min_distance = ant.distance_sum
                    min_path = ant.visited
            self._update_pheromones()
            print(i, sum([ant.distance_sum for ant in self.population]) / self.population_number)
        #self._plot_path()
        self._plot_min_path(min_path, min_distance)

    def _plot_min_path(self, min_path, min_distance):
        print(min_distance)
        plt.scatter([point.x for point in self.data.points], [point.y for point in self.data.points], s=10)
        x = [self.data.points[node].x for node in min_path]
        y = [self.data.points[node].y for node in min_path]
        plt.plot(x, y, 'r')
        plt.show()

    def _update_pheromones(self):
        for iy, ix in np.ndindex(self.pheromone.shape):
            self.pheromone[iy, ix] = (1 - self.evaporation_coefficient) * self.pheromone[iy, ix]
            self.pheromone[ix, iy] = (1 - self.evaporation_coefficient) * self.pheromone[ix, iy]
        for ant in self.population:
            for idx, point in enumerate(ant.visited[:-1]):
                self.pheromone[point, ant.visited[idx+1]] += 1 / ant.distance_sum
                self.pheromone[ant.visited[idx+1], point] += 1 / ant.distance_sum

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
        
