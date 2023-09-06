from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from os import path
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import math

COLOR = [[51, 153, 255], [255, 0, 255], [51, 204, 51]]




def load_map(file="input.txt"):
    if not path.isfile(file):
        print('File "' + file + '" does not exist')
        return
    f = open(file, "r")
    height = 0
    width = 0
    vertex = []
    reader = f.readlines()

    width, height = np.array(reader[0].split(','), dtype=int)
    # print(witdth,"-",height)
    game_map = np.full((height + 1, width + 1, 3), 255)

    game_map[0] = [183, 183, 183]
    game_map[height] = [183, 183, 183]
    game_map[:, 0] = [183, 183, 183]
    game_map[:, width] = [183, 183, 183]

    t = np.array(reader[1].split(','), dtype=int)
    for i in range(t.shape[0] // 2):
        vertex.append((t[2 * i], height - t[2 * i + 1]))

    for v in vertex:
        game_map[v[1], v[0]] = [255, 64, 0]

    n_polygons = int(reader[2])

    for i in range(n_polygons):
        t = np.array(reader[3 + i].split(','), dtype=int)
        v = []
        x = []
        y = []
        for j in range(t.shape[0] // 2):
            x.append(t[2 * j])
            y.append(t[2 * j + 1])
        x_max = max(x)
        x_min = min(x)
        y_min = min(y)
        y_max = max(y)
        for j in range(len(x)):
            v.append((x[j], y[j]))
        fill_polygon(game_map, v, x_min, x_max, y_min, y_max, height)
    f.close()

    return game_map, vertex


# fill color to obstacles by 4 points
def fill_polygon(game_map, polygon_vertex, x_min, x_max, y_min, y_max, height):
    polygon = Polygon(polygon_vertex)
    d = [(0, 0), (-0.5, 0), (0, 0.5), (0.5, 0.5), (0.5, -0.5)]
    for i in range(y_min, y_max + 1):
        for j in range(x_min, x_max + 1):
            for dt in d:
                if polygon.contains(Point(j + dt[0], i + dt[1])) or polygon.touches(Point(j + dt[0], i + dt[1])):
                    game_map[height - i, j] = [255, 255, 102]
                    break


def create_graph(func, game_map, vertex):
    path = dict()
    cost = np.zeros((len(vertex), len(vertex)), dtype=int)
    mapping = dict()
    for i in range(len(vertex)):
        mapping[str(i)] = vertex[i]

    for i in range(len(vertex) - 1):
        for j in range(i + 1, len(vertex)):
            p, c = func(game_map, vertex[i], vertex[j])
            path[str(vertex[i]) + str(vertex[j])] = p
            cost[i, j] = c
            p, c = func(game_map, vertex[j], vertex[i])
            path[str(vertex[j]) + str(vertex[i])] = p
            cost[j, i] = c

    return path, mapping, cost


 
def find_best_path(k, n, current_path, actual_path, min_cost, cost):
    if k == n:
        c = 0
        path = []
        path.append(0)
        for i in current_path:
            path.append(i)
        path.append(n + 1)
        for j in range(len(path) - 1):
            c += cost[path[j], path[j + 1]]
        if min_cost[0] == -1 or c < min_cost[0]:
            while actual_path.__len__() > 0:
                actual_path.pop()
            for tmp in path:
                actual_path.append(tmp)
            min_cost[0] = c
    else:
        for i in range(k - 1, n):
            curr_path[k - 1], curr_path[i] = curr_path[i], curr_path[k - 1]
            find_best_path(k + 1, n, curr_path, actual_path, min_cost, cost)
            curr_path[k - 1], curr_path[i] = curr_path[i], curr_path[k - 1]

            
# to fill color to the path
def fill_color(game_map, path, start, goal, color):
    v = path[str(goal)]
    while not np.all(start == v):
        if not np.all(game_map[v[1], v[0]] == [255, 64, 0]):
            game_map[v[1], v[0]] = color
        v = path[str(v)]


def find_path(func, game_map, vertex):
    ordered_vertex = []
    ordered_vertex.append(vertex[0])
    temp = vertex[2:]
    if len(temp) > 0:
        for i in temp:
            ordered_vertex.append(i)
    ordered_vertex.append(vertex[1])

    path, mapping, graph = create_graph(func, game_map, ordered_vertex)

    min_cost = [-1]
    actual_path = []
    if len(ordered_vertex) == 2:
        current_path = []
        find_best_path(0, 0, current_path, actual_path, min_cost, graph)
    else:
        current_path = [i for i in range(1, len(ordered_vertex) - 1)]
        find_best_path(1, len(ordered_vertex) - 2, current_path, actual_path, min_cost, graph)

    for i in range(len(actual_path) - 1):
        key = str(mapping[str(actual_path[i])]) + str(mapping[str(actual_path[i + 1])])
        current_path = path[key]
        fill_color(game_map, current_path, mapping[str(actual_path[i])], mapping[str(actual_path[i + 1])], color=COLOR[i % 3])


def draw(game_map, nameWindow):
    width = game_map.shape[1]
    height = game_map.shape[0]

    fig = plt.figure()
    fig.canvas.set_window_title(nameWindow)
    ax = fig.gca()

    ax.set_xticks(np.arange(0, width, 1))
    ax.set_yticks(np.arange(0, height, 1))

    ax.set_xticklabels(np.arange(0, width, 1))
    ax.set_yticklabels(np.arange(height - 1, -1, -1))

   
    ax.set_xticks(np.arange(-.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-.5, height, 1), minor=True)

    ax.grid(which='minor', color='k', linestyle='-', linewidth=1)
    plt.imshow(game_map)
    plt.show()
