from ant import Ant
from random import uniform

class Pheromone:
    def __init__(self, ant: Ant, pheromone, cost, beta: int = 1):
        self.ant = ant
        self.beta = beta
        self.pheromone = pheromone
        self.cost = cost

    def get_new_point_by_roulette_wheel(self):
        cumulative_sum = self._calculate_cumulative_sum()
        random_number = uniform(0, next(iter(cumulative_sum.values())))
        for point, sum in list(reversed(list(cumulative_sum.items()))):
            if random_number < sum:
                return point
    
    def _calculate_cumulative_sum(self):
        probabilities = self._calculate_probabilities()
        return {point : sum(list(probabilities.values())[idx:]) for idx, point in enumerate(probabilities.keys())}

    def _calculate_probabilities(self):
        denominator = self._calculate_denominator()
        return {point : self._calculate_edge_probability(point, denominator) for point in self.ant.not_visited}

    def _calculate_denominator(self):
        denominator = 0
        for point in self.ant.not_visited:
            if point != self.ant.current_point:
                denominator += self._pheromone_mul_inverted_cost(point)
        return denominator

    def _pheromone_mul_inverted_cost(self, point: int):
        return self.pheromone[self.ant.current_point, point] * (1 / self.cost[self.ant.current_point, point])**self.beta

    def _calculate_edge_probability(self, point: int, denominator: float):
        return self._pheromone_mul_inverted_cost(point) / denominator