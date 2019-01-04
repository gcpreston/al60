"""
Various algorithm implementations.
"""

from typing import List, Set, Callable
from .data.types import Node

from al60.data.graphs import Graph, Undirected
from al60.data.iterators import DepthFirstIterator, DijkstraIterator


def post_order(graph: Graph, v: Node) -> List[Node]:
    """
    Compute the post-order of the given graph using a depth-first search from v.
    Total runtime: O(|V| + |E|) time due to DFS.

    :param graph: the graph to operate on
    :param v: the node to search from
    :return: a list of nodes in the order they were done being processed
    :raises ValueError: if v is not a defined node in graph
    """
    if v not in graph.nodes():
        raise ValueError(f'node {v} is not defined')

    order = [node for node in DepthFirstIterator(graph, v)]
    order.reverse()
    return order


# TODO: Fix key type
def topological_sort(graph: Graph, key: Callable[[Node], int] = None)\
        -> List[Node]:
    """
    Topologically sort this graph by repeatedly removing a node with no
    incoming edges and all of its outgoing edges and adding it to the order.
    Total runtime: O(|E|) + O(|V|) + O(|V|) = O(|V| + |E|).
    TODO: Check total runtime

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
    in_degrees = {v: len(graph.parents(v)) for v in graph.nodes()}
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


def components(graph: Undirected) -> List[Set[Node]]:
    """
    Compute a tuple of sets of nodes that make up connected components in the
    given graph. Implemented as follows:

    1. Create a set containing the nodes of the graph: O(|V|).
    2. Create an empty list: O(1).
    3. Perform a breadth-first search from any node in the set: O(|V| + |E|).
    4. Remove the discovered nodes from the set and add them to the list as a
       new set: O(|V|) + O(|V|).
    5. Repeat until the set is empty: O(|V|).
    6. Return the list

    TODO: Calculate total runtime (3. and 5. are not necessarily multiplied)

    :param graph: the undirected graph to operate on
    :return: a tuple of connected components
    """
    nodes = graph.nodes()  # 1.
    comps = []  # 2.

    while nodes:  # 5.
        # 3.
        discovered: Set[Node] = set(
            DepthFirstIterator(graph, next(iter(nodes))))
        # 4.
        nodes.difference_update(discovered)
        comps.append(discovered)

    return comps  # 6.


def shortest_path(g: Graph, s: Node, t: Node) -> List[Node]:
    """
    Compute the shortest path from s to t in the given graph.

    :param g: the graph to operate on
    :param s: the start node
    :param t: the end node
    :return: a list of nodes making up the shortest path from s to t in g
    :raises ValueError: if there is no path from s to t in g
    """
    # TODO: Fix shortest path with parent pointers
    path = []
    for (u, d_u) in DijkstraIterator(g, s):
        path.append(u)
        if u == t:
            return path

    raise ValueError(f'node {t} is not reachable from {s}')


def distance(g: Graph, s: Node, t: Node) -> float:
    """
    Compute the shortest path distance from s to t in the given graph.

    :param g: the graph to operate on
    :param s: the start node
    :param t: the end node
    :return: the distance of the shortest path from s to  in g
    :raises ValueError: if there is no path from s to t in g
    """
    for (u, d_u) in DijkstraIterator(g, s):
        if u == t:
            return d_u

    raise ValueError(f'node {t} is not reachable from {s}')
