"""
Tests for graph classes defined in data.graphs.
"""

import unittest

from al60.data.graphs import Graph, Undirected


class TestGraph(unittest.TestCase):
    """
    Tests for Graph (directed).
    """

    def setUp(self):
        self.g_empty = Graph()

        self.g1 = Graph()
        self.g1.add_nodes('u', 'a', 'b', 'c', 'x', 'y')
        self.g1.add_edge('u', 'a')
        self.g1.add_edge('a', 'u')
        self.g1.add_edge('u', 'c')
        self.g1.add_edge('c', 'a')
        self.g1.add_edge('c', 'b')
        self.g1.add_edge('b', 'u')
        self.g1.add_edge('x', 'y')

        self.g2 = Graph()
        self.g2.add_nodes('a', 'b', 'c', 'd')
        self.g2.add_edge('a', 'b')
        self.g2.add_edge('a', 'd')
        self.g2.add_edge('b', 'd')
        self.g2.add_edge('c', 'd')

    def test_copy_constructor(self):
        g1_copy = Graph(self.g1)

        self.assertEqual(self.g1.nodes(), g1_copy.nodes())
        self.assertEqual(self.g1.edges(), g1_copy.edges())

        # changes made to g1_copy should not affect self.g1
        g1_copy.add_node('new1')
        g1_copy.add_edge('a', 'new1')

        self.assertTrue('new1' in g1_copy.nodes())
        self.assertTrue('new1' in g1_copy.neighbors('a'))
        self.assertTrue('new1' not in self.g1.nodes())
        self.assertTrue('new1' not in self.g1.neighbors('a'))

        # changes made to self.g1 should not affect g1_copy
        self.g1.add_node('new2')
        self.g1.add_edge('b', 'new2')

        self.assertTrue('new2' in self.g1.nodes())
        self.assertTrue('new2' in self.g1.neighbors('b'))
        self.assertTrue('new2' not in g1_copy.nodes())
        self.assertTrue('new2' not in g1_copy.neighbors('b'))

    def test_copy_constructor_mutable_node(self):
        class A:
            def __init__(self, v):
                self.v = v

        obj_node = A(['mutable', 'list'])
        self.g1.add_node(obj_node)
        self.g1.add_edge('y', obj_node)

        g1_copy = Graph(self.g1)

        self.assertEqual(self.g1, g1_copy)
        self.assertFalse(self.g1 is g1_copy)

        # ensure that obj_node is updated everywhere (deep copy will not work)
        obj_node.v.append('new')

        self.assertEqual(self.g1, g1_copy)
        self.assertFalse(self.g1 is g1_copy)

    def test_add_node(self):
        self.g_empty.add_node(5)
        self.g_empty.add_node('hello')
        self.g_empty.add_node(True)

        self.assertEqual({5, 'hello', True}, self.g_empty._nodes)

        self.assertRaises(ValueError, self.g_empty.add_node, 1)

    def test_add_nodes(self):
        onebyone = Graph()
        onebyone.add_node('a')
        onebyone.add_node('b')
        onebyone.add_node('c')

        allatonce = Graph()
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

    def test_parents(self):
        self.assertEqual({'a', 'b'}, self.g1.parents('u'))
        self.assertEqual({'u', 'c'}, self.g1.parents('a'))
        self.assertEqual({'c'}, self.g1.parents('b'))
        self.assertEqual({'u'}, self.g1.parents('c'))
        self.assertEqual(set(), self.g1.parents('x'))
        self.assertEqual({'x'}, self.g1.parents('y'))

    def test_neighbors(self):
        self.assertEqual({'a', 'c'}, self.g1.neighbors('u'))
        self.assertEqual({'u'}, self.g1.neighbors('a'))
        self.assertEqual({'u'}, self.g1.neighbors('b'))
        self.assertEqual({'a', 'b'}, self.g1.neighbors('c'))
        self.assertEqual({'y'}, self.g1.neighbors('x'))
        self.assertEqual(set(), self.g1.neighbors('y'))


class TestUndirectedGraph(unittest.TestCase):
    """
    Tests for Undirected.
    """

    def setUp(self):
        self.g1 = Undirected(Graph())
        self.g1.add_nodes('a', 'b', 'c')
        self.g1.add_edge('a', 'b')
        self.g1.add_edge('b', 'c')

        self.g_directed = Graph()
        self.g_directed.add_nodes(1, 2, 3, 4, 5)
        self.g_directed.add_edge(1, 2)
        self.g_directed.add_edge(1, 3)
        self.g_directed.add_edge(3, 2)
        self.g_directed.add_edge(3, 4)
        self.g_directed.add_edge(4, 3)

        self.g2 = Undirected(self.g_directed)

    def test_eq_directed_edges(self):
        # it is implied that these directed edges exists already in self.g2
        self.g_directed.add_edge(2, 1)
        self.g_directed.add_edge(3, 1)
        g2_test1 = Undirected(self.g_directed)

        self.assertEqual(self.g2, g2_test1)

    def test_eq_new_edge(self):
        # connecting previously disconnected nodes should make them different
        self.g_directed.add_edge(4, 5)
        g2_test2 = Undirected(self.g_directed)

        self.assertNotEqual(self.g2, g2_test2)

    def test_eq_new_node(self):
        # a new node should make them different
        self.g_directed.add_node(6)
        g2_test3 = Undirected(self.g_directed)

        self.assertNotEqual(self.g2, g2_test3)

    def test_parents(self):
        self.assertEqual({'b'}, self.g1.parents('a'))
        self.assertEqual({'a', 'c'}, self.g1.parents('b'))
        self.assertEqual({'b'}, self.g1.parents('c'))

    def test_neighbors(self):
        self.assertEqual({'b'}, self.g1.neighbors('a'))
        self.assertEqual({'a', 'c'}, self.g1.neighbors('b'))
        self.assertEqual({'b'}, self.g1.neighbors('c'))

    def test_double_decorator(self):
        double_g_directed = Undirected(Undirected(self.g_directed))
        double_g2 = Undirected(self.g2)

        self.assertEqual(self.g2, double_g_directed)
        self.assertEqual(self.g2, double_g2)

    # TODO: Write more tests for undirected graph


if __name__ == '__main__':
    unittest.main()
