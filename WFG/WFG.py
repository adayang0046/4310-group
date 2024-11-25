
# pip install networkx matplotlib
import matplotlib.pyplot as plot # type: ignore
import networkx as nx # type: ignore

# Reference: https://www.geeksforgeeks.org/wait-for-graph-deadlock-detection-in-distributed-system/
# Reference for dfs: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/ 

# The below three methods create_graph, create_edge and delete_edge
# are for a more dynamic approach

# def create_graph():
#     return {} # empty graph

# def create_edge(): # Adding edges to simulate processes waiting on each other
#     ...

# def delete_edge():
#     ...

# Function for illustrating the graph
def draw_graph(adj, deadlock):
   
   # Create a directed graph using NetworkX
    Graph = nx.DiGraph()
    
    # Add edges based on adjacency list
    for process, dependencies in enumerate(adj):
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
    # Hardcoded example for now -- create dynamic later

    V = 4  # Number of vertices (processes) - change if processes are added/deleted

    # Create an adjacency list for the graph
    adj = [[] for _ in range(V)]

    # Define edges representing process dependencies
    edges = [
        [0, 1],  # Process 0 waits for Process 1
        [1, 2],  # Process 1 waits for Process 2
        [2, 3],  # Process 2 waits for Process 3
        [3, 0],  # Process 3 waits for Process 0 (cycle)
        #[4, 5],  # Process 4 waits for Process 5 (no cycle)
    ]

    # Populate the adjacency list with edges
    for e in edges:
        adj[e[0]].append(e[1])

    deadlock = None
    if detect_deadlock(adj, V):
        deadlock = "Deadlock detected!"
    else:
        deadlock = "No deadlock detected."

    draw_graph(adj, deadlock)

main()