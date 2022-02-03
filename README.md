# Graphs
This is a package enabling users to do basic operations with graphs.
## Graph requirements
This package supports all sorts of graphs, including weighted graphs, multigraphs and directed graphs. A drawback to that is that some implemented algorithms could be more efficient if they were specified only for non-multigraphs, for example. 

What I'm saying is, this isn't meant to handle huge graphs super quickly (for start, it's written in Python). 

## Features
* Saving/loading a graph to/from a file (human-readable JSON format)
* BFS, DFS
* Finding the shortest path between two vertices
* Finding the distance between two vertices
* Adding vertices and edges to already loaded graphs
* Getting induced subgraphs
* Splitting a graph to components
* Finding a spanning tree to a graph (minimal spanning tree in weighted graphs)

## Command-line testing interface
You can try the package out or test it by running the command-line interface. You do that by running `main.py` with at least Python 3.9 (older versions not tested).

There is a menu with a `HELP` command included, there you can find a description to all the commands.

## Help
if you're running the command-line interface, use the `HELP` command. If you're implementing it into your own project, read the module description written below, or look in the main source code (graph.py). Each function has a detailed Docstring explaining what it does. 

In case you still run into issues, you can open a new issue on Github or you can message me at filip.uradnik9@gmail.com

## Module description

### Edge

Stores information about an edge, including weight and the order of vertices, even in non-weighted non-directed graphs. 

You can, in principle, force an edge of a non-weighted graph to have a different weight than one, but it is not advised because when finding the shortest path, the weight will not be taken into account if the overall graph's `is_weighted` attribute is set to `False`. Similarly, you can force just one edge of a graph to be directed, by setting its `directed` attribute. 

The `forward` and `backward` functions take as an argument a vertex - one end of the edge. They return the other vertex. When the graph is directed, `forward` returns the vertex only if moving from the input vertex to the output vertex would be in the direction of the edge (ie. it would be possible to use the edge to go from the input vertex to the output vertex). `backward` returns it only if it would be against the direction of the edge.

### Vertex

Stores information about a vertex. It is not recommended to directly edit the `E` attribute, instead, use `neighbors` and `backtracks`. 

Identically to `forward` and `backward` in `Edge`, `neighbors` and `backtracks` are indentical when the graph is not directed and when it is, `neighbors` lists all neighbors, to which you can go from the vertex and `backtracks` lists all neighbors, from which you can arrive at the vertex. 

Both functions also include the optional `distance` parameter. When set to `True`, the function returns a list of tuples in format `(vertex, weight)`, where `weight` is the weight of the edge connecting them.

### Graph

The main class you should use when implementing the module in your program. When you create a `Graph` object, DO NOT manually change any of the attributes directly. 

The attribute `N` represents the number of vertices and changes dynamically. `V` and `E` are lists of vertices and edges. These can be altered to some extend. 
You can add edges by `connect(v1, v2)`, where `v1` and `v2` are vertices of the graph. You can add vertices by `add_vertex(value)` (where `value` is a value to be stored in the vertex, optional). 

Vertices CANNOT be removed from the graph. If you want to remove an edge, do so by manually setting its `connected` attribute to `False`. 

`vertex` is used to retrieve a vertex by its `id` (natural numbers starting from 0) or `value` (in that case be wary of having vertices with duplicate values).

`dfs` and `bfs` are functions returning a Python generator for vertices in the order of depth first search or breath first search. You can specify which vertex to start with (defaults to the one with index 0). In `bfs` you can specify a priority function for the PriorityQueue in use (if not specified, it uses a normal Queue), and whether you also want info about the edge from which the algorithm arrived at that vertex.

In `dfs` you can specify `past`, which is a list of length `N`, where the algorithm will store `True` for every vertex it yields. This is an inner feature needed for the functioning of the algorithm, not recommended to use, but might come in handy.

The `find_distance` function uses the Dijkstra's algorithm (with PriorityQueue, or normal Queue for non-oriented graphs) and sets the `distance` attribute of each vertex to either the distance from starting vertex, or `None`. `find_path` then uses backtracking to find the shortest path and returns it as a graph (it creates a graph to preserve the edges lengths, if you need a set of vertices, use `bfs` on the new graph from the starting vertex).

The `export_graph_data` and `import_graph_data` functions convert the graph to/from a nice human-readable JSON format. 

#### Subgraphs

The `get_component`, `get_components`, `get_spanning_tree` and `get_induced_subgraph` all create various subgraphs of the original graph. 

The `get_induced_subgraph` function takes a list of vertices, puts them into a new graph and it goes through all the edges and when both ends of the edge are in the new graph, it adds the edge.

The `get_component` function uses `bfs` to get all the vertices connected to each other and then returns their induced subgraph. 

The `get_components` function uses a vertex map - a list of length `N` (number of vertices in the graph) - passes it to `get_component`, there for every vertex from the bfs generator `vertex_map[vertex.index]` to `True`. `get_components` repeats that with another vertex that doesn't have `vertex_map[vertex.index] == True` until all the spots in vertex_map are set to `True` - then the whole graph has been searched and split to components.

The `get_spanning_tree` function finds a spanning tree using bfs. For weighted graphs you can set the `minimum` argument to `True` to find the minimum spanning tree using the Prim–Jarník algorithm (similarly to Dijkstra's algorithm, it does so by using `PriorityQueue` instead of `Queue` in the bfs, effectively always choosing the edge with minimal weight)

Finally the `get_empty` function returns an empty graph with the exact same parameters as the original (apart from the number of vertices, of course).