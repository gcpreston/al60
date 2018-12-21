"""
Various iterators over defined data structures.
"""

import abc

from collections import deque
from .graphs import Graph


class GraphIterator(abc.ABC):
    """
    Abstract base class for graph iterators.
    """

    def __init__(self, graph: Graph, start, key=None):
        """
        Create a new DepthFirstIterator object.

        :param graph: the graph to iterate over
        :param start: the first node to visit
        :param key: a function of one argument used to extract a comparison key
            to determine which node to visit first (the "smallest" element)
        :raises ValueError: if start is not defined in graph
        """
        if start not in graph.nodes():
            raise ValueError(f'node {start} is not defined')

        self._graph = graph
        self._key = key
        self._worklist = deque([start])
        self._remaining = set(graph.nodes())

    def _next_unvisited(self):
        """
        Pop nodes off of the worklist until an unvisited one is found.

        :return: the next unvisited node on the worklist, None if there are no
            unvisited nodes remaining
        """
        already_visited = True

        while already_visited and self._worklist:
            curr = self._worklist.pop()
            if curr in self._remaining:
                return curr

        return None

    def __iter__(self):
        return self

    def __next__(self):
        u = self._next_unvisited()
        if u:
            self._remaining.remove(u)
            self._visit(u)
            return u
        else:
            raise StopIteration

    @abc.abstractmethod
    def _visit(self, u):
        """
        Visit the given node u. Update the worklist with the new node(s) to
        visit.

        :raises ValueError: if u is not a defined node in this iterator's graph
        """
        if u not in self._graph.nodes():
            raise ValueError(f'node {u} is not defined')


class DepthFirstIterator(GraphIterator):
    """
    Iterate over a graph in depth-first order.
    """

    def _visit(self, u):
        super()._visit(u)

        neighbors = list(self._graph.neighbors(u))
        neighbors.sort(key=self._key)
        # reverse because DFS uses a stack and nodes to be visited last should
        # be put on the bottom
        neighbors.reverse()

        for n in neighbors:
            if n in self._remaining:
                # append + pop => stack
                self._worklist.append(n)


class BreadthFirstIterator(GraphIterator):
    """
    Iterate over a graph in breadth-first order.
    """

    def _visit(self, u):
        super()._visit(u)

        neighbors = list(self._graph.neighbors(u))
        neighbors.sort(key=self._key)

        for n in neighbors:
            if n in self._remaining:
                # appendleft + pop => queue
                self._worklist.appendleft(n)
