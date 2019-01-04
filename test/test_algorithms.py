"""
Tests for algorithm implementations in algorithms module.
"""

import unittest
import itertools

from al60.data.graphs import Undirected, Graph
from al60.algorithms import post_order, topological_sort, components,\
    shortest_path, distance


class TestGraphAlgorithms(unittest.TestCase):
    """
    Tests for graph algorithms.
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

        self.g3 = Undirected(Graph())
        self.g3.add_nodes('a', 'b', 'c')
        self.g3.add_nodes('x', 'y', 'z')

        self.g3.add_edge('a', 'b')
        self.g3.add_edge('a', 'c')
        self.g3.add_edge('c', 'b')

        self.g3.add_edge('x', 'y')
        self.g3.add_edge('y', 'z')

        self.g4 = Graph()
        self.g4.add_nodes('a', 'b', 'c', 'd', 'e')
        self.g4.add_edge('a', 'b', weight=10)
        self.g4.add_edge('a', 'c', weight=3)
        self.g4.add_edge('b', 'c', weight=1)
        self.g4.add_edge('b', 'd', weight=2)
        self.g4.add_edge('c', 'b', weight=4)
        self.g4.add_edge('c', 'd', weight=8)
        self.g4.add_edge('c', 'e', weight=2)
        self.g4.add_edge('d', 'e', weight=7)
        self.g4.add_edge('e', 'd', weight=9)

    def test_post_order(self):
        self.assertRaises(ValueError, post_order, self.g1, 'fake')

        acceptable_orders = [['a', 'b', 'c', 'u'],
                             ['a', 'c', 'b', 'u'],
                             ['b', 'c', 'a', 'u'],
                             ['b', 'a', 'c', 'u'],
                             ['c', 'a', 'b', 'u'],
                             ['c', 'b', 'a', 'u']]
        actual = post_order(self.g1, 'u')
        self.assertTrue(actual in acceptable_orders)
        self.assertEqual(['y', 'x'], post_order(self.g1, 'x'))

    def test_topological_sort(self):
        self.assertEqual([], topological_sort(self.g_empty))

        g2_order = topological_sort(self.g2)
        for u, v in self.g2.edges():
            self.assertTrue(g2_order.index(u) < g2_order.index(v))

        # TODO: Test key

    def test_count_components(self):
        self.assertTrue(tuple(components(self.g3)) in
                        itertools.permutations([{'a', 'b', 'c'},
                                                {'x', 'y', 'z'}]))
        # TODO: More tests

    def test_shortest_path(self):
        self.assertEqual(['a', 'c', 'b', 'd'], shortest_path(self.g4, 'a', 'd'))

    def test_distance(self):
        self.assertEqual(9, distance(self.g4, 'a', 'd'))
