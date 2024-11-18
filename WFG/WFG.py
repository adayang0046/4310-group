

# Reference: https://www.geeksforgeeks.org/wait-for-graph-deadlock-detection-in-distributed-system/
# We can change the format, this is just what seemed easiest so far

# The below three methods create_graph, create_edge and delete_edge
# are for a more dynamic approach

# def create_graph():
#     return {} # empty graph

# def create_edge(): # Adding edges to simulate processes waiting on each other
#     ...

# def delete_edge():
#     ...

def dfs(): # Perform DFS
    ...

def detect_deadlock(): # We will use DFS approach 
    ...

def main():
    # Hardcoded example

    graph = {
        "P1": ["P2"], # P1 waiting on P2
        "P2": ["P3"], # P2 waiting on P3
        "P3": ["P4"], # P3 waiting on P4
        "P4": ["P1"], # P4 waiting on P1 creating the deadlock cycle
        # "P4": ["P5"], # To test no cycle 
    }

    if detect_deadlock(graph):
        print("A deadlock has been detected in the system.")
    else:
        print("No deadlock has been detected in the system.")

main()