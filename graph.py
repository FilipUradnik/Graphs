from queue import Queue


class Vertex:
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

    def __init__(self, index):
        self.index = index
        self.E = []
        self.distance = None

    def connect(self, v):
        if not v in self.E:
            self.E.append(v)


class Graph:
    def __init__(self, N):
        self.N = N
        self.V = [Vertex(i) for i in range(N)]
        self.distances_found = False

    def connect(self, v, w):
        """Connects two vertices with an edge

        Args:
            v (Vertex): one end of the edge
            w (Vertex): one end of the edge
        """
        v, w = self.vertex(v), self.vertex(w)
        v.connect(w)
        w.connect(v)

    def vertex(self, v):
        """gets a Vertex object with a given index

        Args:
            v (int): Index of the vertex

        Returns:
            Vertex: Vertex with the given index
        """
        if not isinstance(v, Vertex):
            v = self.V[v]
        return v

    def get_neighbors(self, v):
        """Returns neighbors of a given vertex

        Args:
            v (Vertex)

        Returns:
            list: A list of vertices neighboring v
        """
        v = self.vertex(v)
        return self.V[v.index].E.copy()

    def dfs(self, v=0, past=None):
        """Depth first search (generator)

        Args:
            v (Vertex, optional): Starting point. Defaults to 0.

        Yields:
            Vertex: Vertices of the component one by one
        """
        v = self.vertex(v)
        if past is None:
            past = [None for _ in range(self.N)]
        yield v
        past[v.index] = True
        for x in self.get_neighbors(v):
            if past[x.index] is None:
                self.dfs(x, past=past)

    def bfs(self, v=0, queue=None):
        """Breadth first search (generator)

        Args:
            v (Vertex, optional): Starting point. Defaults to 0.
            queue (Queue-like, optional): Custom Queue-like object, for example PriorityQueue. Defaults to Python Queue.

        Yields:
            Vertex: Vertices of the component one by one
        """
        v = self.vertex(v)
        if queue is None:
            queue = Queue()
        past = [None for _ in range(self.N)]
        queue.put(v)
        past[v.index] = True
        while not queue.empty():
            v = queue.get()
            yield v
            for x in v.E:
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
