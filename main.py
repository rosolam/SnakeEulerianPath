import networkx as nx
import matplotlib.pyplot as plt
import random
import csv

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

# Shuffle the order of edges to introduce randomness
edges = list(G.edges())
random.shuffle(edges)
G = nx.Graph()
G.add_edges_from(edges)

# Plot the graph
pos = {node: node for node in G.nodes()}  # Position nodes as per their coordinates

def draw_graph(graph, pos):
    plt.figure(figsize=(12, 12))
    nx.draw(graph, pos, node_size=20, node_color='black', edge_color='gray', with_labels=False)
    plt.show()

# Draw the graph
#draw_graph(G, pos)

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

# Generate the Eulerian path using networkx function
eulerian_path = list(nx.eulerian_circuit(G))

# Save the Eulerian path to a CSV file
def save_path_to_csv(path, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for edge in path:
            writer.writerow([f"{edge[0][0]},{edge[0][1]}", f"{edge[1][0]},{edge[1][1]}"])

# Save the path to CSV
save_path_to_csv(eulerian_path, 'path_data.csv')

# Plot the Eulerian circuit with path indices on edges
def draw_path_with_indices(path, pos, filename):
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, node_size=20, node_color='black', edge_color='gray', with_labels=False)
    
    edge_labels = {}
    for i, (u, v) in enumerate(path):
        edge_labels[(u, v)] = str(i)
    
    nx.draw_networkx_edges(G, pos, edgelist=path, edge_color='blue', width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=7)
    
    plt.savefig(filename)

    plt.show()

# Visualize the random Eulerian path with indices
draw_path_with_indices(eulerian_path, pos, "eulerian_path.png")