class DirectedGraph:
    """
    An unweighted, directed graph connecting nodes with edges. Implemented using
    an adjacency set for edge representation.
    """

    def __init__(self):
        """
        Initialize a new empty Graph instance.
        """
        self._nodes = set()
        self._a_in = dict()
        self._a_out = dict()

    # TODO: Return set?
    def nodes(self):
        """
        Get a list of nodes in this graph.

        :return: a list of defined nodes
        """
        return list(self._nodes)

    def edges(self):
        """
        Get a list of edges in this graph, represented as 2-tuples (from_node,
        to_node).

        :return: a list of defined edges
        """
        e = []
        for u in self._nodes:
            for v in self._a_out[u]:
                e.append((u, v))
        return e

    def in_edges(self, v):
        """
        Get the incoming edges for the given node.

        :param v: the node to get the incoming edges for
        :return: the incoming edges of v
        :raises ValueError: if v is not a defined node
        """
        if v not in self._nodes:
            raise ValueError(f'node {v} is not defined')

        return [(u, v) for u in self._a_in[v]]

    def out_edges(self, u):
        """
        Get the outgoing edges for the given node.

        :param u: the node to get the outgoing edges for
        :return: the outgoing edges of v
        :raises ValueError: if v is not a defined node
        """
        if u not in self._nodes:
            raise ValueError(f'node {u} is not defined')

        return [(u, v) for v in self._a_out[u]]

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
        Add an edge between nodes u and v.

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

    # TODO: Why *args instead of x?
    def dfs(self, v, pre_visit=lambda *args: None,
            post_visit=lambda *args: None):
        """
        Perform a depth-first search on this graph from node v.

        :param v: the starting node
        :param pre_visit: a function to execute on each discovered node before
            it is visited
        :param post_visit: a function to execute on each discovered node after
            it is visited
        :return: a list of the discovered nodes
        :raises ValueError: if v is not a defined node
        """
        if v not in self._nodes:
            raise ValueError(f'node {v} is not defined')

        found = set()

        def _dfs(_u):
            found.add(_u)

            pre_visit(_u)
            for _v in self._a_out[_u]:
                if _v not in found:
                    _dfs(_v)
            post_visit(_u)

        _dfs(v)
        return found

    def post_order(self, v):
        """
        Compute the post-order of this graph using a depth-first search from v.

        :param v: the node to search from
        :return: a list of nodes in the order they were done being processed
        :raises ValueError: if v is not a defined node
        """
        if v not in self._nodes:
            raise ValueError(f'node {v} is not defined')

        order = []
        self.dfs(v, post_visit=lambda x: order.append(x))

        return order

    def topological_sort(self, key=None):
        """
        Topologically sort this graph by repeatedly removing a node with no
        incoming edges and all of its outgoing edges and adding it to the order.

        :param key: a function of one argument used to extract a comparison key
            to determine which node to visit first (the "smallest" element)
        :return: a topological ordering of this graph
        """
        # TODO: Raise exception if not DAG, or make method on DAG type
        # TODO: Implement using DFS

        # the number of incoming edges for each node
        in_degrees = {key: len(val) for key, val in self._a_in.items()}
        # the nodes ready to be removed
        ready = [v for v in self._nodes if in_degrees[v] == 0]
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

            for v in self._a_out[u]:
                in_degrees[v] -= 1
                if in_degrees[v] == 0:
                    ready.append(v)

        return order
