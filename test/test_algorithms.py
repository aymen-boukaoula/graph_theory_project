import unittest
from graph import Graph
from algorithms import kruskal, prim, dijkstra, bellman_ford

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        for label in ['A', 'B', 'C']:
            self.graph.add_vertex(label)
        self.graph.add_edge(self.graph.vertices[0], self.graph.vertices[1], 1)
        self.graph.add_edge(self.graph.vertices[1], self.graph.vertices[2], 2)
        self.graph.add_edge(self.graph.vertices[0], self.graph.vertices[2], 4)

    def test_kruskal(self):
        mst = kruskal(self.graph)
        self.assertEqual(len(mst), 2)

    def test_prim(self):
        mst = prim(self.graph, self.graph.vertices[0])
        self.assertEqual(len(mst), 2)

    def test_dijkstra(self):
        distances = dijkstra(self.graph, self.graph.vertices[0])
        self.assertEqual(distances[self.graph.vertices[1]], 1)
        self.assertEqual(distances[self.graph.vertices[2]], 3)

    def test_bellman_ford(self):
        distances = bellman_ford(self.graph, self.graph.vertices[0])
        self.assertEqual(distances[self.graph.vertices[1]], 1)
        self.assertEqual(distances[self.graph.vertices[2]], 3)

if __name__ == '__main__':
    unittest.main()
