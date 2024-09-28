import heapq
from collections import defaultdict

# 무한대를 정의합니다.
INF = float('inf')

# 도시와 도로 정보를 저장할 전역 변수
n, m = 0, 0
adj = []
cost = []
item_dict = defaultdict(int)

# 상품 클래스를 정의하여 각 상품의 정보를 관리합니다.
class Item:
    def __init__(self, item_id, revenue, dest):
        self.item_id = item_id
        self.revenue = revenue
        self.dest = dest
        self.profit = 0

        # 이익을 초기화합니다.
        self.update_profit()

    # 우선순위 큐에서 이익을 기준으로 비교하는 방법을 정의합니다.
    def __lt__(self, other):
        if self.profit == other.profit:
            return self.item_id < other.item_id
        return self.profit > other.profit

    # 이익을 갱신하는 함수입니다.
    def update_profit(self):
        global cost
        if cost[self.dest] == INF:
            self.profit = -1  # 목적지까지 도달할 수 없으면 이익은 음수로 설정
        else:
            self.profit = self.revenue - cost[self.dest]  # 수익에서 비용을 뺀 값

# 다익스트라 알고리즘을 이용하여 출발지에서 각 도시까지의 최단 경로를 계산합니다.
def dijkstra(start):
    global n, cost, adj
    cost = [INF] * n  # 모든 도시까지의 비용을 무한대로 초기화
    cost[start] = 0
    pq = [(0, start)]  # 우선순위 큐에 시작 도시를 추가

    while pq:
        cur_cost, cur = heapq.heappop(pq)
        if cur_cost > cost[cur]:
            continue
        for nxt, w in adj[cur]:
            nxt_cost = cost[cur] + w
            if nxt_cost < cost[nxt]:
                cost[nxt] = nxt_cost
                heapq.heappush(pq, (nxt_cost, nxt))

# 상품을 판매하는 함수입니다.
def sell(pq):
    global item_dict

    # 수익이 음수가 아닌 가장 높은 수익을 가진 상품을 찾습니다.
    while pq:
        if pq[0].profit < 0:
            break  # 수익이 음수인 경우, 판매 불가
        item = heapq.heappop(pq)
        if item_dict[item.item_id] == 1:  # 활성화된 상품만 판매
            return item.item_id
    return -1  # 판매할 상품이 없으면 -1을 반환

# 모든 상품의 이익을 갱신하는 함수입니다.
def update_item(pq):
    global cost
    for i in range(len(pq)):
        pq[i].update_profit()  # 각 상품의 이익을 갱신
    heapq.heapify(pq)  # 갱신된 상품 리스트를 다시 우선순위 큐로 만듭니다.

Q = int(input())  # 명령어의 수 입력
cmds = list(map(int, input().split()))

# 도시와 도로 정보를 입력받습니다.
n, m = cmds[1], cmds[2]
adj = [[] for _ in range(n)]  # 인접 리스트 초기화
for i in range(3, len(cmds), 3):
    v, u, w = cmds[i:i + 3]
    adj[v].append((u, w))  # v에서 u로 가는 도로 추가
    adj[u].append((v, w))  # u에서 v로 가는 도로 추가

# 초기 출발지는 0번 도시로 설정하고 최단 경로를 계산합니다.
dijkstra(0)

# 우선순위 큐를 사용하여 상품을 관리합니다.
pq_item = []

for _ in range(Q - 1):
    cmd = list(map(int, input().split()))  # 명령어 입력
    if cmd[0] == 200:
        # 상품을 등록하는 명령
        _, item_id, revenue, dest = cmd
        item = Item(item_id, revenue, dest)
        heapq.heappush(pq_item, item)
        item_dict[item_id] = 1  # 상품 활성화
            
    elif cmd[0] == 300:
        # 상품을 취소하는 명령
        _, item_id = cmd
        item_dict[item_id] = 0  # 상품 비활성화

    elif cmd[0] == 400:
        # 상품을 판매하는 명령
        ret = sell(pq_item)
        print(ret)

    elif cmd[0] == 500:
        # 출발지를 변경하는 명령
        _, s = cmd
        dijkstra(s)  # 새로운 출발지에서 최단 경로를 계산
        update_item(pq_item)  # 모든 상품의 이익을 갱신