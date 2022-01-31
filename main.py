#! /bin/python3

import command_interface, graph
import json, pathlib, os
GRAPHS = {}

# -------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------

def _save_graph(name, g, exclusive=False):
    if exclusive:
        while name in GRAPHS.keys():name += "_"
        GRAPHS[name] = g
    elif (not name in GRAPHS.keys()) or command_interface.get_bool(input("A graph with that name already exists. Replace it?")):
        GRAPHS[name] = g

def _get_graph(name):
    if name in GRAPHS.keys():return GRAPHS[name]
    else:raise Exception("Graph Not Found")

# -------------------------------------------------------------------
# USER INPUT HANDLERS
# -------------------------------------------------------------------

def new_graph(name, N, we, mul, ori, vals):
    if vals:v = [input(f"Vertex {i+1}: ") for i in range(N)]
    else:v = []
    g = graph.Graph(N, v, mul, ori, we)
    
    _save_graph(name, g)
    print("To add edges, use command add_edge [graph_name] [starting_vertex_index] [ending_vertex_index]")

def add_edge(name, v1, v2):
    g = _get_graph(name)

    if g.is_weighted:w = float(input("weight: "))
    else:w = 1
    if w == int(w):w = int(w)
    g.connect(g.vertex(v1), g.vertex(v2), w)
    

def list_graphs():
    for name, graph in GRAPHS.items():
        print("V:", graph.N, "E:", len(graph.E), "NAME:", name)

def get_vertex_indices(name):
    g = _get_graph(name)
    for i, x in enumerate(g.V):
        print(str(i) + ":", x.value)

def print_graph(name):
    g = _get_graph(name)
    print("---INDICES------")
    get_vertex_indices(name)
    print()
    print("---EDGES--------")
    for e in g.E:
        print(e.visualize())

def import_graph(name, file_path, exclusive=False):
    with open(file_path) as f:
        g_data = json.load(f)

    g = graph.Graph()
    g.import_graph_data(g_data)
    _save_graph(name, g, exclusive)

def export_graph(name, path):
    g = _get_graph(name)
    
    with open(path, "w") as f:
        json.dump(g.export_graph_data(), f, indent=4)

def export_all(path):
    path = pathlib.Path(path)
    if not path.exists():
        os.makedirs(path)
    for x in GRAPHS.keys():
        export_graph(x, path / (x + ".json"))

def import_all(path):
    path = pathlib.Path(path)
    for x in os.listdir(path):
        name = x[:-5] if x.endswith(".json") else x
        import_graph(name, path / x, exclusive=True)

def split_to_components(name):
    g = _get_graph(name)

    components = g.get_components()
    for x, i in enumerate(components):
        _save_graph(name + "_component_" + str(i+1), x, True)


def find_distance(name, u, v):
    g = _get_graph(name)
    print(g.get_distance(g.vertex(u), g.vertex(v)))

def find_path(name, u, v):
    g = _get_graph(name)
    path_graph = g.find_path(g.vertex(u), g.vertex(v))
    
    if path_graph is None: print("Path doesn't exist")
    else:
        for x in path_graph.bfs(path_graph.vertex(-1)):
            print(f"Vertex {x.value}")

# -------------------------------------------------------------------
# MENU
# -------------------------------------------------------------------

menu = command_interface.Interface()

menu.add_commands([
    ["list_graphs",list_graphs, "get a list of all graphs in memory"],
    ["print_graph name",print_graph, "prints a graph (as best as it can)"],
    ["new_graph name number_of_vertices:int weighted:bool multigraph:bool directed:bool values_in_vertices:bool",new_graph, "add a new graph to memory"],
    ["get_vertex_indices name",get_vertex_indices, "get list of vertices of a graph, along with their indices"],
    ["add_edge name starting_vertex_index:int end_vertex_index:int",add_edge, "creates a new edge in a graph, for weighted graphs you will be prompted for the weight as well"],
    ["import_graph name file_path",import_graph, "import a graph from a json file specified by file_path"],
    ["export_graph name file_path",export_graph, "export a graph to a json file, location specified by file_path"],
    ["export_all dir_name",export_all, "export all graphs from memory to a directory"],
    ["import_all dir_name",import_all, "import all files from a specified directory to memory (there cannot be any other files in the directory!)"],
    ["split_to_components name",split_to_components, "split a graph to components and save them to memory (the old graph will remain in memory, the components will be called [original_name]_component_[component_number]"],
    ["find_distance name index_of_start:int index_of_end:int",find_distance, "find a distance between two vertices (vertices are specified by their indices, for more info look at get_vertex_indices command)"],
    ["find_path name index_of_start:int index_of_end:int",find_path, "find a shortest path between two vertices (vertices are specified by their indices, for more info look at get_vertex_indices command)"],
])

while True:
    try:
        if menu.input_from_menu() == "EXIT":break
    except Exception as e:
        print(e)
        input("Press ENTER to continue...") 
