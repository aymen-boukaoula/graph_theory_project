def save_graph(graph, filename):
    import json
    data = {
        'vertices': [v.label for v in graph.vertices],
        'edges': [{'start': e.start.label, 'end': e.end.label, 'weight': e.weight} for e in graph.edges]
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_graph(filename):
    import json
    from graph import Graph, Vertex, Edge
    graph = Graph()
    with open(filename, 'r') as f:
        data = json.load(f)
        for v in data['vertices']:
            graph.add_vertex(v)
        for e in data['edges']:
            start = next(v for v in graph.vertices if v.label == e['start'])
            end = next(v for v in graph.vertices if v.label == e['end'])
            graph.add_edge(start, end, e['weight'])
    return graph
