# File for Banker's Algorithm
# This function calculates the need matrix
import matplotlib.pyplot as plot # type: ignore
import networkx as nx # type: ignore

def create_graph(edges, V):
    ... 

def calculate_need(num_processes, num_resources, max_demand, allocation):
    need_list = []
    for i in range(num_processes):
        each_need = []
        for j in range(num_resources):
            each_need.append(max_demand[i][j] - allocation[i][j])
        need_list.append(each_need)
    # Returns a 2D array
    return need_list

# This function checks if a system is in safe state
def is_safe(num_processes, num_resources, available, max_demand, allocation):

    # Calculate the need matrix
    need = calculate_need(num_processes, num_resources, max_demand, allocation)

    # Initialize all tracking attributes
    working_avaliable = available[:] 
    # Tracks if each processes completed 
    finish = [False] * num_processes      

    safe_sequence = []

    while len(safe_sequence) < num_processes:

        # Tracks if in safe state
        found_process = False
        
        for i in range(num_processes):
            if not finish[i]:              
                if all(need[i][j] <= working_avaliable[j] for j in range(num_resources)):
                    # If the current is avaliable, a process can be executed  
                    print(f"Process {i} execute. Allocated: {allocation[i]}.")
                    # Add free instances of the current process to calculate the new avaliable
                    for j in range(num_resources):
                        working_avaliable[j] += allocation[i][j]

                    # Finish the current executing, update the running order
                    finish[i] = True
                    safe_sequence.append(i)
                    print(f"After Process {i} executes: {working_avaliable}\n")

                    # Indicate a process can be execute
                    found_process = True
                    break

        
        if not found_process:
            print("System is NOT in a safe state.\n")
            return False, []

    print("The system is in a safe state.\n")
    return True, safe_sequence

# def main():
#     # Hardcoded
#     n = 4  # Number of processes
#     m = 3  # Number of resource types

#     # Data structures
#     available = [3, 3, 2]  # Available vector (length m)
#     max_demand = [         # Max matrix (n x m)
#         [7, 5, 3],
#         [3, 2, 2],
#         [9, 0, 2],
#         [2, 2, 2],
#         [4, 3, 3]
#     ]
#     allocation = [         
#         [0, 1, 0],
#         [2, 0, 0],
#         [3, 0, 2],
#         [2, 1, 1],
#         [0, 0, 2]
#     ]


#     is_safe_state, safe_sequence = is_safe(n, m, available, max_demand, allocation)

#     # Print results
#     if is_safe_state:
#         print("The order of execute is:", safe_sequence)
#     else:
#         print("The system is NOT in a safe state.")

#function for getting user input
def get_user_input():
    #ask user to enter # of processes and # of resource types
    n = int(input("Enter the number of processes: "))
    m = int(input("Enter the number of resource types: "))

    #ask user for # of available resources
    available = list(map(int, input(f"Enter the {m} available resources (space separated): ").split()))

    #ask user for max matrix demand
    print(f"Enter the maximum demand matrix ({n} processes, {m} resource types):")
    max_demand = []
    for i in range(n):
        max_demand.append(list(map(int, input(f"Enter max demand for process {i} (space separated): ").split())))

    #ask user for allocation matrix
    print(f"Enter the allocation matrix ({n} processes, {m} resource types):")
    allocation = []
    for i in range(n):
        allocation.append(list(map(int, input(f"Enter allocation for process {i} (space separated): ").split())))

    return n, m, available, max_demand, allocation


def main():
    #user input for processes, resources, and matrices
    n, m, available, max_demand, allocation = get_user_input()

    #check system safety/safe sequence if appl.
    is_safe_state, safe_sequence = is_safe(n, m, available, max_demand, allocation)

    #print outcome(if safe>, if unsafe>)
    if is_safe_state:
        print("The order of execution (safe sequence) is:", safe_sequence)
    else:
        print("The system is NOT in a safe state.")


#run main function to use Banker's Algorithm!
main()
