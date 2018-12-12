class DirectedGraph:
    """
    An unweighted, directed graph connecting nodes with edges. Implemented using
    an adjacency set for edge representation.
    """

    def __init__(self):
        """
        Initialize a new empty Graph instance.
        """
        # TODO: Consider adjacency list vs. adjacency set
        self._nodes = set()
        self._a_in = dict()
        self._a_out = dict()

    def add_node(self, name):
        """
        Add a node to this graph.

        :param name: the name of the node to add
        :raises ValueError if name is a previously defined node
        """
        if name in self._nodes:
            raise ValueError(f'node {name} is already defined')

        self._nodes.add(name)
        self._a_in[name] = set()
        self._a_out[name] = set()

    def add_edge(self, u, v):
        """
        Add an edge between nodes u and v.

        :param u: the 'from' node
        :param v: the 'to' node
        :raises ValueError if u or v is not a defined node or (u, v) is a
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
        :raises ValueError if v is not a defined node
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
        :raises ValueError if v is not a defined node
        """
        if v not in self._nodes:
            raise ValueError(f'node {v} is not defined')

        order = []
        self.dfs(v, post_visit=lambda x: order.append(x))

        return order

    def topological_sort(self):
        """
        Topologically sort this graph using DFS calls from each node.

        :return: a topological ordering of this graph
        """
        # TODO: Raise exception if not DAG, or make method on DAG type
        # TODO: Implement using DFS

        stack = []
