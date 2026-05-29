'''
Implementation logic. At each iteration:
1. keep track of the current city,
2. scan all unvisited cities,
3. choose the city with minimum distance from the current city,
4. append it to the tour.

'''

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

'''
print(instance.nodes)

print(instance.euclid_distance)
'''

# Tim duong di ngan nhat giua hai hai thanh pho using nearest neighbor:
current_city = 0
start_city = 0
tour = []
greedy_tour = 0

visited = [False] * len(instance.nodes)
current_city = start_city
tour.append(start_city)

visited[start_city] = True

unvisited_count = len(instance.nodes) - 1

while unvisited_count > 0:
    next_city = None
    for j in range(len(instance.nodes)):
        if not visited[j] and (next_city is None or instance.euclid_distance[current_city][j] < instance.euclid_distance[current_city][next_city]):
            next_city = j
    tour.append(next_city)

    if next_city is None:
        break

    greedy_tour += instance.euclid_distance[current_city][next_city]
    unvisited_count -= 1
    visited[next_city] = True
    current_city = next_city

    if unvisited_count == 0:
        greedy_tour += instance.euclid_distance[current_city][start_city]
        tour.append(start_city)
        


print(greedy_tour) #40526.42105630375

print(tour) #[0, 8, 37, 30, 43, 17, 6, 27, 35, 29, 5, 36, 18, 26, 42, 16, 45, 32, 14, 11, 10, 22, 13, 24, 12, 20, 46, 19, 39, 2, 21, 15, 40, 33, 28, 4, 47, 38, 31, 23, 9, 41, 25, 3, 34, 44, 1, 7, 0]