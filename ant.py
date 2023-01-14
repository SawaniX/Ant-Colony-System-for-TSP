from random import randint
from numpy import random
import numpy as np
import sys

class Ant:
    def __init__(self, num_of_points):
        self.num_of_points = num_of_points
        self.start_point = randint(0, num_of_points-1)
        self.current_point = self.start_point
        self.visited = [self.current_point]
        self.not_visited = list(range(0, num_of_points))
        self.not_visited.remove(self.current_point)
        self.distance_sum = 0

    def go_to_next_point(self, point, distance):
        self.current_point = point
        self.visited.append(point)
        self.not_visited.remove(point)
        self.distance_sum += distance

    def last_point(self, distance):
        self.visited.append(self.start_point)
        self.distance_sum += distance
    