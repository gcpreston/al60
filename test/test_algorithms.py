"""
Tests for algorithm implementations in algorithms module.
"""

import unittest

from al60.data import DirectedGraph
from al60.algorithms import post_order, topological_sort


class TestGraphAlgorithms(unittest.TestCase):
    """
    Tests for graph algorithms.
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
