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
        self._remaining.remove(start)

    def __iter__(self):
        return self

    def __next__(self):
        if self._worklist:
            return self._visit()
        else:
            raise StopIteration

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

    # TODO: Fix bug where node is added to worklist but then found quicker
    def _visit(self):
        u = self._worklist.pop()
        children = list(self._graph.out_nodes(u))
        # TODO: Handle if < is not supported
        children.sort(key=self._key)
        # reverse because DFS uses a stack and nodes to be visited last should
        # be put on the bottom
        children.reverse()

        for v in children:
            if v in self._remaining:
                self._worklist.append(v)
                self._remaining.remove(v)

        return u


class BreadthFirstIterator(GraphIterator):
    """
    Iterate over a graph in breadth-first order.
    """

    def _visit(self):
        u = self._worklist.pop()
        children = list(self._graph.out_nodes(u))
        # TODO: Handle if < is not supported
        children.sort(key=self._key)

        for v in children:
            if v in self._remaining:
                self._worklist.appendleft(v)
                self._remaining.remove(v)

        return u
