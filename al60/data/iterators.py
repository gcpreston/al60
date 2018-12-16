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

    def __iter__(self):
        return self

    def __next__(self):
        if self._worklist:
            return self._visit()
        else:
            raise StopIteration

    # TODO: Abstract more code
    @abc.abstractmethod
    def _visit(self):
        """
        Visit the node on the end of the worklist. Update the worklist with the
        new node(s) to visit and remove newly discovered nodes from remaining.

        :return: the next node in the worklist
        """
        pass


class DepthFirstIterator(GraphIterator):
    """
    Iterate over a graph in depth-first order.
    """

    def _visit(self):
        curr = self._worklist.pop()
        self._remaining.remove(curr)

        neighbors = list(self._graph.out_nodes(curr))
        neighbors.sort(key=self._key)
        # reverse because DFS uses a stack and nodes to be visited last should
        # be put on the bottom
        neighbors.reverse()

        for n in neighbors:
            if n in self._remaining:
                # move n to top of stack
                if n in self._worklist:
                    self._worklist.remove(n)
                self._worklist.append(n)

        return curr


class BreadthFirstIterator(GraphIterator):
    """
    Iterate over a graph in breadth-first order.
    """

    def _visit(self):
        curr = self._worklist.pop()
        self._remaining.remove(curr)

        neighbors = list(self._graph.out_nodes(curr))
        neighbors.sort(key=self._key)

        for n in neighbors:
            # do not visit later in worklist if already queued
            if n in self._remaining and n not in self._worklist:
                self._worklist.appendleft(n)

        return curr

