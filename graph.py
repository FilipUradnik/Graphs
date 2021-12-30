from queue import Queue, PriorityQueue

class Edge:

    def __init__(self, v, w, oriented, index, weight=1):
        self.connected = True
        self.index = index
        self.weight = weight
        self.v = v
        self.w = w
        self.oriented = oriented

    def __repr__(self):
        if not self.connected:return "Edge(x)"
        return f"{self.weight}-Edge({self.v.index}, {self.w.index})"

    def forward(self, v):
        if not self.connected:return None
        if self.v == v:return self.w
        elif self.oriented: return None
        else:return self.v

    def backward(self, v):
        if not self.connected:return None
        if self.w == v:return self.v
        elif self.oriented: return None
        else:return self.w

    def export(self):
        return {
            "weight": self.weight,
            "v": self.v.index,
            "w": self.w.index
        }
class Vertex:
    
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.E = []
        self.distance = None
        self.component = None

    def __hash__(self):
        return hash(self.index)

    def __lt__(self, other):
        if self.distance is None:
            return False
        elif other.distance is None:
            return True
        return self.distance < other.distance

    def __eq__(self, other):
        if isinstance(other, int):return self.index == other
        return self.index == other.index

    def __repr__(self):
        return "Vertex(" + str(self.index) + ")"

    def neighbors(self, distance=False):
        if distance:return [(edge.forward(self.index), edge.weight) for edge in self.E if not edge.forward(self.index) is None]
        return [edge.forward(self.index) for edge in self.E if not edge.forward(self.index) is None]

    def backtracks(self, distance=False):
        if distance:return [(edge.backward(self.index), edge.weight) for edge in self.E if not edge.backward(self.index) is None]
        return [edge.backward(self.index) for edge in self.E if not edge.backward(self.index) is None]

