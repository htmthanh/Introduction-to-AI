#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import support


# In[4]:


def extend(game_map, current):
    stt = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    neighbor = []
    for vt in stt:
        new_vertex = (current[0] + vt[0], current[1] + vt[1])
        if new_vertex[0] < game_map.shape[1] and new_vertex[0] > 0 and new_vertex[1] > 0 and new_vertex[1] < game_map.shape[0]:
            if not np.all(game_map[new_vertex[1], new_vertex[0]] == [255, 255, 102]) and not np.all(game_map[new_vertex[1], new_vertex[0]] == [183, 183, 183]):
                neighbor.append(new_vertex)
    return neighbor

def bfs(game_map,start,goal):
    queue=[]
    visited=[]
    previous=dict()
    _cost_to =dict()
    queue.append(start)
    _cost_to[str(start)]=0
    while len(queue)>0:
        current = queue.pop(0)
        visited.append(current)
        if np.all(current==goal):
            return previous,_cost_to[str(goal)]
        for point in extend(game_map,current):
            cost_to = _cost_to[str(current)]+1
            if point not in visited and point not in queue:
                _cost_to[str(point)]=cost_to
                previous[str(point)]=current
                queue.append(point)
    return previous, np.inf

_map, vertex = support.load_map('input.txt')
support.find_path(bfs,_map,vertex)
support.draw(_map,'Breadth First Search')


# In[ ]:




