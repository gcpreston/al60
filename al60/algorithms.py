"""
Various algorithm implementations.
"""

from al60.data import Graph
from al60.data import DepthFirstIterator


def post_order(graph: Graph, v):
    """
    Compute the post-order of the given graph using a depth-first search from v.

    :param graph: the graph to get the post-order of
    :param v: the node to search from
    :return: a list of nodes in the order they were done being processed
    :raises ValueError: if v is not a defined node
    """
    if v not in graph.nodes():
        raise ValueError(f'node {v} is not defined')

    order = [node for node in DepthFirstIterator(graph, v)]
    order.reverse()
    return order


def topological_sort(graph: Graph, key=None):
    """
    Topologically sort this graph by repeatedly removing a node with no
    incoming edges and all of its outgoing edges and adding it to the order.

    :param graph: the graph to topologically sort
    :param key: a function of one argument used to extract a comparison key
        to determine which node to visit first (the "smallest" element)
    :return: a topological ordering of this graph
    """
    # TODO: Raise exception if not DAG
    # TODO: Implement using DFS

    # the number of incoming edges for each node
    in_degrees = {v: len(graph.in_nodes(v)) for v in graph.nodes()}
    # the nodes ready to be removed
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

    while ready:
        u = pop_min(ready)
        order.append(u)

        for v in graph.out_nodes(u):
            in_degrees[v] -= 1
            if in_degrees[v] == 0:
                ready.append(v)

    return order
