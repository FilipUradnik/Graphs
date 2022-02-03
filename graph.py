from queue import Queue, PriorityQueue


class Edge:

    def __init__(self, v, w, directed, index, weight=1):
        self.connected = True
        self.index = index
        self.weight = weight
        self.v = v
        self.w = w
        self.directed = directed

    def __repr__(self):
        if not self.connected:
            return "Edge(x)"
        return f"{self.weight}-Edge({self.v.value}, {self.w.value})"

    def visualize(self):
        r = str(self.v.value) + " "
        if self.weight != 1:r += f"-({self.weight})-"
        else:r += "---"
        if self.directed:r += ">"
        r += " " + str(self.w.value)
        return r

    def forward(self, v):
        """returns a second end of the edge
        if directed - it returns the edge only if it's in the direction of the edge

        Args:
            v (Vertex): one end of the edge

        Returns:
            Vertex: the other end of the edge
            None: if the edge is disconnected or the graph is directed and you're trying to go against the direction of the edge
        """
        if not self.connected:
            return None
        if self.v == v:
            return self.w
        elif self.directed:
            return None
        else:
            return self.v

    def backward(self, v):
        """returns a second end of the edge
        if directed - it returns the edge only if it's against the direction of the edge

        Args:
            v (Vertex): one end of the edge

        Returns:
            Vertex: the other end of the edge
            None: if the edge is disconnected or the graph is directed and you're trying to go in the direction of the edge
        """
        if not self.connected:
            return None
        if self.w == v:
            return self.v
        elif self.directed:
            return None
        else:
            return self.w

    def export(self):
        """export all important details about the edge

        Returns:
            dict: the exported data
        """
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
        if isinstance(other, int):
            return self.index == other
        return self.index == other.index

    def __repr__(self):
        return "Vertex(" + str(self.index) + ")"

    def neighbors(self, distance=False):
        if distance:
            return [(edge.forward(self.index), edge.weight) for edge in self.E if not edge.forward(self.index) is None]
        return [edge.forward(self.index) for edge in self.E if not edge.forward(self.index) is None]

    def backtracks(self, distance=False):
        if distance:
            return [(edge.backward(self.index), edge.weight) for edge in self.E if not edge.backward(self.index) is None]
        return [edge.backward(self.index) for edge in self.E if not edge.backward(self.index) is None]


