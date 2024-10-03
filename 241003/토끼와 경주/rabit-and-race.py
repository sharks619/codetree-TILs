import heapq
from collections import defaultdict

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

rabbits = []
score_dic = defaultdict(int)
dist_dic = defaultdict(int)

q = int(input())
_, n, m, p, *args = list(map(int, input().split()))

for i in range(p):
    id, d = args[i * 2:i * 2 + 2]
    heapq.heappush(rabbits, (0, 0, 0, id))  # (cnt, r + c, r, id)
    score_dic[id] = 0
    dist_dic[id] = d


def race(k, s):
    selected_rabbits = []

    # K번의 턴을 처리
    for _ in range(k):
        jump_c, c_rc, c_r, id = heapq.heappop(rabbits)
        jump_c += 1
        cr, cc = c_r, c_rc - c_r
        d = dist_dic[id]
        sub = []

        for i in range(4):
            nr, nc = cr+dirs[i][0]*d, cc+dirs[i][1]*d
            if nr<0 or nc<0 or nr>=n or nc>=m:
                nr %= 2*(n-1)
                nc %= 2*(m-1)
                nr = min(nr, 2*(n-1)-nr)
                nc = min(nc, 2*(m-1)-nc)
            sub.append((nr + nc, nr, nc))

        # 가장 우선순위 높은 위치로 이동
        _, r, c = sorted(sub, key=lambda x: (-x[0], -x[1], -x[2]))[0]

        # 토끼를 다시 힙에 넣고, 선택된 토끼 리스트에 추가
        heapq.heappush(rabbits, (jump_c, r + c, r, id))
        selected_rabbits.append((jump_c, r + c, r, id))

        # 모든 토끼의 점수를 갱신
        for key in score_dic.keys():
            if key != id:
                score_dic[key] += r + c + 2

    # 선택된 토끼들 중에서 우선순위가 높은 토끼 선택
    selected_rabbits = sorted(selected_rabbits, key=lambda x: (-x[1], -x[2], -x[3]))
    r_id = selected_rabbits[0][3]

    # 점수 S 추가
    score_dic[r_id] += s


for _ in range(q - 1):
    cmd, *args = list(map(int, input().split()))
    if cmd == 200:
        K, S = args
        race(K, S)
    elif cmd == 300:
        pid_t, L = args
        dist_dic[pid_t] *= L
    elif cmd == 400:
        print(max(score_dic.values()))