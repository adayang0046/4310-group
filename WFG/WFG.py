
# pip install networkx matplotlib
import matplotlib.pyplot as plot # type: ignore
import networkx as nx # type: ignore
import random

# Reference: https://www.geeksforgeeks.org/wait-for-graph-deadlock-detection-in-distributed-system/
# Reference for dfs: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/ 

# Function for creating a new graph using networkx direcxted graph funciton
def create_graph(edges, V):
    adj = {i : [] for i in range(V)}
    Graph = nx.DiGraph()

    for from_node, to_node in edges:
        create_edge(adj, from_node, to_node)
        Graph.add_edge(from_node, to_node)

    return adj, Graph

# Function for adding an edge to the adj list
def create_edge(adj, from_node, to_node): 
    if from_node not in adj:
        adj[from_node]= []
    if to_node not in adj:
        adj[to_node] = []
    
    adj[from_node].append(to_node)


# Function for deleting an edge 
def delete_edge(adj, from_node, to_node):
    if from_node < len(adj):
        if to_node in adj[from_node]:
            adj[from_node].remove(to_node)

# Function for illustrating the graph
def draw_graph(adj, deadlock):
   
   # Create a directed graph using NetworkX
    Graph = nx.DiGraph()
    
    # Add edges based on adjacency list
    for process, dependencies in adj.items():
        for dependency in dependencies:
            Graph.add_edge(process, dependency)
    
    # Use circular_layout for display
    pos = nx.circular_layout(Graph)
    
    # Create labels for the process numbers
    labels = {node: f"P{node}" for node in Graph.nodes()}
    
    # Draw the graph with specifications
    plot.figure(figsize=(8, 8))
    nx.draw(
        Graph, 
        pos, 
        labels=labels, 
        with_labels=True, 
        node_size=2000, 
        node_color="red", 
        font_size=10, 
        font_weight="bold", 
        arrowsize=20
    )

    if deadlock:
        # Add text for the output -- deadlock detected or not
        plot.text(0.5, 1.05, deadlock, horizontalalignment='center', verticalalignment='bottom', fontsize=12, color="black", weight="bold")
    
    # Display the graph
    plot.title("Wait-For Graph")
    plot.show()


def dfs_rec(adj, visited, node, recList):
    visited[node] = True
    recList[node] = True # rec_stack to avoid false detection

    # Look through adjacent nodes
    for i in adj[node]:
        if not visited[i]:
            if dfs_rec(adj, visited, i, recList):
                return True
        elif recList[i]:
            return True  # Cycle detected

    recList[node] = False  # Backtrack
    return False


def detect_deadlock(adj, V):
    visited = [False] * V
    recList = [False] * V  # Tracks nodes in the current recursion stack

    for node in range(V):
        if not visited[node]:
            if dfs_rec(adj, visited, node, recList):
                return True  # Cycle detected
    return False

def main():
    while True:
        # Ask the number of vertices and check for invalid input
        try:
            V = int(input("Enter the number of vertices (V): "))
            if V <= 0:
                raise ValueError("The number of vertices must be positive.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

    # Ask if user would like to:
    # A: auto generate edges
    # B: input edges in terminal
    print("\nHow would you like to add edges?\nA: Have this program to auto-generate edges\nB: Manually input edges")
    # Collect choice and check for invalid input
    while True:
        choice = input("Enter your choice (A/B): ").strip().upper()
        if choice in ['A', 'B']:
            break
        print("Invalid choice. Please enter 'A' or 'B'.")
    
    # An empty list for edges
    edges = []
    if choice == 'A':
        # Auto-generate edges
        num_edges = random.randint(V, V * 2)  # Generate a random number of edges

        for _ in range(num_edges):
            from_node = random.randint(0, V - 1)
            to_node = random.randint(0, V - 1)
            while from_node == to_node:  # Avoid self-loops
                to_node = random.randint(0, V - 1)
            edges.append((from_node, to_node))

        print(f"Generated edges: {edges}")
    elif choice == 'B':
        # Manually input edges
        print("Enter edges in the format 'from_node to_node' (For example: 2 1). \nEnter 'end' to finish.\nNote: Nodes must be within the range of 0 to V-1.\n")
        while True:
            edge_input = input("Enter edge: ").strip()
            if edge_input.lower() == "end":
                break
            try:
                from_node, to_node = map(int, edge_input.split())
                if from_node < 0 or from_node >= V or to_node < 0 or to_node >= V:
                    raise ValueError("Nodes must be within the range of 0 to V-1.")
                edges.append((from_node, to_node))
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")


    adj, Graph = create_graph(edges, V)

    # Print the list
    print("\nAdjacency List:")
    for node, dependencies in adj.items():
        print(f"{node}: {dependencies}")


    deadlock = None
    if detect_deadlock(adj, V):
        deadlock = "Deadlock detected!"
        print(f"\n{deadlock}")
    else:
        deadlock = "No deadlock detected."
        print(f"\n{deadlock}")

    draw_graph(adj, deadlock)
    
    return
    

main()