class Graph:
    def __init__(self, N=0, values=[], multigraph=False, directed=False, weighted=False):
        self.N = N
        self.E = []
        self.is_multigraph = multigraph
        self.is_directed = directed
        self.is_weighted = weighted
        if len(values) != N:
            values = [i for i in range(N)]
        self.V = [Vertex(i, values[i]) for i in range(N)]

    def __repr__(self):
        return f"{self.N}-Graph(" + ", ".join([str(x) for x in self.E if x.connected]) + ")"

    def __eq__(self, other):
        if isinstance(other, Graph):
            return self.export_graph_data() == other.export_graph_data()

        if isinstance(other, dict):
            return self.export_graph_data() == other

        return False

    def connect(self, v, w, weight=1):
        """Connects two vertices with an edge

        Args:
            v (Vertex): one end of the edge
            w (Vertex): one end of the edge
        """
        if not self.is_weighted:
            weight = 1
        if self.is_multigraph or (not w in v.neighbors() and not v in w.neighbors() and not w == v):
            edge = Edge(v, w, self.is_directed, len(self.E), weight)
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
        if not index is None and -self.N <= index < self.N:
            index = index % self.N
            return self.V[index]
        if not value is None:
            for x in self.V:
                if x.value == value:
                    return x

        return None

    def dfs(self, v=None, past=None):
        """Depth first search (generator)

        Args:
            v (Vertex, optional): Starting point. Defaults to 0.

        Yields:
            Vertex: Vertices of the component one by one
        """
        if self.N == 0: raise Exception("No vertices to go through")
        if v is None:
            v = self.V[0]

        if past is None:
            past = [None for _ in range(self.N)]
        yield v
        past[v.index] = True
        for x in v.neighbors():
            if past[x.index] is None:
                for y in self.dfs(x, past=past):
                    yield y

    def bfs(self, v=None, priority=None, edge=False):
        """Breadth first search (generator)

        Args:
            v (Vertex, optional): Starting point. Defaults to 0.
            priority (function, optional): priority function to be applied to the vertices. Forces PriorityQueue, slows down the algorithm
            edge (bool, optional): option to also yield the neighbor from which the alg. got to that vertex and the distance to it
        Yields:
            Vertex: Vertices of the component one by one
        """
        if v is None:
            v = self.V[0]

        if priority is None:
            queue = Queue()
            queue.put(v)
        else:
            queue = PriorityQueue()
            queue.put((priority(v), v))

        past = [None for _ in range(self.N)]
        past[v.index] = True

        if edge:
            origin = [None for _ in range(self.N)]
            weight = [None for _ in range(self.N)]

        while not queue.empty():
            v = queue.get()
            if not priority is None:
                v = v[1]
            
            if edge:yield v, origin[v.index], weight[v.distance]
            else:yield v
            
            for x, d in v.neighbors(distance=True):
                if not past[x.index]:
                    past[x.index] = True

                    if edge and (weight[x.index] is None or weight[x.index] > d):
                        origin[x.index] = v
                        weight[x.index] = d

                    if priority is None:
                        queue.put(x)
                    else:
                        queue.put((priority(x), x))

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

        priority = (lambda x: x.distance) if self.is_weighted else None
        for w in self.bfs(v, priority):
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

        r = self.get_empty()
        r.add_vertex(u.value)
        n = 1

        if u.distance is None:return None

        while v != u:
            # only choose from those neighbors, whose paths are optimal
            u, w = min([x for x in u.backtracks(True) if (not x[0].distance is None) and u.distance -
                    x[0].distance == x[1]], key=lambda x: x[0].distance)
            d = u.distance

            #add the new vertex to the path and connect it with the last one
            r.add_vertex(u.value)
            r.connect(r.vertex(index=n), r.vertex(index=n-1), weight=w)
            n += 1

        return r

    def export_graph_data(self):
        """exports graph to JSON

        Returns:
            dict: everything important about the graph
        """
        parameters = {
            "N": self.N,
            "is_weighted": self.is_weighted,
            "is_multigraph": self.is_multigraph,
            "is_directed": self.is_directed
        }
        vertices = [v.value for v in self.V]
        edges = [e.export() for e in self.E if e.connected]
        return {"parameters": parameters, "vertices": vertices, "edges": edges}

    def import_graph_data(self, data):
        """imports graph from exported JSON

        Args:
            data (dict): graph data

        Raises:
            Exception: the data is invalid
        """
        if "parameters" in data.keys():
            parameters = data["parameters"]
            if "N" in parameters.keys():
                self.N = parameters["N"]
            if "is_weighted" in parameters.keys():
                self.is_weighted = parameters["is_weighted"]
            if "is_multigraph" in parameters.keys():
                self.is_multigraph = parameters["is_multigraph"]
            if "is_directed" in parameters.keys():
                self.is_directed = parameters["is_directed"]

        if "vertices" in data.keys():
            if self.N != len(data["vertices"]):
                raise ValueError("invalid number of vertices")
            self.V = [Vertex(i, data["vertices"][i]) for i in range(self.N)]

            if "edges" in data.keys():
                self.E = []
                for i in data["edges"]:
                    self.connect(self.vertex(i["v"]),
                                 self.vertex(i["w"]), i["weight"])

        elif "edges" in data.keys():
            raise ValueError("found edges, haven't found vertices")

    def add_vertex(self, value=None):
        if value is None:value = self.N
        self.V.append(Vertex(self.N, value))
        self.N += 1

    def get_empty(self):
        return Graph(0, multigraph=self.is_multigraph, directed=self.is_directed, weighted=self.is_weighted)

    def get_spanning_tree(self, v=None, minimal=False):
        """returns a spanning tree
        for disconnected graphs, it finds a spanning tree of a connected subgraph containing v.
        for directed, it finds spanning tree of a subgraph rooted in v.

        Args:
            v (Vertex, optional): Starting vertex of the algorithm. Defaults to the vertex with index 0.
        
        Returns:
            Graph: The spanning tree
        """
        priority = (lambda x: x.distance) if (self.is_weighted and minimal) else None
        generator = self.bfs(v, priority, edge=True)

        r = self.get_empty()
        vertex_map = [None for _ in range(self.N)]
        for vertex, starting, weight in generator:
            r.add_vertex(vertex.value)
            vertex_map[vertex.index] = r.N - 1
            if not starting is None:
                r.connect(
                    r.vertex(vertex_map[starting.index]), 
                    r.vertex(vertex_map[vertex.index]), 
                    weight)
        
        return r

    def get_induced_subgraph(self, vertices):
        """creates an induced subgraph from a list of vertices

        Args:
            vertices (list): list of vertices

        Returns:
            Graph: Induced subgraph
        """
        vertex_map = [None for _ in range(self.N)]
        g = self.get_empty()
        for x in vertices:
            vertex_map[x.index] = g.N
            g.add_vertex(x.value)

        for edge in self.E:
            u, v, w = vertex_map[edge.v.index], vertex_map[edge.w.index], edge.weight
            if u is None or v is None:pass
            else:
                u, v = g.vertex(index=u), g.vertex(index=v)
                g.connect(u, v, w)
        
        return g
    
    def get_component(self, v, vertex_map=None):
        """get a component containing v

        Args:
            v (Vertex): one vertex from the component
            vertex_map (list, optional): all vertices' original indices will be set to 1. Defaults to None.

        Returns:
            Graph: The component
        """
        r = self.bfs(v)
        if not vertex_map is None:
            r = list(r)
            for x in r:
                vertex_map[x.index] = 1

        return self.get_induced_subgraph(r)

    def get_components(self):
        """creates a list of all components

        Returns:
            list: a list containing Graphs - components of the parent graph
        """
        vertex_map = [None for _ in range(self.N)]

        r = []
        for i in range(len(vertex_map)):
            if vertex_map[i] is None:
                r.append(self.get_component(self.vertex(i), vertex_map))

        return r

            

if __name__ == '__main__':
    G = Graph(6, weighted=True)
    G.connect(G.vertex(0), G.vertex(1))
    G.connect(G.vertex(0), G.vertex(2))
    G.connect(G.vertex(0), G.vertex(3))
    G.connect(G.vertex(3), G.vertex(4))
    G.connect(G.vertex(3), G.vertex(5))
    G.connect(G.vertex(4), G.vertex(5))
    print(G)
    print("")
    print("DFS")
    for x in G.dfs():
        print(x)
    print("")
    print('BFS')
    for x in G.bfs():
        print(x)
    print()
    print('Distance')
    print(G.find_distance(G.vertex(0), G.vertex(5)))
    print(G.find_path(G.vertex(0), G.vertex(5)))
    print()
    print('Export')
    print(G.export_graph_data())
    print()
    print('Import')
    H = Graph(0)
    H.import_graph_data(G.export_graph_data())
    print(G.export_graph_data() == H.export_graph_data())
    print()
    print("Spanning Tree")
    G.connect(G.vertex(4), G.vertex(2))
    print(G)
    print(G.get_spanning_tree())
    G.add_vertex()
    print('Components')
    print(G.get_components())
