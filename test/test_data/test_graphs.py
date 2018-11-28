import unittest

from data.graphs import Graph


class TestGraph(unittest.TestCase):
    """
    Tests for data.graphs.Graph object.
    """

    def setUp(self):
        self.g1 = Graph()

    def test_add_node(self):
        self.g1.add_node(1)
        self.g1.add_node(1)
        self.g1.add_node(2)
        self.g1.add_node('hello')

        self.assertEqual(self.g1._nodes, {1, 2, 'hello'})

    def test_add_edge(self):
        self.g1.add_node(1)
        self.g1.add_node(2)
        self.g1.add_edge(1, 2)

        self.assertEqual(self.g1._edges, {(1, 2)})

    def test_add_edge_undefined_node(self):
        self.assertRaises(ValueError, self.g1.add_edge, 'hello', 'world')


if __name__ == '__main__':
    unittest.main()
