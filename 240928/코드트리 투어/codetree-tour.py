import heapq
from collections import defaultdict

INF = float('inf')

n,m = 0,0
cost = []
adj = []
item_dict = defaultdict(int)

class Item():
    def __init__(self, id, re, de):
        self.id = id
        self.re = re
        self.de = de
        self.profit = 0
        
        self.update_profit()
        
    def __lt__(self, other):
        if self.profit == other.profit:
            return self.id < other.id
        return self.profit > other.profit

    def update_profit(self):
        global cost

        if cost[self.de] == INF:
            self.profit = -1
        else:
            self.profit = self.re - cost[self.de]

def dijkstra(start):
    global n,cost,adj

    cost = [INF]*n
    cost[start] = 0
    pq = [(0,start)] # 비용, 위치

    while pq:
        cur_cost, cur =  heapq.heappop(pq)

        if cur_cost > cost[cur]:
            continue
        for nxt, w in adj[cur]:
            nxt_cost = cost[cur] + w
            if cost[nxt] > nxt_cost:
                cost[nxt] = nxt_cost
                heapq.heappush(pq, (nxt_cost,nxt))


def sell(pq):
    global item_dict

    while pq:
        if pq[0].profit < 0:
            break
        item = heapq.heappop(pq)
        if item_dict[item.id]==1:
            return item.id
    return -1

def update_item(pq):
    global cost

    for i in range(len(pq)):
        pq[i].update_profit()
    heapq.heapify(pq)

def main():
    global Q,n,m,cost,adj,item_dict

    Q = int(input())
    cmds = list(map(int, input().split()))
    n, m = cmds[1], cmds[2]
    adj = [[] for _ in range(n)]

    for i in range(3,len(cmds),3):
        v,u,w = cmds[i:i+3]
        adj[v].append((u,w))
        adj[u].append((v,w))

    dijkstra(0)

    pq_item = []

    for _ in range(Q-1):
        cmd = list(map(int, input().split()))

        if cmd[0]==200:
            _, id, re, de = cmd
            item = Item(id,re,de)
            heapq.heappush(pq_item,item)
            item_dict[id]=1

        elif cmd[0]==300:
            _, id = cmd
            item_dict[id]=0

        elif cmd[0]==400:
            ans = sell(pq_item)
            print(ans)

        elif cmd[0]==500:
            _, s = cmd
            dijkstra(s)
            update_item(pq_item)

if __name__ == '__main__':
    main()