class Graph:
    def __init__(self, N, values=[], multigraph=False, oriented=False, weighted=False):
        self.N = N
        self.E = []
        self.is_multigraph = multigraph
        self.is_oriented = oriented
        self.is_weighted = weighted
        if len(values) != N:values = [i for i in range(N)]
        self.V = [Vertex(i, values[i]) for i in range(N)]

    def __repr__(self):
        return f"{self.N}-Graph(" + ", ".join([str(x) for x in self.E if x.connected]) + ")"

    def connect(self, v, w, weight=1):
        """Connects two vertices with an edge

        Args:
            v (Vertex): one end of the edge
            w (Vertex): one end of the edge
        """
        if not self.is_weighted:weight = 1
        if self.is_multigraph or (not w in v.neighbors() and not w == v):
            edge = Edge(v, w, self.is_oriented, len(self.E), weight)
            self.E.append(edge)
            v.E.append(edge)
            w.E.append(edge)

    def vertex(self, index=None, value=None):
        """gets a Vertex object with a given index or value

        Args:
            v (int): Index of the vertex

        Returns:
            Vertex: Vertex with the given index
        """
        if not index is None and index < self.N:return self.V[index]
        if not value is None:
            for x in self.V:
                if x.value == value: return x

        return None

    def dfs(self, v=None, past=None):
        """Depth first search (generator)

        Args:
            v (Vertex, optional): Starting point. Defaults to 0.

        Yields:
            Vertex: Vertices of the component one by one
        """
        if v is None:v = self.V[0]

        if past is None:
            past = [None for _ in range(self.N)]
        yield v
        past[v.index] = True
        for x in v.neighbors():
            if past[x.index] is None:
                for y in self.dfs(x, past=past):yield y

    def bfs(self, v=None, priority=None):
        """Breadth first search (generator)

        Args:
            v (Vertex, optional): Starting point. Defaults to 0.
            queue (Queue-like, optional): Custom Queue-like object, for example PriorityQueue. Defaults to Python Queue.

        Yields:
            Vertex: Vertices of the component one by one
        """
        if v is None:v = self.V[0]

        if priority is None:
            queue = Queue()
            queue.put(v)
        else:
            queue = PriorityQueue()
            queue.put((priority(v), v))

        past = [None for _ in range(self.N)]
        past[v.index] = True

        while not queue.empty():
            v = queue.get()
            if not priority is None:v = v[1]
            yield v
            for x in v.neighbors():
                if not past[x.index]:
                    past[x.index] = True

                    if priority is None:queue.put(x)
                    else:queue.put((priority(x), x))

    def find_distance(self, v, u=None):
        """Finds distance between two vertices, sets the value of "distance" of every vertex to its distance from v

        Args:
            v (Vertex): The vertex from which to calculate the distance
            u (Vertex, optional): The vertex to which to calculate the distance. Defaults to None.

        Returns:
            int: Distance from u to v. None if there is no path between them or u wasn't specified
        """
        for x in self.V:
            x.distance = None
        v.distance = 0

        for w in self.bfs(v, lambda x: x.distance):
            if (not u is None) and w == u:
                return w.distance
            for vertex, weight in w.neighbors(True):
                if vertex.distance is None or vertex.distance > w.distance + weight:
                    vertex.distance = w.distance + weight

    def find_path(self, v, u):
        """Finds the shortest path between two vertices

        Args:
            v (Vertex): Starting point
            u (Vertex): Ending point

        Returns:
            list: List of vertices through which the path leads
        """
        d = self.find_distance(v, u)
        if d is None:
            return None

        r = [u]
        while v != u:
            #only choose from those neighbors, whose paths are optimal 
            u = min([x[0] for x in u.backtracks(True) if u.distance - x[0].distance == x[1]], key=lambda x: x.distance)
            d = u.distance
            r.append(u)

        return r[::-1]

    def export_graph_data(self):
        parameters = {
            "N": self.N,
            "is_weighted": self.is_weighted,
            "is_multigraph": self.is_multigraph,
            "is_oriented": self.is_oriented
        }
        vertices = [v.value for v in self.V]
        edges = [e.export() for e in self.E if e.connected]
        return {"parameters": parameters, "vertices": vertices, "edges": edges}

    def import_graph_data(self, data):
        if "parameters" in data.keys():
            parameters = data["parameters"]
            if "N" in parameters.keys():self.N = parameters["N"]
            if "is_weighted" in parameters.keys():self.is_weighted = parameters["is_weighted"]
            if "is_multigraph" in parameters.keys():self.is_multigraph = parameters["is_multigraph"]
            if "is_oriented" in parameters.keys():self.is_oriented = parameters["is_oriented"]
        
        if "vertices" in data.keys():
            if self.N != len(data["vertices"]):raise Exception
            self.V = [Vertex(i, data["vertices"][i]) for i in range(self.N)]

            if "edges" in data.keys():
                self.E = []
                for i in data["edges"]:
                    self.connect(self.vertex(i["v"]), self.vertex(i["w"]), i["weight"])
                    
        elif "edges" in data.keys(): raise Exception

if __name__ == '__main__':
    G = Graph(6, weighted=True)
    G.connect(G.vertex(0), G.vertex(1))
    G.connect(G.vertex(0), G.vertex(2))
    G.connect(G.vertex(0), G.vertex(3))
    G.connect(G.vertex(3), G.vertex(4))
    G.connect(G.vertex(3), G.vertex(5))
    G.connect(G.vertex(4), G.vertex(5))
    print(G); print("")
    print("DFS")
    for x in G.dfs():print(x)
    print(""); print('BFS')
    for x in G.bfs():print(x)
    print(); print('Distance')
    print(G.find_distance(G.vertex(0), G.vertex(5)))
    print(G.find_path(G.vertex(0), G.vertex(5)))
    print(); print('Export')
    print(G.export_graph_data())
    print(); print('Import')
    H = Graph(0)
    H.import_graph_data(G.export_graph_data())
    print(G.export_graph_data() == H.export_graph_data())

    