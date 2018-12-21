"""
Various algorithm implementations.
"""

from al60.data.graphs import Graph, UndirectedGraph
from al60.data.iterators import DepthFirstIterator, BreadthFirstIterator

# TODO: Figure out how to use types module


def post_order(graph: Graph, v) -> list:
    """
    Compute the post-order of the given graph using a depth-first search from v.
    Runs in O(|V| + |E|) time due to DFS.

    :param graph: the graph to operate on
    :param v: the node to search from
    :return: a list of nodes in the order they were done being processed
    :raises ValueError: if v is not a defined node
    """
    if v not in graph.nodes():
        raise ValueError(f'node {v} is not defined')

    order = [node for node in DepthFirstIterator(graph, v)]
    order.reverse()
    return order


def topological_sort(graph: Graph, key=None) -> list:
    """
    Topologically sort this graph by repeatedly removing a node with no
    incoming edges and all of its outgoing edges and adding it to the order.

    https://courses.cs.washington.edu/courses/cse326/03wi/lectures/RaoLect20.pdf

    :param graph: the graph to operate on
    :param key: a function of one argument used to extract a comparison key
        to determine which node to visit first (the "smallest" element)
    :return: a topological ordering of the given graph
    """
    # TODO: Raise exception if not DAG
    # TODO: Implement using DFS
    # TODO: Implement using priority queue

    # the number of incoming edges for each node: O(|E|)
    in_degrees = {v: len(graph.in_nodes(v)) for v in graph.nodes()}
    # the nodes ready to be removed: O(|V|)
    ready = [v for v in graph.nodes() if in_degrees[v] == 0]
    # the topological ordering
    order = []

    def pop_min(l):
        if key:
            _, idx = min([(ready[i], i) for i in range(len(ready))],
                         key=key)
            return l.pop(idx)
        else:
            _, idx = min((ready[i], i) for i in range(len(ready)))
            return l.pop(idx)

    # dequeue and output: O(|V|)?
    while ready:
        u = pop_min(ready)
        order.append(u)

        for v in graph.neighbors(u):
            in_degrees[v] -= 1
            if in_degrees[v] == 0:
                ready.append(v)

    return order


def components(graph: UndirectedGraph) -> tuple:
    """
    Compute a tuple of sets of nodes that make up connected components in the
    given graph. Implemented as follows:

    1. Create a set containing the nodes of the graph.
    2. Create an empty list.
    3. Perform a breadth-first search from any node in the set: O(|V| + |E|)
    4. Remove the discovered nodes from the set and add them to the list as a
       new set.
    5. Repeat until the set is empty.
    6. Convert the list to a tuple and return it.

    :param graph: the undirected graph to operate on
    :return: a tuple of connected components
    """
    nodes = graph.nodes()  # 1.
    comps = []  # 2.

    while nodes:  # 5.
        discovered = set(BreadthFirstIterator(graph, next(iter(nodes))))  # 3.
        # 4.
        nodes.difference_update(discovered)
        comps.append(discovered)

    return tuple(comps)  # 6.
