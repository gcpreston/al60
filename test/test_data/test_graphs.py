import unittest

from data.graphs import DirectedGraph


class TestGraph(unittest.TestCase):
    """
    Tests for data.graphs.DirectedGraph object.
    """

    def setUp(self):
        self.g_empty = DirectedGraph()

        self.g1 = DirectedGraph()
        self.g1.add_node('u')
        self.g1.add_node('a')
        self.g1.add_node('b')
        self.g1.add_node('c')
        self.g1.add_node('x')
        self.g1.add_node('y')

        self.g1.add_edge('u', 'a')
        self.g1.add_edge('a', 'u')
        self.g1.add_edge('u', 'c')
        self.g1.add_edge('c', 'a')
        self.g1.add_edge('c', 'b')
        self.g1.add_edge('b', 'u')
        self.g1.add_edge('x', 'y')

        self.g2 = DirectedGraph()
        self.g2.add_node('a')
        self.g2.add_node('b')
        self.g2.add_node('c')
        self.g2.add_node('d')

        self.g2.add_edge('a', 'b')
        self.g2.add_edge('a', 'd')
        self.g2.add_edge('b', 'd')
        self.g2.add_edge('c', 'd')

    def test_add_node(self):
        self.g_empty.add_node(1)
        self.g_empty.add_node('hello')
        # NOTE: When True is added, a ValueError is raised???
        self.g_empty.add_node(False)

        self.assertEqual({1, 'hello', False}, self.g_empty._nodes)

        self.assertRaises(ValueError, self.g_empty.add_node, 1)

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

    def test_dfs(self):
        self.assertRaises(ValueError, self.g1.dfs, 'fake')

        u_found = self.g1.dfs('u')
        x_found = self.g1.dfs('x')

        self.assertEqual({'u', 'a', 'c', 'b'}, u_found)
        self.assertEqual({'x', 'y'}, x_found)

        # TODO: Test pre_visit and post_visit

    def test_post_order(self):
        self.assertRaises(ValueError, self.g1.post_order, 'fake')

        self.assertEqual(['a', 'b', 'c', 'u'], self.g1.post_order('u'))
        self.assertEqual(['y', 'x'], self.g1.post_order('x'))

    def test_topological_sort(self):
        print(self.g2.topological_sort())


if __name__ == '__main__':
    unittest.main()
