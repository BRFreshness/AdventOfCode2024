
from icecream import ic

from util import Headings


class Vertex:
    def __init__(self, loc: tuple, h: Headings):
        self.loc = loc
        self.h = h

    def __repr__(self):
        return f'Vertex({self.loc}, {self.h})'

    def __str__(self):
        return f"{self.loc}-{self.h.name}"
class Edge:
    def __init__(self, u: int, v: int, weight: int):
        self.u = u
        self.v = v
        self.weight = weight

class Graph:
    def __init__(self):
        self.vertices: list[Vertex] = []
        self.edges: list[Edge] = []
        self.vertex_indices = {}
        self.edge_indices = {}
        self.dist = [[]]
        self.prev = [[]]

    def add_vertex(self, loc: tuple, h: Headings) -> int:
        idx = self.lookup_vertex(loc, h)
        if idx is None:
            key = (loc, h)
            idx = len(self.vertices)
            vertex = Vertex(loc, h)
            self.vertices.append(vertex)
            self.vertex_indices[key] = idx
        return idx

    def lookup_vertex(self, loc: tuple, h: Headings) -> int | None:
        key = (loc, h)
        if key in self.vertex_indices:
            return self.vertex_indices[key]
        return None

    def add_edge(self, edge: Edge):
        idx = len(self.edges)
        self.edges.append(edge)
        self.edge_indices[edge] = idx


    """
    From https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    
    let dist be a |V| x |V| array of minimum distances initialized to INF
    let prev be a |V| x |V| array of vertex indices initialized to None
    
    procedure FloydWarshallWithPathReconstruction() is
        for each edge (u, v) do
            dist[u][v] = w(u, v)  // The weight of the edge (u, v)
            prev[u][v] = u
        for each vertex v do
            dist[v][v] = 0
            prev[v][v] = v
        for k from 1 to |V| do // standard Floyd-Warshall implementation
            for i from 1 to |V|
                for j from 1 to |V|
                    if dist[i][j] > dist[i][k] + dist[k][j] then
                        dist[i][j] = dist[i][k] + dist[k][j]
                        prev[i][j] = prev[k][j]
    """
    def initialize(self):
        num_vertices = len(self.vertices)

        # initialize matrices
        self.dist = [[float("inf") for _ in range(num_vertices)] for _ in range(num_vertices)]
        self.prev = [[None for _ in range(num_vertices)] for _ in range(num_vertices)]
        for u in range(num_vertices):
            self.dist[u][u] = 0
            self.prev[u][u] = u

        # apply initial edge weights
        for e in self.edges:
            self.dist[e.u][e.v] = e.weight
            self.prev[e.u][e.v] = e.u

    def solve(self):
        num_vertices = len(self.vertices)
        last_p = 0
        # perform Floyd-Warshall algorithm
        for k in range(num_vertices):
            p = 100 * k // num_vertices
            if p != last_p:
                print(f"\r{p}%  ", end="", flush=True)
                last_p = p
            for i in range(num_vertices):
                for j in range(num_vertices):
                    if self.dist[i][j] > self.dist[i][k] + self.dist[k][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.prev[i][j] = self.prev[k][j]
        print()

        # check for negative cycles
        for i in range(num_vertices):
            if self.dist[i][i] != 0:
                print(F"Negative cycle at vertex {i} {self.vertices[i]}")


    """
    procedure Path(u, v) is
        if prev[u][v] = null then
            return []
        path = [v]
        while u ≠ v do
            v = prev[u][v]
            path.prepend(v)
        return path
    """
    def get_path(self, u: int, v: int):
        try:
            dist = self.dist[u][v]
        except IndexError:
            print(f"No path between {self.vertices[u]} and {self.vertices[v]}")
            dist = float("inf")
        if self.prev[u][v] is None:
            return [], dist
        path = [v]
        while v != u:
            v = self.prev[u][v]
            path.append(v)
        path.reverse()
        return path, dist

    def get_all_paths(self) -> (int, int, list):
        p = []
        for u in range(len(self.vertices)):
            for v in range(len(self.vertices)):
                if u != v and self.dist[u][v] < float("inf"):
                    p.append((u, v, self.get_path(u, v)))
        return p


def _test():
    g = Graph()
    g.add_vertex(loc=(1, 2), h=Headings.SOUTH)
    g.add_vertex(loc=(2, 2), h=Headings.EAST)
    g.add_vertex(loc=(5, 1), h=Headings.SOUTH)
    g.add_vertex(loc=(3, 9), h=Headings.NORTH)
    g.add_vertex(loc=(4, 4), h=Headings.WEST)
    g.add_edge(Edge(1, 2, 3))
    g.add_edge(Edge(2, 3, 4))
    g.add_edge(Edge(3, 4, 2))
    g.add_edge(Edge(3, 0, 6))
    g.add_edge(Edge(4, 1, 1))
    g.solve()
    ic(g.vertices, g.vertex_indices, g.dist, g.prev)

    for p in g.get_all_paths():
        print(f"{p[0]}->{p[1]} = {p[2]}")

if __name__ == "__main__":
    _test()
