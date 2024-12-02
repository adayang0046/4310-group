# File for Banker's Algorithm

# Import tkinter which is the interface tool to showcase Banker's
import tkinter as tk
from tkinter import ttk


def create_graph(available, max_demand, allocation, n, m):
    # n is number of processes
    # m is number of resource types

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Banker's Algorithm")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Create headers for the tables
    ttk.Label(frame, text="Process", anchor="center").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(frame, text="Allocation", anchor="center").grid(row=0, column=1, padx=5)
    ttk.Label(frame, text="Max Demand", anchor="center").grid(row=0, column=2, padx=5)
    ttk.Label(frame, text="Available Resources", anchor="center").grid(row=0, column=3, padx=5)

    # Configure grid weights
    frame.grid_columnconfigure(0, weight=1, uniform="equal")
    frame.grid_columnconfigure(1, weight=1, uniform="equal")
    frame.grid_columnconfigure(2, weight=1, uniform="equal")
    frame.grid_columnconfigure(3, weight=1, uniform="equal")

    # Populate the matrix tables
    for i in range(n):
        ttk.Label(frame, text=f"Process {i + 1}", anchor="center").grid(row=i + 1, column=0, padx=5, pady=5)
        
        # Allocation matrix 
        allocation_row = " ".join(str(allocation[i][j]) for j in range(m))
        ttk.Label(frame, text=allocation_row, anchor="center").grid(row=i + 1, column=1, padx=5, pady=5)

        # Max Demand matrix 
        max_demand_row = " ".join(str(max_demand[i][j]) for j in range(m))
        ttk.Label(frame, text=max_demand_row, anchor="center").grid(row=i + 1, column=2, padx=5, pady=5)

    # Available Resources table
    available_row = " ".join(str(available[j]) for j in range(m))
    ttk.Label(frame, text=available_row, anchor="center").grid(row=1, column=3, padx=5, pady=5)

    # Check if the system is in a safe state
    is_safe_state, safe_sequence = is_safe(n, m, available, max_demand, allocation)

    # Display Safe State Result
    safe_state_message = "The system is in a SAFE state." if is_safe_state else "The system is NOT in a SAFE state."
    ttk.Label(frame, text="System State:", anchor="center").grid(row=n + 4, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Label(frame, text=safe_state_message, anchor="center", foreground="green" if is_safe_state else "red").grid(
        row=n + 4, column=1, sticky=tk.W, padx=5, pady=5
    )

    # Display Safe Sequence if in a safe state
    if is_safe_state:
        ttk.Label(frame, text="Safe Sequence:", anchor="center").grid(row=n + 5, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(
            frame, text=", ".join(f"P{p + 1}" for p in safe_sequence), anchor="center"
        ).grid(row=n + 5, column=1, sticky=tk.W, padx=5, pady=5)

    # Start tkinter
    root.mainloop()
   
# Method to calculate the need matrix
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

    create_graph(available, max_demand, allocation, n, m)


#run main function to use Banker's Algorithm!
main()
