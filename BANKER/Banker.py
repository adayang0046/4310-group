# File for Banker's Algorithm
# This function calculates the need matrix
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


def main():
    # Hardcoded
    # Example setup this example is given by chatgpt
    n = 5  # Number of processes
    m = 3  # Number of resource types

    # Data structures
    available = [3, 3, 2]  # Available vector (length m)
    max_demand = [         # Max matrix (n x m)
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    allocation = [         
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]


    is_safe_state, safe_sequence = is_safe(n, m, available, max_demand, allocation)

    # Print results
    if is_safe_state:
        print("The order of execute is:", safe_sequence)
    else:
        print("The system is NOT in a safe state.")

main()
