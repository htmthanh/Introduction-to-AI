#!/usr/bin/env python
# coding: utf-8

# In[1]:


import support
import numpy as np


# In[3]:


def ucs_search(game_map, start, goal):
    _from = dict()
    _cost_to = dict()
    p = []
    cost = np.zeros((game_map.shape[0], game_map.shape[1]), dtype = int)
    p.append(start)
    _from[str(start)] = start
    _cost_to[str(start)] = 0

    while p.__len__() > 0:
        current = get_promissing(p, cost)
        p.remove(current)
        if np.all(current == goal):
            return _from, _cost_to[str(goal)]

        for point in extend(game_map, current):
            cost_to = _cost_to[str(current)] + 1
            if str(point) not in _cost_to or cost_to < _cost_to[str(point)]:
                _cost_to[str(point)] = cost_to
                cost[point[1], point[0]] = cost_to 
                p.append(point)
                _from[str(point)] = current

    return _from, np.inf



def get_promissing(p, cost):
    min_cost = -1
    min_point = p[0]
    for point in p :
        if min_cost == -1 or cost[point[1], point[0]] < min_cost:
            min_point = point
            min_cost = cost[point[1], point[0]]
    return min_point

def extend(game_map, current):
    stt = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    near = []
    for vt in stt:
        new_vertex = (current[0] + vt[0], current[1] + vt[1])
        if new_vertex[0] < game_map.shape[1] and new_vertex[0] > 0 and new_vertex[1] > 0 and new_vertex[1] < game_map.shape[0]:
            if (not np.all(game_map[new_vertex[1], new_vertex[0]] == [255, 255, 102])) and (not np.all(game_map[new_vertex[1], new_vertex[0]] == [183, 183, 183])):
                near.append(new_vertex)
    return near

def heuristic(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


_map, vertex = support.load_map('input.txt')

support.find_path(ucs_search, _map, vertex)

support.draw(_map, 'UCS Search')


# In[ ]:




