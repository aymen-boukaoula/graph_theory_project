import math

def kruskal(graph):
    parent = {}
    def find(vertex):
        if parent[vertex] != vertex:
            parent[vertex] = find(parent[vertex])
        return parent[vertex]

    def union(v1, v2):
        root1 = find(v1)
        root2 = find(v2)
        if root1 != root2:
            parent[root2] = root1

    mst = []
    edges = sorted(graph.edges, key=lambda e: e.weight)
    for vertex in graph.vertices:
        parent[vertex] = vertex

    for edge in edges:
        if find(edge.start) != find(edge.end):
            union(edge.start, edge.end)
            mst.append(edge)

    return mst

def prim(graph, start_vertex):
    import heapq
    mst = []
    visited = set()
    edges = [(0, start_vertex, None)]
    while edges:
        weight, current_vertex, from_vertex = heapq.heappop(edges)
        if current_vertex in visited:
            continue
        visited.add(current_vertex)
        if from_vertex is not None:
            mst.append((from_vertex, current_vertex, weight))
        for edge in graph.edges:
            if edge.start == current_vertex and edge.end not in visited:
                heapq.heappush(edges, (edge.weight, edge.end, current_vertex))
            elif edge.end == current_vertex and edge.start not in visited:
                heapq.heappush(edges, (edge.weight, edge.start, current_vertex))
    return mst



import math

def dijkstra(graph, start_vertex):
    distances = {vertex: math.inf for vertex in graph.vertices}
    distances[start_vertex] = 0
    visited = set()

    while len(visited) < len(graph.vertices):
        current_vertex = min((vertex for vertex in graph.vertices if vertex not in visited), key=distances.get)
        visited.add(current_vertex)

        for neighbor, weight in graph.get_neighbors(current_vertex):
            new_distance = distances[current_vertex] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

    return distances



def bellman_ford(graph, start_vertex):
    distances = {vertex: math.inf for vertex in graph.vertices}
    distances[start_vertex] = 0

    for _ in range(len(graph.vertices) - 1):
        for edge in graph.edges:
            if distances[edge.start] + edge.weight < distances[edge.end]:
                distances[edge.end] = distances[edge.start] + edge.weight

    # Vérifier les cycles de poids négatif
    for _ in range(len(graph.vertices) - 1):
        for edge in graph.edges:
            if distances[edge.start] + edge.weight < distances[edge.end]:
                raise ValueError("Graph contains negative cycle")

    return distances


def welch_powell(graph):
    """
    Algorithme de Welch-Powell pour trouver l'ensemble stable dans un graphe.

    Args:
    - graph: Le graphe sur lequel l'algorithme est appliqué.

    Returns:
    - L'ensemble stable trouvé dans le graphe.
    """
    stable_set = set()
    available_vertices = set(graph.vertices)

    # Trier les sommets par degré décroissant
    sorted_vertices = sorted(graph.vertices, key=lambda v: len(graph.get_adjacent_vertices(v)), reverse=True)

    while available_vertices:
        # Sélectionner le sommet avec le plus grand degré
        max_degree_vertex = sorted_vertices[0]
        stable_set.add(max_degree_vertex)
        available_vertices.remove(max_degree_vertex)

        # Retirer les voisins du sommet sélectionné
        for vertex in available_vertices.copy():
            if vertex not in graph.get_adjacent_vertices(max_degree_vertex):
                stable_set.add(vertex)
                available_vertices.remove(vertex)

    return stable_set
