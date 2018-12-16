"""
Tests for iterators defined in data.iterators.
"""

import unittest

from al60.data import DirectedGraph
from al60.data import DepthFirstIterator


class TestDepthFirstIterator(unittest.TestCase):
    """
    Tests for DepthFirstIterator.
    """

    def setUp(self):
        self.g = DirectedGraph()
        self.g.add_nodes('u', 'a', 'b', 'c')
        self.g.add_nodes('x', 'y')

        self.g.add_edge('u', 'a')
        self.g.add_edge('a', 'u')
        self.g.add_edge('u', 'c')
        self.g.add_edge('c', 'a')
        self.g.add_edge('c', 'b')
        self.g.add_edge('b', 'u')

        self.g.add_edge('x', 'y')

    def test_iterator(self):
        g_u = [node for node in DepthFirstIterator(self.g, 'u')]
        g_x = [node for node in DepthFirstIterator(self.g, 'x')]

        self.assertEqual(['u', 'a', 'c', 'b'], g_u)
        self.assertEqual(['x', 'y'], g_x)
