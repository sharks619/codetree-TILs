import heapq
from collections import defaultdict

dirs = [(0,1),(1,0),(0,-1),(-1,0)]

rabbits = []
heapq.heapify(rabbits)

score_dic = defaultdict(int)
dist_dic = defaultdict(int)

q = int(input())
_, n, m, p, *args = list(map(int, input().split()))

for i in range(p):
    id, d = args[i*2:i*2+2]
    heapq.heappush(rabbits,(0, 0, 0, id))  # (cnt, r + c, r, id)
    score_dic[id] = 0
    dist_dic[id] = d


def race(k,s):
    for _ in range(k):
        jump_c, r_c, r, id = heapq.heappop(rabbits)
        jump_c += 1
        r, c = r, r_c - r
        d = dist_dic[id]
        sub = []

        for i in range(4):
            dist = d
            if i==0: # r 그대로
                dist %= 2*(m-1)
                nr, nc = r, c + dist
                if nc > m-1:
                    nc = (m-1)-(dist-m+c+1)

            elif i==1: # c 그대로
                dist %= 2*(n-1)
                nr, nc = r + dist, c
                if nr > n-1:
                    nr = (n-1)-(dist-n+r+1)

            elif i==2: # r 그대로
                dist %= 2*(m-1)
                nr, nc = r, c - dist
                if nc < 0:
                    nc = dist-c

            elif i==3: # c 그대로
                dist %= 2*(n-1)
                nr, nc = r - dist, c
                if nr < 0 :
                    nr = dist-r

            sub.append((nr+nc, nr, nc))

        _, r, c = sorted(sub, key=lambda x: (-x[0],-x[1],-x[2]))[0]
        heapq.heappush(rabbits,(jump_c, r+c, r, id))  # (cnt, r + c, r, id)

        for key in score_dic.keys():
            if key != id:
                score_dic[key] += r+c

    new_rabbits = rabbits[:]
    new_rabbits_list = sorted(new_rabbits, key=lambda x: (-x[1],-x[2],-x[3]))
    for i in new_rabbits_list:
        if i[0]:
            r_id = i[3]
            score_dic[r_id] += s


for _ in range(q-1):
    cmd, *args = list(map(int, input().split()))
    if cmd == 200:
        K, S = args
        race(K, S)

    elif cmd == 300:
        pid_t, L = args
        dist_dic[pid_t] *= L

    elif cmd == 400:
        print(max(score_dic.values()))