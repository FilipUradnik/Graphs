from queue import Queue

class Edge:

    def __init__(self, v, w, oriented, index, weight=1):
        self.connected = True
        self.index = index
        self.weight = weight
        self.v = v
        self.w = w
        self.oriented = oriented

    def forward(self, v):
        if self.v == v:return self.w
        elif self.oriented: return None
        else:return self.v

    def backward(self, v):
        if self.w == v:return self.v
        elif self.oriented: return None
        else:return self.w

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

    @property
    def neighbors(self):
        return [edge.forward(self.index) for edge in self.E if not edge is None]

class Graph:
    def __init__(self, N, values=[], multigraph=False, oriented=False, weighted=False):
        self.N = N
        self.E = []
        self.is_multigraph = multigraph
        self.is_oriented = oriented
        self.is_weighted = weighted
        if len(values) != N:values = [i for i in range(N)]
        self.V = [Vertex(i, values[i]) for i in range(N)]

    def connect(self, v, w, weight=1):
        """Connects two vertices with an edge

        Args:
            v (Vertex): one end of the edge
            w (Vertex): one end of the edge
        """
        if not self.is_oriented:weight = 1
        if self.is_multigraph or (not w in v.neighbors and not w == v):
            edge = Edge(v, w, self.is_oriented, len(self.E), weight)
            self.E.append(edge)
            v.E.append(edge)
            if not self.is_oriented:w.E.append(edge)

    def vertex(self, index=None, value=None):
        """gets a Vertex object with a given index or value

        Args:
            v (int): Index of the vertex

        Returns:
            Vertex: Vertex with the given index
        """
        if index is None and value is None:return None

        if not index is None:return self.V[index]

    def get_neighbors(self, v):
        """Returns neighbors of a given vertex

        Args:
            v (Vertex)

        Returns:
            list: A list of vertices neighboring v
        """
        return 

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
        for x in v.neighbors:
            if past[x.index] is None:
                for y in self.dfs(x, past=past):yield y

    def bfs(self, v=None, queue=None):
        """Breadth first search (generator)

        Args:
            v (Vertex, optional): Starting point. Defaults to 0.
            queue (Queue-like, optional): Custom Queue-like object, for example PriorityQueue. Defaults to Python Queue.

        Yields:
            Vertex: Vertices of the component one by one
        """
        if v is None:v = self.V[0]

        if queue is None:
            queue = Queue()

        past = [None for _ in range(self.N)]
        queue.put(v)
        past[v.index] = True
        while not queue.empty():
            v = queue.get()
            yield v
            for x in v.neighbors:
                if not past[x.index]:
                    past[x.index] = True
                    queue.put(x)

    def find_distance(self, v, u=None):
        """Finds distance between two vertices, sets the value of "distance" of every vertex to its distance from v

        Args:
            v (Vertex): The vertex from which to calculate the distance
            u (Vertex, optional): The vertex to which to calculate the distance. Defaults to None.

        Returns:
            int: Distance from u to v. None if there is no path between them or u wasn't specified
        """
        v, u = self.vertex(v), self.vertex(u)
        for x in self.V:
            x.distance = None
        v.distance = 0

        for w in self.bfs(v):
            for x in w.E:
                if x.distance is None:
                    x.distance = x.distance + 1
                    if (not u is None) and x == u:
                        return w.distance

    def find_path(self, v, u):
        """Finds the shortest path between two vertices

        Args:
            v (Vertex): Starting point
            u (Vertex): Ending point

        Returns:
            list: List of vertices through which the path leads
        """
        v, u = self.vertex(v), self.vertex(u)
        d = self.find_distance(v, u)
        if d is None:
            return None

        r = [u]
        while d != 0:
            u = min(u.E)
            d = u.distance
            r.append(u)

        return r[::-1]

if __name__ == '__main__':
    G = Graph(6)
    G.connect(G.vertex(0), G.vertex(1))
    G.connect(G.vertex(0), G.vertex(2))
    G.connect(G.vertex(0), G.vertex(3))
    G.connect(G.vertex(3), G.vertex(4))
    G.connect(G.vertex(3), G.vertex(5))
    G.connect(G.vertex(4), G.vertex(5))
    print("DFS")
    for x in G.dfs():print(x)
    print(); print('BFS')
    for x in G.bfs():print(x)
    print(); print('BFS')
