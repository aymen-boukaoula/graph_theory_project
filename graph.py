class Vertex:
    def __init__(self, label):
        self.label = label

class Edge:
    def __init__(self, start, end, weight=1):
        self.start = start
        self.end = end
        self.weight = weight

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def add_vertex(self, label):
        vertex = Vertex(label)
        self.vertices.append(vertex)

    def add_edge(self, start, end, weight=1):
        edge = Edge(start, end, weight)
        self.edges.append(edge)
    
    def get_neighbors(self, vertex):
        """
        Retourne les voisins d'un sommet avec leur poids.

        Args:
        - vertex: Le sommet dont on veut les voisins.

        Returns:
        - Une liste de tuples (voisin, poids).
        """
        neighbors = []
        for edge in self.edges:
            if edge.start == vertex:
                neighbors.append((edge.end, edge.weight))
        return neighbors
