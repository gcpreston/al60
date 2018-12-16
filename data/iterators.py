from collections import deque
from .graphs import DirectedGraph


class DepthFirstIterator:
    """
    Iterate over a graph in depth-first order.
    """

    def __init__(self, graph: DirectedGraph, start, key=None):
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
            u = self._worklist.pop()
            self._visit(u)
            return u
        else:
            raise StopIteration

    def _visit(self, u):
        """
        Add the unencountered nodes current has out-edges to to the worklist and
        remove them from the remaining nodes.

        :param u: the node to add the
        :raises ValueError: if current is not defined in self._graph
        """
        children = [v for _, v in self._graph.out_edges(u)]
        children.sort(key=self._key)
        # reverse because DFS uses a stack and nodes to be visited last should
        # be put on the bottom
        children.reverse()

        for v in children:
            if v in self._remaining:
                self._worklist.append(v)
                self._remaining.remove(v)
