"""
Tests for graph classes defined in data.graphs.
"""

import unittest

from al60.data.graphs import DirectedGraph


class TestDirectedGraph(unittest.TestCase):
    """
    Tests for DirectedGraph.
    """

    def setUp(self):
        self.g_empty = DirectedGraph()

        self.g1 = DirectedGraph()
        self.g1.add_nodes('u', 'a', 'b', 'c', 'x', 'y')
        self.g1.add_edge('u', 'a')
        self.g1.add_edge('a', 'u')
        self.g1.add_edge('u', 'c')
        self.g1.add_edge('c', 'a')
        self.g1.add_edge('c', 'b')
        self.g1.add_edge('b', 'u')
        self.g1.add_edge('x', 'y')

        self.g2 = DirectedGraph()
        self.g2.add_nodes('a', 'b', 'c', 'd')
        self.g2.add_edge('a', 'b')
        self.g2.add_edge('a', 'd')
        self.g2.add_edge('b', 'd')
        self.g2.add_edge('c', 'd')

    def test_add_node(self):
        self.g_empty.add_node(5)
        self.g_empty.add_node('hello')
        self.g_empty.add_node(True)

        self.assertEqual({5, 'hello', True}, self.g_empty._nodes)

        self.assertRaises(ValueError, self.g_empty.add_node, 1)

    def test_add_nodes(self):
        onebyone = DirectedGraph()
        onebyone.add_node('a')
        onebyone.add_node('b')
        onebyone.add_node('c')

        allatonce = DirectedGraph()
        allatonce.add_nodes('a', 'b', 'c')

        self.assertEqual(onebyone.nodes(), allatonce.nodes())

    def test_add_edge(self):
        self.assertRaises(ValueError, self.g_empty.add_edge, 'fake1', 'fake2')

        self.g_empty.add_node(1)
        self.g_empty.add_node(2)
        self.g_empty.add_edge(1, 2)

        self.assertEqual(self.g_empty._a_in, {1: set(), 2: {1}})
        self.assertEqual(self.g_empty._a_out, {1: {2}, 2: set()})

        self.assertRaises(ValueError, self.g_empty.add_edge, 1, 2)

    def test_add_edge_undefined_node(self):
        self.assertRaises(ValueError, self.g_empty.add_edge, 'hello', 'world')


if __name__ == '__main__':
    unittest.main()
