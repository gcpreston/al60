import unittest

from data.graphs import DirectedGraph
from data.iterators import DepthFirstIterator


class TestDepthFirstIterator(unittest.TestCase):
    """Tests for DepthFirstIterator"""

    def setUp(self):
        self.g = DirectedGraph()
        self.g.add_node('u')
        self.g.add_node('a')
        self.g.add_node('b')
        self.g.add_node('c')

        self.g.add_edge('u', 'a')
        self.g.add_edge('a', 'u')
        self.g.add_edge('u', 'c')
        self.g.add_edge('c', 'a')
        self.g.add_edge('c', 'b')
        self.g.add_edge('b', 'u')

    def test_iterator(self):
        g_dfs = []
        for node in DepthFirstIterator(self.g, 'u'):
            g_dfs.append(node)

        self.assertEqual(['u', 'a', 'c', 'b'], g_dfs)
