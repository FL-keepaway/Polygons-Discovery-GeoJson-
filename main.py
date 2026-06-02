import json
from collections import defaultdict


with open("samples/re_12021310131033.json") as f:
    data = json.load(f)

def find_cycles_dfs(type_of_lines, cycles, connect_matrix, visited, path, current_id, start):
    n = len(connect_matrix)
    for i in range(n):
        if connect_matrix[current_id][i] == 0:
            continue

        if i == start and len(path) >=3:
            cycle = path[:]
            cycles.append(cycle)
            continue

        if i in visited or i < start:
            continue

        path.append(i)
        visited.append(i)
        find_cycles_dfs(type_of_lines, cycles, connect_matrix, visited, path, i, start)
        path.pop()
        visited.remove(i)

def normalize_cycle(cycle):
    best = None
    n = len(cycle)
    for rev in (False, True):
        cyc = cycle if not rev else list(reversed(cycle))
        for shift in range(n):
            cand = cyc[shift:] + cyc[:shift]
            cand_t = tuple(cand)
            if best is None or cand_t < best:
                best = cand_t
    return list(best)



lines_by_type = defaultdict(list)
for item in data["features"]:
    if item["geometry"]["type"] == "LineString":
       lines_by_type[item["properties"]["type"]].append(item["geometry"]["coordinates"])

lines_by_type = dict(lines_by_type)
# print(lines_by_type)

#print(lines_by_type["d"])

lines_a = []
# lines_d = copy.deepcopy(lines_by_type["d"])
# lines_a.append([[0, 0], [1, 1], [1, 3], [0, 0]])
lines_a.append([[0, 0], [1, 1]])
lines_a.append([[1, 1], [3, 3]])
lines_a.append([[3, 0], [1, 3]])
lines_a.append([[1, 0], [0.5, 1]])
lines_a.append([[3, 3], [4, 1]])
lines_a.append([[1, 1], [1, 0]])
lines_a.append([[0, 2], [1, 2]])
lines_a.append([[1, 1], [4, 1]])
lines_a.append([[0.5, 1], [0, 0]])




islands = defaultdict(list)


# for type_of_lines in lines_by_type.keys():
#     lines = lines_by_type[type_of_lines]
type_of_lines = 'a'
lines_count = len(lines_a)
connect_matrix = [[0 for j in range(lines_count)] for i in range(lines_count)]
visited = []
for i, line in enumerate(lines_a):
    processed = set()

    begin = tuple(line[0])
    end = tuple(line[-1])

    if begin == end:
        islands[type_of_lines].append([i])
        visited.append(i)
        continue

    processed.add(i)

    for idx, edge in enumerate(lines_a):
        if idx in processed:
            continue

        b = tuple(edge[0])
        e = tuple(edge[-1])

        if (b == end or b == begin or e == end or e == begin) and idx not in visited:
            connect_matrix[i][idx] = 1

for connection in connect_matrix:
    print(connection)

cycles = []

for i in range(lines_count):
    path = []
    find_cycles_dfs(type_of_lines, cycles, connect_matrix, visited, path, i, i)

unique_cycles = {}
for cyc in cycles:
    norm = tuple(normalize_cycle(cyc))
    if norm not in unique_cycles:
        unique_cycles[norm] = list(norm)

print(unique_cycles)



for island in islands:
    print(island, islands[island])

# for i, line in enumerate(connect):
#     print(i, line)
