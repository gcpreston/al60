class Graph:
    """
    An unweighted, undirected graph connecting nodes with edges.
    """

    def __init__(self):
        """
        Initialize a new empty Graph instance.
        """
        self._nodes = set()
        self._edges = set()

    def add_node(self, name):
        """
        Add a node to this graph.

        :param name: the name of the node to add
        """
        self._nodes.add(name)

    def add_edge(self, u, v):
        """
        Add an edge between nodes u and v. Raises ValueError if u or v is not a defined node.

        :param u: the 'from' node
        :param v: the 'to' node
        """
        if not (u in self._nodes and v in self._nodes):
            s1 = f"'{u}'" if isinstance(u, str) else u
            s2 = f"'{v}'" if isinstance(v, str) else v
            raise ValueError(f'invalid edge ({s1}, {s2})')

        self._edges.add((u, v))
