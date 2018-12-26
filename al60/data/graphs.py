"""
Module for graph representations.
"""

from typing import Set, Dict
from .types import Node, Edge


class Graph:
    """
    An weighted, directed graph relating nodes with edges. This is the most
    basic graph class. Nodes can be any hashable type.
    TODO: Make nodes have a value which can be any type, and give each a
     hashable unique ID?

    Please note that in Python, False == 0 and True == 1. Therefore,
    {1}.add(True) remains {1}. This means that if 1 is a defined node, a node
    True cannot be defined, and vice versa. The same goes for 0 and False.
    """

    def __init__(self, other: 'Graph' = None, default_weight: float = 1):
        """
        Initialize a new Graph. Either copy an existing Graph or create an empty
        one. When copying another graph, the nodes are not deep copied. This
        means that if other has a node which is an object that is mutated,
        this mutation will appear in both this Graph and other.

        :param other: the Graph to copy
        :param default_weight: the weight to give new edges if unspecified
        """
        if other:
            self._nodes: Set[Node] = set(other._nodes)
            self._a_in: Dict[Node, Set[Node]] =\
                {u: set(other._a_in[u]) for u in other._a_in}
            self._a_out: Dict[Node, Set[Node]] =\
                {u: set(other._a_out[u]) for u in other._a_out}
            self._weights: Dict[Edge, float] =\
                {key: default_weight for key in self.edges()}
        else:
            self._nodes: Set[Node] = set()
            self._a_in: Dict[Node, Set[Node]] = dict()
            self._a_out: Dict[Node, Set[Node]] = dict()
            self._weights: Dict[Edge, float] = dict()
        self._default_weight = default_weight

    def nodes(self) -> Set[Node]:
        """
        Get the set of nodes in this graph.

        :return: the set of defined nodes
        """
        return set(self._nodes)

    def edges(self) -> Set[Edge]:
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

    def parents(self, v: Node) -> Set[Node]:
        """
        Get the set of nodes which have outgoing edges to v.

        :param v: the node to get the parents of
        :return: the parents of v
        :raises ValueError: if v is not a defined node
        """
        if v not in self._nodes:
            raise ValueError(f'node {v} is not defined')

        return set(self._a_in[v])

    # TODO: Change to children?
    def neighbors(self, u: Node) -> Set[Node]:
        """
        Get the set of nodes which u has outgoing edges to.

        :param u: the node to get the neighbors of
        :return: the neighbors of u
        :raises ValueError: if u is not a defined node
        """
        if u not in self._nodes:
            raise ValueError(f'node {u} is not defined')

        return set(self._a_out[u])

    def add_node(self, node: Node) -> None:
        """
        Add a node to this graph.

        :param node: the value to reference this node by
        :raises ValueError: if name is a previously defined node
        """
        if node in self._nodes:
            raise ValueError(f'node {node} is already defined')

        self._nodes.add(node)
        self._a_in[node] = set()
        self._a_out[node] = set()

    def add_nodes(self, *names: Node) -> None:
        """
        Shortcut for adding multiple nodes in one call.

        :param names: the names of the nodes to add
        :raises ValueError: if any name is a previously defined node
        """
        for name in names:
            self.add_node(name)

    def add_edge(self, u: Node, v: Node, weight: float = None) -> None:
        """
        Add an edge from u to v.

        :param u: the 'from' node
        :param v: the 'to' node
        :param weight: the weight of the edge
        :raises ValueError: if u or v is not a defined node or (u, v) is a
            previously defined edge
        """
        # TODO: Abstract adding quotes if str
        # add quotes to str if needed
        su = f"'{u}'" if isinstance(u, str) else u
        sv = f"'{v}'" if isinstance(v, str) else v

        if not (u in self._nodes and v in self._nodes):
            raise ValueError(f'invalid edge ({su}, {sv})')
        if v in self._a_out[u]:
            raise ValueError(f'edge ({su}, {sv}) is already defined')

        self._a_in[v].add(u)
        self._a_out[u].add(v)

        if weight:
            self._weights[(u, v)] = weight
        else:
            self._weights[(u, v)] = self._default_weight

    def remove_node(self, u: Node) -> None:
        """
        Remove the node u from this graph.

        :param u: the node to remove
        :raises ValueError: if u is not a defined node
        """
        if u not in self._nodes:
            raise ValueError(f'node {u} is not defined')

        self._nodes.remove(u)
        del self._a_in[u]
        del self._a_out[u]

    def remove_edge(self, u: Node, v: Node) -> None:
        """
        Remove the edge from u to v.

        :param u: the 'from' node of the edge to be removed
        :param v: the 'to' node of the edge to be removed
        :raises ValueError: if edge (u, v) does not exist in this graph
        """
        if v in self._a_out[u]:
            self._a_out[u].remove(v)
            self._a_in[v].remove(u)
        else:
            # add quotes to str if needed
            su = f"'{u}'" if isinstance(u, str) else u
            sv = f"'{v}'" if isinstance(v, str) else v
            raise ValueError(f'edge ({su}, {sv}) is not defined')

    def __eq__(self, other):
        if isinstance(other, Graph):
            return (self._nodes == other._nodes and
                    self._a_in == other._a_in and
                    self._a_out == other._a_out)
        else:
            return False


