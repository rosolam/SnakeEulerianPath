import networkx as nx
import matplotlib.pyplot as plt

# Define the grid size
GRID_SIZE = 24

# Initialize the graph
G = nx.Graph()

# Add nodes to the graph
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        G.add_node((x, y))

# Add edges to the graph
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE - 1):
        G.add_edge((x, y), (x, y + 1))
        G.add_edge((y, x), (y + 1, x))

# Remove alternating border edges
# Top border
for x in range(1, GRID_SIZE - 1, 2):
    G.remove_edge((x, 0), (x + 1, 0))

# Bottom border
for x in range(1, GRID_SIZE - 1, 2):
    G.remove_edge((x, GRID_SIZE - 1), (x + 1, GRID_SIZE - 1))

# Left border
for y in range(1, GRID_SIZE - 1, 2):
    G.remove_edge((0, y), (0, y + 1))

# Right border
for y in range(1, GRID_SIZE - 1, 2):
    G.remove_edge((GRID_SIZE - 1, y), (GRID_SIZE - 1, y + 1))

# Plot the graph
pos = {node: node for node in G.nodes()}  # Position nodes as per their coordinates

def draw_graph(graph, pos):
    plt.figure(figsize=(12, 12))
    nx.draw(graph, pos, node_size=20, node_color='black', edge_color='gray', with_labels=False)
    plt.show()

# Draw the graph
draw_graph(G, pos)

# Debug: Check node degrees
print("Node degrees:")
odd_degree_nodes = []
for node, degree in G.degree():
    if degree % 2 != 0:
        odd_degree_nodes.append(node)
        print(f"Node {node} has degree {degree}")

if odd_degree_nodes:
    print(f"Odd degree nodes: {odd_degree_nodes}")
else:
    print("All nodes have even degrees.")

# Check if the graph is Eulerian
if not nx.is_eulerian(G):
    print("The graph is not Eulerian. Please adjust the edges.")
    exit()

# Generate the Eulerian path
eulerian_path = list(nx.eulerian_circuit(G))

# Plot the Eulerian circuit with path indices on edges
def draw_path_with_indices(path, pos):
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, node_size=20, node_color='black', edge_color='gray', with_labels=False)
    
    edge_labels = {}
    for i in range(len(path) - 1):
        edge_labels[(path[i], path[i + 1])] = str(i)
    edge_labels[(path[-1], path[0])] = str(len(path) - 1)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=7)
    
    plt.show()

# Extract the path and visualize it with indices
path_nodes = [edge[0] for edge in eulerian_path] + [eulerian_path[-1][1]]
draw_path_with_indices(path_nodes, pos)
