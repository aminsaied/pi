import queue
from typing import Tuple, Set

import numpy as np

class Graph:
    def __init__(self, vertices: Set, edges: Set[Tuple]):
        """A graph is a set of vertices togther with a set of edges.

        Edges are tuples (a, b) where a, b are vertices. Note our graph is
        not directed, so (a, b) = (b, a)
        """
        self.vertices = vertices
        self.edges = edges

    @classmethod
    def from_maze_array(cls, arr: np.array):
        """Build graph from binary array.

        Note: We assume that 0s correspond to vertices.

        Algorithm:
            Suppose arr.shape = (n, m)
            1. Vertices correspond to index of 0s in flattened array
            2. Proceed though set of vertices:
                - If v + m in vertices then add the edge (v, v + m)
                - If v + 1 in vertices then add the edge (v, v + 1) unless
                    v is at the end of its row (i.e. v + 1 % m == 0)
        """
        # build vertices
        vertices = set()
        for i, x in enumerate(arr.flatten()):
            if x == 0:
                vertices.add(i)

        # build edges
        _, m = arr.shape
        edges = set()
        for v in vertices:
            if v + m in vertices:
                sorted_edge = (v, v + m)
                edges.add(sorted_edge)
            if v + 1 in vertices and (v + 1) % m > 0:
                sorted_edge = (v, v + 1)
                edges.add(sorted_edge)

        return cls(vertices=vertices, edges=edges)

    def is_solvable(self, start, end) -> bool:
        """Is there a path in the graph from `start` to `end`."""
        q = queue.Queue()
        q.put(start)

        enqueued = set()
        enqueued.add(start)

        while not q.empty():
            v = q.get()

            if v == end:
                return True

            # explore nhd of v
            for s, t in self.edges:
                if v == s:
                    if t not in enqueued:
                        q.put(t)
                        enqueued.add(t)
                elif v == t:
                    if s not in enqueued:
                        q.put(s)
                        enqueued.add(s)

        return False
    
    @staticmethod
    def coordinate_to_vertex(coordinate, arr):
        i, j = coordinate
        _, m = arr.shape
        return i * m + j

    @staticmethod
    def point_to_vertex(point, arr):
        _, m = arr.shape
        return point.x * m + point.y

    @classmethod
    def is_solvable_from_array(cls, arr, start, end):
        graph = cls.from_maze_array(arr)
        start_vertex = cls.point_to_vertex(start, arr)
        end_vertex = cls.point_to_vertex(end, arr)
        return graph.is_solvable(start_vertex, end_vertex)


if __name__ == "__main__":
    
    # example
    arr = np.array([
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 1],
    ]).T
    start = (0, 0)
    end = (0, 3)

    graph = Graph.from_maze_array(arr)

    start_vertex = graph.coordinate_to_vertex(start, arr)
    end_vertex = graph.coordinate_to_vertex(end, arr)
    print(graph.is_solvable(start_vertex, end_vertex))
