import math


def load_map():
    file = open("grid.txt", "r")
    result = list(map(lambda line: list(map(lambda n: int(n), line.split())), file.readlines()))
    file.close()

    result.reverse()

    return result


def get_neighbours(point):
    neighbours = [
        Point(point.x, point.y + 1, point),
        Point(point.x, point.y - 1, point),
        Point(point.x - 1, point.y, point),
        Point(point.x + 1, point.y, point)
    ]
    neighbours = list(filter(lambda p: p.x >= 0 and p.x < 20 and p.y >= 0 and p.y < 20, neighbours))
    return neighbours


def euklides(point, target):
    return math.sqrt((point.x - target.x) ** 2 + (point.y - target.y) ** 2)


def g(point):
    count = 0
    parent = point.parent
    while parent is not None:
        count = count + 1
        parent = parent.parent
    return count


class Point(object):
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.f = None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def main():
    net = load_map()

    initial = Point(0, 0, None)
    target = Point(19, 19, None)
    closed_set = [initial]
    open_set = []

    current = initial
    while current != target:
        neighbours = get_neighbours(current)
        neighbours = list(filter(lambda p: net[p.y][p.x] != 5, neighbours))
        neighbours = list(filter(lambda p: p not in closed_set, neighbours))

        for point in neighbours:
            f = g(point) + euklides(point, target)
            point.f = f
            old_point = next(filter(lambda p: p == point, open_set), None)
            if old_point is None:
                open_set.append(point)
            elif old_point.f is not None and f < old_point.f:
                old_point.f = f
                old_point.parent = current

        if not open_set:
            break

        later = min(open_set, key=lambda x: x.f)
        open_set.remove(later)
        closed_set.append(later)
        current = later;

    if current != target:
        print("Nie można odnaleźć ścieżki")
        return

    road_set = []
    while current is not None:
        road_set.append([current.x, current.y])
        net[current.y][current.x] = 3
        current = current.parent

    net.reverse()
    for row in net:
        print(row)
    road_set.reverse()
    print(road_set)


if __name__ == "__main__":
    main()