class Undirected(Graph):
    """
    An undirected graph. Takes an existing Graph object and makes an undirected
    copy. Please note that in an undirected graph, the edges (u, v) and (v, u)
    are interchangable. Therefore, if you are checking whether the returned
    tuple from edges() contains an edge (u, v), you should also check if it
    contains (v, u). Due to this discrepency between directed and undirected
    graphs, it is preferrable to use the parents/neighbors methods to check if
    two nodes are connected.
    """

    def __init__(self, graph: Graph):
        """
        Initialize a new Undirected.

        :param graph: the Graph to make an undirected version of
        """
        super().__init__(graph)

    def parents(self, v: Node) -> Set[Node]:
        """
        Get the set of nodes which have outgoing edges to v. For an undirected
        graph, this is the same set that neighbors(v) provides.

        :param v: the node to get the parents of
        :return: the parents of v
        :raises ValueError: if v is not a defined node
        """
        return super().parents(v).union(self._a_out[v])

    def neighbors(self, u: Node) -> Set[Node]:
        """
        Get the set of nodes which u has outgoing edges to. For an undirected
        graph, this is the same set that parents(u) provides.

        :param u: the node to get the neighbors of
        :return: the neighbors of u
        :raises ValueError: if u is not a defined node
        """
        return super().neighbors(u).union(self._a_in[u])

    def remove_edge(self, u: Node, v: Node) -> None:
        """
        Remove the edge between u and v.

        :param u: the first node of the edge to be removed
        :param v: the second node of the edge to be removed
        :raises ValueError: if edge (u, v)/(v, u) does not exist in this graph
        """
        if v in self._a_out[u]:
            self._a_out[u].remove(v)
            self._a_in[v].remove(u)
        if u in self._a_out[v]:
            self._a_out[v].remove(u)
            self._a_in[u].remove(v)
        else:
            # add quotes to str if needed
            su = f"'{u}'" if isinstance(u, str) else u
            sv = f"'{v}'" if isinstance(v, str) else v
            raise ValueError(f'edge ({su}, {sv}) is not defined')

    def __eq__(self, other):
        if isinstance(other, Undirected):
            if self._nodes == other._nodes:
                for u in self._nodes:
                    if self.neighbors(u) != other.neighbors(u):
                        return False
                # all the same nodes which have all the same neighbors
                return True
        # not Undirected or different nodes
        return False


class Unweighted(Graph):
    """
    An unweighted graph. Takes an existing Graph object and makes an unweighted
    copy.
    """

    def __init__(self, graph: Graph):
        """
        Initialize a new Unweighted.

        :param graph: the Graph to make an unweighted version of
        """
        super().__init__(graph, default_weight=1)

    def add_edge(self, u: Node, v: Node, weight: float = 1):
        """
        Add an edge from u to v. The weight parameter sholuld not be used, as
        it is ignored.

        :param u: the 'from' node
        :param v: the 'to' node
        :param weight: the weight of the edge
        :raises ValueError: if u or v is not a defined node or (u, v) is a
            previously defined edge
        """
        super().add_edge(u, v)
        self._weights[(u, v)] = 1
