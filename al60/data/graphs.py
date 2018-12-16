"""
Module for graph representations.

This module makes use of abstract base
classes. Various concrete classes are subclasses of an abstract base class,
overriding its methods, as well as creating its own helper methods. Any
override of an abstract method will not repeat documentation from the abstract
base class. Any override of a non-abstract method will include documentation
indicating what has changed.
"""

import abc


class Graph(abc.ABC):
    """
    Abstract base class for a graph relating nodes with edges. Implements code
    common between all Graph subclasses, which is a directed graph using an
    adjacency set for edge representation.
    """

    @abc.abstractmethod
    def __init__(self):
        """
        Initialize default instance variables.
        """
        self._nodes = set()
        self._a_in = dict()
        self._a_out = dict()

    def nodes(self) -> set:
        """
        Get the set of nodes in this graph.

        :return: the set of defined nodes
        """
        return set(self._nodes)

    def edges(self) -> set:
        """
        Get the set of edges in this graph, represented as 2-tuples (from_node,
        to_node).

        :return: the set of defined edges
        """
        e = set()
        for u in self._nodes:
            for v in self._a_out[u]:
                e.add((u, v))
        return e

    def in_nodes(self, v):
        """
        Get the set of nodes with incoming edges to v.

        :param v: the node to get the incoming nodes for
        :return: the incoming nodes of v
        :raises ValueError: if v is not a defined node
        """
        if v not in self._nodes:
            raise ValueError(f'node {v} is not defined')

        return set(self._a_in[v])

    # TODO: Change name to neighbors?
    def out_nodes(self, u):
        """
        Get the set of nodes that v has outgoing edges to.

        :param u: the node to get the outgoing nodes for
        :return: the outgoing nodes of v
        :raises ValueError: if v is not a defined node
        """
        if u not in self._nodes:
            raise ValueError(f'node {u} is not defined')

        return set(self._a_out[u])

    def add_node(self, name):
        """
        Add a node to this graph.

        :param name: the name of the node to add
        :raises ValueError: if name is a previously defined node
        """
        if name in self._nodes:
            raise ValueError(f'node {name} is already defined')

        self._nodes.add(name)
        self._a_in[name] = set()
        self._a_out[name] = set()

    def add_nodes(self, *names):
        """
        Shortcut for adding multiple nodes in one call.

        :param names: the names of the nodes to add
        :raises ValueError: if any name is a previously defined node
        """
        for name in names:
            self.add_node(name)

    def add_edge(self, u, v):
        """
        Add an edge from u to v.

        :param u: the 'from' node
        :param v: the 'to' node
        :raises ValueError: if u or v is not a defined node or (u, v) is a
            previously defined edge
        """
        # add quotes to str if needed
        su = f"'{u}'" if isinstance(u, str) else u
        sv = f"'{v}'" if isinstance(v, str) else v

        if not (u in self._nodes and v in self._nodes):
            raise ValueError(f'invalid edge ({su}, {sv})')
        if v in self._a_out[u]:
            raise ValueError(f'edge ({su}, {sv}) is already defined')

        self._a_in[v].add(u)
        self._a_out[u].add(v)


# TODO: Remove and use Graph as DirectedGraph?
class DirectedGraph(Graph):
    """
    An unweighted, directed graph. Graph has all the implementation details of a
    DirectedGraph to reuse in other subclasses. DirectedGraph provides the
    concrete class name.
    """

    def __init__(self):
        super().__init__()


class UndirectedGraph(Graph):
    """
    An unweighted, undirected graph.
    """

    def __init__(self):
        super().__init__()

    def edges(self):
        """
        Get a set of edges in this graph, represented as 2-tuples (u, v) where
        u and v are defined nodes. Please that in an undirected graph, (u, v)
        == (v, u).

        :return: a set of defined edges
        """
        e = set()
        for u in self._nodes:
            for v in self._a_out[u]:
                if (v, u) not in e:
                    e.add((u, v))
        return e

    def add_edge(self, u, v):
        """
        Add an edge between u and v.

        :param u: the first node
        :param v: the second node
        :raises ValueError: if u or v is not a defined node or there already
            exists an edge between u and v
        """
        super().add_edge(u, v)
        super().add_edge(v, u)
