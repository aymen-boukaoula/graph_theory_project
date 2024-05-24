import unittest
from graph import Graph

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_edge(self.graph.vertices[0], self.graph.vertices[1], 10)

    def test_add_vertex(self):
        self.assertEqual(len(self.graph.vertices), 2)
        self.graph.add_vertex('C')
        self.assertEqual(len(self.graph.vertices), 3)

    def test_add_edge(self):
        self.assertEqual(len(self.graph.edges), 1)
        self.graph.add_edge(self.graph.vertices[0], self.graph.vertices[1], 5)
        self.assertEqual(len(self.graph.edges), 2)

if __name__ == '__main__':
    unittest.main()
