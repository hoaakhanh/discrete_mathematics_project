import time

# Start benchmarking timers
start_ni = time.perf_counter()
start_ls = time.perf_counter()

class Instance:
    nodes = []
    euclid_distance = []

    def __init__(self):
        self.nodes = []
        self.euclid_distance = []

    # Get information from the data file:
    def get_info(self):
        with open ("att48.tsp", "r") as file:
            lines = file.readlines()
            
            for i in range(len(lines) - 1):
                line = lines[i]
                if line == '' or line[0].isalpha():
                    continue

                # Get information: node index, x-coordinate, y-coordinate
                node, x, y = line.split()
                node = int(node)
                x = float(x)
                y = float(y)
                self.nodes.append((x, y))

        return self.nodes
    
    # Calculate Euclidean distance between two nodes
    def calc_euclid_distance(self, u, v):
        return ((self.nodes[u][0] - self.nodes[v][0])**2 +(self.nodes[u][1]- self.nodes[v][1])**2)**0.5
    
    # Create the complete symmetric distance matrix
    def create_matrix(self):
        n = len(self.nodes)

        self.euclid_distance =[[0] * n for _ in range(n)]

        for k in range(n):
            for h in range(n):
                self.euclid_distance[k][h] = (self.calc_euclid_distance(k, h))

        return self.euclid_distance

# Calculate total tour trajectory cost
def calc_tour_length(tour, euclid_distance):
    total_length = 0
    for r in range(len(tour) - 1):
        total_length += euclid_distance[tour[r]][tour[r+1]]
    return total_length

# Initialize data structures
instance = Instance()
instance.get_info()
instance.create_matrix()


# ==============================================================================
# PHASE 1: NEAREST NEIGHBOR CONSTRUCTIVE HEURISTIC
# ==============================================================================

# Initialize routing control variables and state tracking
current_city = 0
start_city = 0
tour = []
greedy_tour = 0  # Accumulates the total scalar distance (cost) of the tour

# Initialize the boolean visited array to prevent sub-tour duplication
visited = [False] * len(instance.nodes)

# Establish the origin depot: seed the tour sequence with the starting city
current_city = start_city
tour.append(start_city)
visited[start_city] = True

# Track the structural cardinality of remaining unvisited vertices
unvisited_count = len(instance.nodes) - 1

# Execute the greedy constructive optimization loop
while unvisited_count > 0:
    next_city = None
    
    # Scan the geometric neighborhood to locate the unvisited node 
    # that minimizes the immediate edge cost from the current position
    for j in range(len(instance.nodes)):
        if not visited[j] and (next_city is None or instance.euclid_distance[current_city][j] < instance.euclid_distance[current_city][next_city]):
            next_city = j
            
    # Append the selected locally-optimal node to the active sequence
    tour.append(next_city)

    # Safety boundary check to prevent runtime exceptions on isolated nodes
    if next_city is None:
        break

    # Accumulate the standard Euclidean weight of the chosen edge
    greedy_tour += instance.euclid_distance[current_city][next_city]
    
    # Update loop invariants and transition the vehicle state to the new city
    unvisited_count -= 1
    visited[next_city] = True
    current_city = next_city

    # Enforce Hamiltonian cycle symmetry once all vertices have been evaluated
    if unvisited_count == 0:
        # Penalize the final return leg back to the initial origin depot
        greedy_tour += instance.euclid_distance[current_city][start_city]
        tour.append(start_city)

end_ni = time.perf_counter()
ni_time_ms = (end_ni - start_ni) * 1000

# ------------------------------------------------------------------------------
# LOCAL SEARCH: RELOCATE NEIGHBORHOOD OPTIMIZATION
# ------------------------------------------------------------------------------
def relocate_local_search(tour, euclid_distance):
    improved = True
    while improved:
        improved = False
        current_cost = calc_tour_length(tour, euclid_distance)

        for x in range(1, len(tour) - 1): # Protect start/end boundary nodes
            city = tour[x]

            # Tentatively remove the city from the current tour sequence
            temp_tour = tour.copy()
            temp_tour.pop(x)

            # Test insertion across all alternative slots in the tour
            for y in range(1, len(temp_tour)):
                if y == x or y == x - 1:
                    continue
                new_tour = temp_tour.copy()
                new_tour.insert(y, city)
                new_cost = calc_tour_length(new_tour, instance.euclid_distance)

                # Check if the candidate relocation yields a lower total routing cost
                if new_cost < current_cost:
                    tour = new_tour
                    current_cost = new_cost
                    improved = True
                    break

            if improved:
                break

    return tour

improved_tour = relocate_local_search(tour, instance.euclid_distance)

end_ls = time.perf_counter()
ls_time_ms = (end_ls - start_ls) * 1000

# ------------------------------------------------------------------------------
# SOLUTION FEASIBILITY VERIFICATION MODULE
# ------------------------------------------------------------------------------
def check_feasibility(tour, dataset_size):
    # Exclude the final returning city to isolate individual node entries
    actual_visited_cities = tour[:-1]

    # 1. Check whether all cities appear exactly once
    if len(actual_visited_cities) != len(set(actual_visited_cities)):
        print("Feasibility Error: Duplicated or unvisited cities found.")
        return False

    # 2. Check whether the tour returns to the starting city
    if tour[0] != tour[-1]:
        print("Feasibility Error: Tour fails to form a closed cycle back to origin.")
        return False

    # 3. Check whether the number of visited cities equals the dataset size
    if len(actual_visited_cities) != dataset_size:
        print(f"Feasibility Error: Visited size footprint ({len(actual_visited_cities)}) mismatch with dataset size ({dataset_size}).")
        return False

    print("Feasibility Verification: Valid Hamiltonian cycle successfully confirmed.")
    return True


# ==============================================================================
# EMPIRICAL RESULTS DISPLAY
# ==============================================================================
print(f"Nearest Neighbor Tour: {tour}") #[0, 8, 37, 30, 43, 17, 6, 27, 35, 29, 5, 36, 18, 26, 42, 16, 45, 32, 14, 11, 10, 22, 13, 24, 12, 20, 46, 19, 39, 2, 21, 15, 40, 33, 28, 4, 47, 38, 31, 23, 9, 41, 25, 3, 34, 44, 1, 7, 0]
print(f"Relocate Local Search Tour: {improved_tour}") 

print(f"Nearest Neighbor Length: {calc_tour_length(tour, instance.euclid_distance):.4f}")  #40526.42105630375
print(f"Relocate Local Search Length: {calc_tour_length(improved_tour, instance.euclid_distance):.4f}") 

print(f"Nearest Neighbor Time: {ni_time_ms:.3f} ms")
print(f"Relocate Local Search Time: {ls_time_ms:.3f} ms")

is_valid = check_feasibility(improved_tour, 48)
print(f"Checking Result: {is_valid}")


import matplotlib.pyplot as plt


def visualize_tour(instance, tour):

    x_coords = []
    y_coords = []

    # lay toa do theo tour
    for city in tour:

        x_coords.append(
            instance.nodes[city][0]
        )

        y_coords.append(
            instance.nodes[city][1]
        )

    plt.figure(figsize=(10,10))

    plt.plot(x_coords, y_coords, marker='o')

    # hien label city
    for city in tour[:-1]:

        x = instance.nodes[city][0]
        y = instance.nodes[city][1]

        plt.text(x, y, str(city))

    plt.title("TSP Tour")

    plt.xlabel("X")
    plt.ylabel("Y")

    plt.grid(True)

    plt.show()

visualize_tour(instance, improved_tour)