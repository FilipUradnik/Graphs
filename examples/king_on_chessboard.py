from graph import Graph
"""
given a list of obsticles, find the shortest path of a king from start to end points.
"""
class Chessboard:

    def __init__(self, obsticles):
        # vertices represent squares, sorted line by line
        self.g = Graph(64)
        self.obsticles = [x-1 + (y-1)*8 for x,y in obsticles]
        
        for i in range(64):
            if i%8 != 7:
                self.connect_spaces(i, i+1)
            if i < 56:
                self.connect_spaces(i, i+8)
            if i%8 != 7 and i < 56:
                self.connect_spaces(i, i+9)

    def connect_spaces(self, i, j):
        if not (i in self.obsticles or j in self.obsticles):
            self.g.connect(self.g.vertex(i), self.g.vertex(j))

    def calculate_path(self, start, end):
        start, end = start[0]-1 + (start[1]-1)*8, end[0]-1 + (end[1]-1)*8
        path = self.g.find_path(self.g.vertex(start), self.g.vertex(end))
        path_as_vertices = path.bfs(path.vertex(-1))
        
        r = []
        for vertex in path_as_vertices:
            x = vertex.value % 8 + 1
            y = vertex.value//8 + 1
            r.append([x, y])

        return r


obsticles = [
    [2, 2],
    [2, 1],
    [2, 3],
]

start = [1, 1]
end = [3, 3]

chb = Chessboard(obsticles)

print(chb.calculate_path(start, end))