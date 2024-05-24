import tkinter as tk
from tkinter import simpledialog, messagebox
from graph import Graph
from algorithms import kruskal, prim, dijkstra, bellman_ford, welch_powell
import math

class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Theory Application")
        self.geometry("900x600")
        self.graph = Graph()
        self.vertex_positions = {}
        self.selected_vertex = None
        self.directed = False
        self.weighted = False
        self.colored_edges = []
        self.colored_vertices = []
        self.result_label = tk.Label(self, text="Results:")
        self.result_label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")
        self.results_text = tk.Text(self, height=10, width=50)
        self.results_text.pack(side=tk.TOP, padx=10, pady=5)
        self.get_graph_properties()
        self.create_widgets()

    def get_graph_properties(self):
        self.directed = messagebox.askyesno("Graph Type", "Is the graph directed?")
        self.weighted = messagebox.askyesno("Graph Type", "Is the graph weighted?")

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.kruskal_button = tk.Button(self, text="Kruskal MST", command=self.run_kruskal)
        self.kruskal_button.pack(side=tk.LEFT)

        self.prim_button = tk.Button(self, text="Prim MST", command=self.run_prim)
        self.prim_button.pack(side=tk.LEFT)

        self.dijkstra_button = tk.Button(self, text="Dijkstra", command=self.run_dijkstra)
        self.dijkstra_button.pack(side=tk.LEFT)

        self.bellman_ford_button = tk.Button(self, text="Bellman-Ford", command=self.run_bellman_ford)
        self.bellman_ford_button.pack(side=tk.LEFT)

        self.stable_set_button = tk.Button(self, text="Stable Set", command=self.run_stable_set)
        self.stable_set_button.pack(side=tk.LEFT)
        
        self.clear_button = tk.Button(self, text="Clear Results", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT)

    def on_canvas_click(self, event):
        clicked_vertex = self.get_clicked_vertex(event.x, event.y)
        if clicked_vertex is not None:
            if self.selected_vertex is None:
                self.selected_vertex = clicked_vertex
            else:
                start_vertex = self.selected_vertex
                end_vertex = clicked_vertex
                weight = 1
                if self.weighted:
                    weight = simpledialog.askinteger("Input", "Enter edge weight:", initialvalue=1)
                    if weight is None:
                        self.selected_vertex = None
                        return

                self.graph.add_edge(self.graph.vertices[start_vertex], self.graph.vertices[end_vertex], weight)
                if not self.directed:
                    self.graph.add_edge(self.graph.vertices[end_vertex], self.graph.vertices[start_vertex], weight)

                x1, y1 = self.vertex_positions[start_vertex]
                x2, y2 = self.vertex_positions[end_vertex]

                start_x, start_y, end_x, end_y = self.get_edge_coordinates(x1, y1, x2, y2)

                self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST if self.directed else tk.NONE)

                if self.weighted:
                    self.canvas.create_text((start_x + end_x) // 2, (start_y + end_y) // 2, text=str(weight), fill="blue")

                self.selected_vertex = None
        else:
            self.add_vertex(event.x, event.y)

    def get_clicked_vertex(self, x, y):
        for vertex, (vx, vy) in self.vertex_positions.items():
            if math.sqrt((x - vx) ** 2 + (y - vy) ** 2) <= 20:
                return vertex
        return None

    def add_vertex(self, x, y):
        label = len(self.graph.vertices)
        self.graph.add_vertex(label)
        self.vertex_positions[label] = (x, y)
        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="black")
        self.canvas.create_text(x, y, text=str(label), fill="white", font=("Arial", 12, "bold"))

    def get_edge_coordinates(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return x1, y1, x2, y2

        unit_dx = dx / distance
        unit_dy = dy / distance
        radius = 20

        start_x = x1 + unit_dx * radius
        start_y = y1 + unit_dy * radius
        end_x = x2 - unit_dx * radius
        end_y = y2 - unit_dy * radius

        return start_x, start_y, end_x, end_y

    def run_kruskal(self):
        mst = kruskal(self.graph)
        self.highlight_result(mst, "kruskal")

    def run_prim(self):
        mst = prim(self.graph, self.graph.vertices[0])
        self.highlight_result(mst, "prim")

    def run_dijkstra(self):
        start_vertex = simpledialog.askinteger("Input", "Enter start vertex:")
        if start_vertex is None:
            return
        distances, shortest_paths = dijkstra(self.graph, self.graph.vertices[start_vertex])
        self.highlight_result(distances, "dijkstra")
        self.highlight_shortest_path(shortest_paths)

    def run_bellman_ford(self):
        start_vertex = simpledialog.askinteger("Input", "Enter start vertex:")
        if start_vertex is None:
            return
        distances, shortest_paths = bellman_ford(self.graph, self.graph.vertices[start_vertex])
        self.highlight_result(distances, "bellman_ford")
        self.highlight_shortest_path(shortest_paths)


    def run_stable_set(self):
        stable_set = welch_powell(self.graph)
        self.highlight_result(stable_set, "welch_powell")

    def highlight_result(self, result, algorithm_type):
        self.results_text.delete(1.0, tk.END)  # Effacer le texte précédent
        self.clear_results()  # Effacer les colorations précédentes

        if algorithm_type in ["kruskal", "prim"]:
            # Afficher les arêtes du MST
            self.results_text.insert(tk.END, "Minimum Spanning Tree Edges:\n")
            for edge in result:
                self.results_text.insert(tk.END, f"{edge.start.label} -- {edge.end.label} (Weight: {edge.weight})\n")
                self.color_edge(edge, "red")
                self.colored_edges.append(edge)

        elif algorithm_type in ["dijkstra", "bellman_ford"]:
            # Afficher les distances
            self.results_text.insert(tk.END, "Shortest Path Distances:\n")
            for vertex, distance in result.items():
                self.results_text.insert(tk.END, f"Vertex {vertex.label}: Distance {distance}\n")
                self.color_vertex(vertex, "red")
                self.colored_vertices.append(vertex)

        elif algorithm_type == "welch_powell":
            # Afficher l'ensemble stable
            self.results_text.insert(tk.END, "Stable Set:\n")
            for vertex in result:
                self.results_text.insert(tk.END, f"Vertex {vertex.label}\n")
                self.color_vertex(vertex, "red")
                self.colored_vertices.append(vertex)

    def highlight_shortest_path(self, shortest_paths):
        for path in shortest_paths.values():
            for start_vertex, end_vertex in path:
                edge = self.graph.get_edge(start_vertex, end_vertex)
                if edge is not None:
                    self.color_edge(edge, "blue")


    def color_edge(self, edge, color):
        start_vertex, end_vertex = edge.start.label, edge.end.label
        x1, y1 = self.vertex_positions[start_vertex]
        x2, y2 = self.vertex_positions[end_vertex]
        start_x, start_y, end_x, end_y = self.get_edge_coordinates(x1, y1, x2, y2)
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color)

    def color_vertex(self, vertex, color):
        x, y = self.vertex_positions[vertex.label]
        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
        self.canvas.create_text(x, y, text=str(vertex.label), fill="white", font=("Arial", 12, "bold"))

    def clear_results(self):
        # Effacer les résultats précédents
        for edge in self.colored_edges:
            self.color_edge(edge, "black")
        self.colored_edges.clear()

        for vertex in self.colored_vertices:
            self.color_vertex(vertex, "black")
        self.colored_vertices.clear()

        # Effacer la coloration des arêtes
        for edge in self.graph.edges:
            self.color_edge(edge, "black")


if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()

