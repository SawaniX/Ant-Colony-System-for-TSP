from point import Point


class Benchmark:
    def __init__(self, name):
        self.points = []
        with open(f'benchmarks/{name}.tsp', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if idx > 7 and line.split()[0] != 'EOF':
                    array = line.split()
                    self.points.append(Point(int(array[0]) - 1, int(array[1]), int(array[2])))
        self.length = len(self.points)

    def print_data(self):
        point : Point
        for point in self.points:
            print(f'Number: {point.point_idx}, x: {point.x}, y: {point.y}')