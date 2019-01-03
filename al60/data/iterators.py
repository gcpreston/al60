"""
Various iterators over defined data structures.
"""

import abc
import math

from typing import Iterable, Optional, Tuple
from collections import deque
from heapdict import HeapDict

from .types import Node
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
        self._worklist = deque([start])  # TODO: Default -> priority queue?
        self._remaining = set(graph.nodes())

    def _next_unvisited(self) -> Optional[Node]:
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

    def __iter__(self) -> Iterable[Node]:
        return self

    def __next__(self) -> Node:
        u = self._visit_next()
        if u:
            self._remaining.remove(u)
            return u
        else:
            raise StopIteration

    @abc.abstractmethod
    def _visit_next(self) -> Optional[Node]:
        """
        Visit the next unvisited node. Update the worklist with the new node(s)
        to visit.

        :return: the node that was visited, None if no unvisited nodes remain
        """
        pass


class DepthFirstIterator(GraphIterator):
    """
    Iterate over a graph in depth-first order.
    """

    def _visit_next(self) -> Optional[Node]:
        u = self._next_unvisited()

        if u:
            neighbors = list(self._graph.neighbors(u))
            neighbors.sort(key=self._key)
            # reverse because DFS uses a stack and nodes to be visited last
            # should be put on the bottom
            neighbors.reverse()

            for v in neighbors:
                if v in self._remaining:
                    # append + pop => stack
                    self._worklist.append(v)

            return u
        else:
            return None


class BreadthFirstIterator(GraphIterator):
    """
    Iterate over a graph in breadth-first order.
    """

    def _visit_next(self) -> Optional[Node]:
        u = self._next_unvisited()

        if u:
            neighbors = list(self._graph.neighbors(u))
            neighbors.sort(key=self._key)

            for v in neighbors:
                if v in self._remaining:
                    # appendleft + pop => queue
                    self._worklist.appendleft(v)

            return u
        else:
            return None


class WeightedGraphIterator(GraphIterator):
    """
    Abstract base class for graph iterators that include edge weight data. The
    difference between this class and GraphIterator is the signature of
    __next__, where GraphIterator simply returns a node, but
    WeightedGraphIterator returns a (node, weight) tuple.
    """

    def __next__(self) -> Tuple[Node, float]:
        (u, weight) = self._visit_next()
        if u:
            self._remaining.remove(u)
            return u, weight
        else:
            raise StopIteration

    @abc.abstractmethod
    def _visit_next(self) -> Tuple[Optional[Node], float]:
        """
        Visit the next unvisited node. Update the worklist with the new node(s)
        to visit.

        :return: a tuple of the node that was visited and its distance from
            the start node, (None, math.inf) if no unvisited nodes remain
        """
        pass


class DijkstraIterator(WeightedGraphIterator):
    """
    Iterate over the nodes of a graph based on their distance from the given
    start node using Dijkstra's shortest path algorithm.
    """

    def __init__(self, graph: Graph, start, key=None):
        """
        Create a new DijkstraIterator object.

        :param graph: the graph to iterate over
        :param start: the first node to visit
        :param key: a function of one argument used to extract a comparison key
            to determine which node to visit first in the case of a tie (the
            "smallest" element)
        :raises ValueError: if start is not defined in graph
        """
        super().__init__(graph, start, key=key)

        self._worklist = HeapDict()
        for u in graph.nodes():
            self._worklist[u] = math.inf
        self._worklist[start] = 0

    # TODO: Give distance information in iterable

    def _visit_next(self) -> Optional[Node]:
        try:
            (u, d_u) = self._worklist.popitem()
        except KeyError:
            return None, math.inf

        neighbors = list(self._graph.neighbors(u))
        neighbors.sort(key=self._key)

        for v in neighbors:
            if v in self._worklist:
                d_v = self._worklist[v]
                l_uv = self._graph.weight(u, v)

                if d_v > d_u + l_uv:
                    self._worklist[v] = d_u + l_uv

        return u, d_u
