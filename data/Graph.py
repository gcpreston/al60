class Graph:
    """
    A mathematical graph connection nodes with edges.
    """

    def __init__(self, v: set, e: set):
        """
        Create a new Graph instance with the given nodes and edges. A node can be any object. An edge is a 2-tuple
        of two defined nodes.

        Example:
        v = {1, 2, 3}
        e = {(1, 2), (3, 1)}

        :param v: the set of nodes
        :param e: the set of edges
        """
        self._verify_edges(v, e)
        self._v = v
        self._e = e

    @staticmethod
    def _verify_edges(v: set, e: set):
        """
        Verify each member of e is a 2-tuple of values contained in v. Raises ValueError if this is not the case,
        otherwise does nothing.

        :param v: the set of defined nodes
        :param e: the set of edges to check
        """
        for edge in e:
            if not (isinstance(edge, tuple) and len(edge) == 2 and edge[0] in v and edge[1] in v):
                raise ValueError(f'nvalid edge {edge}')
