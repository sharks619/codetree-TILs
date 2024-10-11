import heapq
from collections import defaultdict

q = int(input())
cmd, n, m, *args = list(map(int, input().split()))

graph = defaultdict(list) # {current_node:(next_node, cost)}

travel_q = [] # 현재 판매할 수 있는 여행 상품
ids = defaultdict(bool) # 모든 여행 상품
travel_info = defaultdict(list) # {id:(revenue, dest)}

for i in range(m):
    v,u,w = args[i*3:(i+1)*3]
    graph[v].append((u, w))
    graph[u].append((v, w))

INF = float('inf')

def dijkstra(start):
    distance = [INF] * n
    distance[start] = 0

    q = []
    heapq.heappush(q, (start,0))

    while q:
        c_node, c_dist = heapq.heappop(q)
        if c_dist > distance[c_node]:
            continue
        for n_node, cost in graph[c_node]:
            n_dist = c_dist + cost
            if n_dist < distance[n_node]:
                distance[n_node] = n_dist
                heapq.heappush(q, (n_node,n_dist))

    return distance

distance = dijkstra(0)

for _ in range(q-1):
    cmd, *args = list(map(int, input().split()))

    # print("명령어", cmd, args)
    # print("명령 전")
    # print("graph", graph)
    # print("travel_q", travel_q)
    # print("ids", ids)
    # print()

    if cmd == 200:
        id, revenue, dest = args
        ids[id] = True
        travel_info[id] = (revenue, dest)
        dist = distance[dest]
        if dist == INF:
            continue
        if dist > revenue:
            continue
        heapq.heappush(travel_q, (dist-revenue, id))

    elif cmd == 300:
        id = args[0]
        ids[id] = False

    elif cmd == 400:
        while travel_q:
            dist, id = heapq.heappop(travel_q)
            if ids[id]:
                print(id)
                ids[id] = False
                break
        else:
            print(-1)

    elif cmd == 500:
        s = args[0]

        distance = dijkstra(s)

        travel_q.clear()
        for id in ids:
            if ids[id]:
                r, d = travel_info[id]
                dist = distance[d]
                if dist == INF:
                    continue
                if dist > r:
                    continue
                heapq.heappush(travel_q, (dist - r, id))

    # print()
    # print("명령 후")
    # print("graph", graph)
    # print("travel_q", travel_q)
    # print("ids", ids)
    # print()