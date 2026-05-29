import time
start_ni = time.perf_counter()
start_ls = time.perf_counter()

class Instance:
    nodes = []
    euclid_distance = []

    def __init__(self):
        self.nodes = []
        self.euclid_distance = []

    # get information from file:
    def get_info(self):
        with open ("att48.tsp", "r") as file:
            lines = file.readlines()
            
            for i in range(len(lines) - 1):
                line = lines[i]
                if line == '' or line[0].isalpha():
                    continue

                # lay thong tin tu file: node, toa do x, toa do y
                node, x, y = line.split()
                node = int(node)
                x = float(x)
                y = float(y)
                self.nodes.append((x, y))

        return self.nodes
    
    # tinh khoang cach giua 2 node qua khoang cach euclid
    def calc_euclid_distance(self, u, v):
        return ((self.nodes[u][0] - self.nodes[v][0])**2 +(self.nodes[u][1]- self.nodes[v][1])**2)**0.5
    
    # tao ma tran luu khoang cach giua cac node
    def create_matrix(self):
        n = len(self.nodes)

        self.euclid_distance =[[0] * n for _ in range(n)]

        for k in range(n):
            for h in range(n):
                self.euclid_distance[k][h] = (self.calc_euclid_distance(k, h))

        return self.euclid_distance


instance = Instance()
instance.get_info()

instance.create_matrix()

instance.nodes
instance.euclid_distance


# Tim duong di ngan nhat using nearest insertion:

# tao 1 chu trinh nho:
current_city = 0
start_city = 0
tour = []

# bat dau tour voi thanh pho dau tien
visited = [False] * len(instance.nodes)
current_city = start_city
tour.append(start_city)

visited[start_city] = True
unvisited_count = len(instance.nodes) - 1

# tao 1 tour con tu start_city den closet_city:
closest_city = None
for j in range(len(instance.nodes)):
    if not visited[j] and (closest_city is None or instance.euclid_distance[current_city][j] < instance.euclid_distance[current_city][closest_city]):
            closest_city = j
tour.append(closest_city)

visited[closest_city] = True
unvisited_count -= 1

# Insertion method:
while unvisited_count > 0:
    # tim city gan tour nhat:
    next_city = None
    min_distance_to_tour = float('inf')
    for u in range(len(instance.nodes)):
        if not visited[u]:
            for j in tour:
                if instance.euclid_distance[u][j] < min_distance_to_tour:
                    min_distance_to_tour = instance.euclid_distance[u][j]
                    next_city = u
    u = next_city
    unvisited_count -= 1

    # tim vi tri chen u voi chi phi min:
    best_insertion_node = None
    min_insertion_cost = float('inf')

    # duyet canh
    for idx in range(len(tour) - 1):
        m = tour[idx]
        n = tour[idx + 1]
    
        cost_increase = instance.euclid_distance[m][u] + instance.euclid_distance[u][n] - instance.euclid_distance[m][n]
        if cost_increase < min_insertion_cost:
            min_insertion_cost = cost_increase
            best_insertion_node = idx + 1

    # chen city u vao vi tri tot nhat:
    tour.insert(best_insertion_node, u)
    visited[u] = True

    # tour hoan chinh:
    completed_tour = tour + [start_city]

# tinh do dai duong di:
def calc_tour_length(tour, euclid_distance):
    total_length = 0
    for r in range(len(tour) - 1):
        total_length += euclid_distance[tour[r]][tour[r+1]]
    return total_length



end_ni = time.perf_counter()
ni_time_ms = (end_ni - start_ni) * 1000

# Local Search: Relocate
def relocate_local_search(tour, euclid_distance):
    improved = True
    while improved:
        improved = False
        current_cost = calc_tour_length(tour, euclid_distance)

        for x in range(1, len(tour) - 1): # khong remove start/end node
            city = tour[x]

            #remove city khoi tour
            temp_tour = tour.copy()
            temp_tour.pop(x)

            # chen city do vao vi tri khac
            for y in range(1, len(temp_tour)):
                if y == x or y == x - 1:
                    continue
                new_tour = temp_tour.copy()
                new_tour.insert(y, city)
                new_cost = calc_tour_length(new_tour, euclid_distance)

                # check cem co cheaper k
                if new_cost < current_cost:
                    tour = new_tour
                    current_cost = new_cost
                    improved = True

                    break

            if improved:
                break

    return tour

improved_tour = relocate_local_search(completed_tour, instance.euclid_distance)

end_ls = time.perf_counter()
ls_time_ms = (end_ls - start_ls) * 1000

def check_feasibility(tour, dataset_size):
    # Exclude the final returning city to analyze the unique set of visited vertices
    # Example: [0, 21, ..., 8, 0] -> the actual sequence of cities to verify is tour[:-1]
    actual_visited_cities = tour[:-1]

    # 1. Check whether all cities appear exactly once
    # (Verified by comparing the length of the list against a unique element set)
    if len(actual_visited_cities) != len(set(actual_visited_cities)):
        print("Invalid: Certain cities are either duplicated or left unvisited.")
        return False

    # 2. Check whether the tour returns to the starting city
    # (Verified by ensuring the first and the last elements of the tour are identical)
    if tour[0] != tour[-1]:
        print("Invalid: The tour does not return to the initial starting city.")
        return False

    # 3. Check whether the number of visited cities equals the dataset size
    # (Verified by matching the length of the sliced tour with the total instance size)
    if len(actual_visited_cities) != dataset_size:
        print(f"Invalid: The total number of visited cities ({len(actual_visited_cities)}) does not match the dataset size ({dataset_size}).")
        return False

    # 4. If all conditions are satisfied: return Valid
    print("Valid: The TSP tour successfully satisfies all feasibility constraints!")
    return True

# -----------TESTING------------

print(f"Nearest Insertion Tour: {completed_tour}") # [0, 21, 15, 7, 37, 30, 43, 6, 27, 36, 18, 26, 16, 42, 5, 29, 35, 17, 45, 32, 19, 11, 10, 46, 20, 31, 38, 47, 4, 23, 44, 34, 3, 25, 9, 41, 1, 28, 12, 24, 13, 22, 33, 40, 2, 14, 39, 8, 0]
print(f"Relocate Tour: {improved_tour}") # [0, 21, 15, 7, 37, 30, 43, 17, 6, 27, 5, 36, 18, 26, 16, 42, 29, 35, 45, 32, 19, 46, 20, 38, 31, 23, 9, 44, 34, 3, 25, 41, 1, 28, 4, 47, 24, 12, 13, 33, 40, 2, 22, 10, 11, 14, 39, 8, 0]

print(f"Nearest Insertion Length: {calc_tour_length(completed_tour, instance.euclid_distance)}") # 37994.32137894776
print(f"Relocate Length: {calc_tour_length(improved_tour, instance.euclid_distance)}") # 34665.44625404617 < 37994.32137894776

print(f"Nearest Insertion Time: {ni_time_ms:.3f} ms")
print(f"Relocate Local Search Time: {ls_time_ms:.3f} ms")

is_valid = check_feasibility(completed_tour, 48)
print(f"Checking Result: {is_valid}")

