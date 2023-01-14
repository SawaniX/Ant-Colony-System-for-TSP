from main import TSP
from math import sqrt
import numpy as np


def test_calculate_cost_matrix_3x3() -> None:
    tsp = TSP('test_calc_cost_matrix_3x3')

    result = np.array([[0, sqrt(18), sqrt(29)],
                       [sqrt(18), 0, sqrt(89)],
                       [sqrt(29), sqrt(89), 0]])

    assert np.array_equal(tsp.cost, result)

def test_calculate_cost_matrix_the_same_points() -> None:
    tsp = TSP('test_calc_cost_matrix_the_same_points')

    result = np.array([[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]])

    assert np.array_equal(tsp.cost, result)

def test_start_pheromone_matrix() -> None:
    tsp = TSP('test_calc_cost_matrix_3x3')

    result = np.array([[0, 1, 1],
                       [1, 0, 1],
                       [1, 1, 0]])

    assert np.array_equal(tsp.pheromone, result)

def test_start_pheromone_matrix_other_start_pheromone() -> None:
    tsp = TSP('test_calc_cost_matrix_the_same_points', start_pheromone=10)

    result = np.array([[0, 10, 10, 10, 10],
                       [10, 0, 10, 10, 10],
                       [10, 10, 0, 10, 10],
                       [10, 10, 10, 0, 10],
                       [10, 10, 10, 10, 0]])

    assert np.array_equal(tsp.pheromone, result)

def test_ants_population() -> None:
    tsp = TSP('test_calc_cost_matrix_the_same_points', start_pheromone=10)
    assert len(tsp.population) == 5
