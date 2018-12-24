"""
Tests for iterators defined in data.iterators.
"""

import unittest

from al60.data.graphs import Graph, Undirected
from al60.data.iterators import DepthFirstIterator, BreadthFirstIterator


class TestDepthFirstIterator(unittest.TestCase):
    """
    Tests for DepthFirstIterator.
    """

    def setUp(self):
        self.g1 = Graph()
        self.g1.add_nodes('u', 'a', 'b', 'c')
        self.g1.add_nodes('x', 'y')
        self.g1.add_edge('u', 'a')
        self.g1.add_edge('a', 'u')
        self.g1.add_edge('u', 'c')
        self.g1.add_edge('c', 'a')
        self.g1.add_edge('c', 'b')
        self.g1.add_edge('b', 'u')
        self.g1.add_edge('x', 'y')

        self.g2 = Graph()
        self.g2.add_nodes('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 's')
        self.g2.add_edge('a', 'b')
        self.g2.add_edge('a', 's')
        self.g2.add_edge('s', 'c')
        self.g2.add_edge('s', 'g')
        self.g2.add_edge('c', 'd')
        self.g2.add_edge('c', 'e')
        self.g2.add_edge('c', 'f')
        self.g2.add_edge('f', 'g')
        self.g2.add_edge('g', 'h')
        self.g2.add_edge('h', 'e')

    def test_iterator(self):
        g1_u = list(DepthFirstIterator(self.g1, 'u'))
        g1_x = list(DepthFirstIterator(self.g1, 'x'))

        self.assertEqual(['u', 'a', 'c', 'b'], g1_u)
        self.assertEqual(['x', 'y'], g1_x)

        g2_a = list(DepthFirstIterator(self.g2, 'a'))

        self.assertEqual(['a', 'b', 's', 'c', 'd', 'e', 'h', 'g', 'f'], g2_a)

    def test_key(self):
        # reverse alphabetical order
        g1_u = list(DepthFirstIterator(self.g1, 'u', key=lambda x: -1 * ord(x)))
        g2_a = list(DepthFirstIterator(self.g2, 'a', key=lambda x: -1 * ord(x)))

        self.assertEqual(['u', 'c', 'b', 'a'], g1_u)
        self.assertEqual(['a', 's', 'g', 'h', 'e', 'c', 'f', 'd', 'b'], g2_a)


class TestBreadthFirstIterator(unittest.TestCase):
    """
    Tests for BreadthFirstIterator.
    """

    def setUp(self):
        self.g1 = Graph()
        self.g1.add_nodes('u', 'a', 'b', 'c')
        self.g1.add_nodes('x', 'y')
        self.g1.add_edge('u', 'a')
        self.g1.add_edge('a', 'u')
        self.g1.add_edge('u', 'c')
        self.g1.add_edge('c', 'a')
        self.g1.add_edge('c', 'b')
        self.g1.add_edge('b', 'u')
        self.g1.add_edge('x', 'y')

        self.g2 = Undirected(Graph())
        self.g2.add_nodes('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 's')
        self.g2.add_edge('a', 'b')
        self.g2.add_edge('a', 's')
        self.g2.add_edge('s', 'c')
        self.g2.add_edge('s', 'g')
        self.g2.add_edge('c', 'd')
        self.g2.add_edge('c', 'e')
        self.g2.add_edge('c', 'f')
        self.g2.add_edge('f', 'g')
        self.g2.add_edge('g', 'h')
        self.g2.add_edge('h', 'e')

    def test_iterator(self):
        g1_u = list(BreadthFirstIterator(self.g1, 'u'))
        g1_x = list(BreadthFirstIterator(self.g1, 'x'))

        self.assertEqual(['u', 'a', 'c', 'b'], g1_u)
        self.assertEqual(['x', 'y'], g1_x)

        g2_a = list(BreadthFirstIterator(self.g2, 'a'))

        self.assertEqual(['a', 'b', 's', 'c', 'g', 'd', 'e', 'f', 'h'], g2_a)

    def test_key(self):
        # reverse alphabetical order
        g1_u = list(BreadthFirstIterator(self.g1, 'u',
                                         key=lambda x: -1 * ord(x)))
        g2_a = list(BreadthFirstIterator(self.g2, 'a',
                                         key=lambda x: -1 * ord(x)))

        self.assertEqual(['u', 'c', 'a', 'b'], g1_u)
        self.assertEqual(['a', 's', 'b', 'g', 'c', 'h', 'f', 'e', 'd'], g2_a)
