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
    for KK in range(k):
        jump_c, c_rc, c_r, id = heapq.heappop(rabbits)
        jump_c += 1
        cr, cc = c_r, c_rc - c_r
        d = dist_dic[id]
        sub = []
        # print(KK+1)
        # print('점프 전 id,r,c', id,cr,cc)
        for i in range(4):
            dist = d
            r,c = cr,cc
            if i == 0:  # 오른쪽 이동
                dist %= 2 * (m - 1)
                nc = c + dist
                if nc > m - 1:
                    nc = (m - 1) - (dist - (m - c - 1))
                    if nc < 0:
                        nc = abs(nc)
                sub.append((r + nc, r, nc))
                # print(r, nc)

            elif i == 1:  # 아래쪽 이동
                dist %= 2 * (n - 1)
                nr = r + dist
                if nr > n - 1:
                    nr = (n - 1) - (dist - (n - r - 1))
                    if nr < 0:
                        nr = abs(nr)
                sub.append((nr + c, nr, c))
                # print(nr, c)

            elif i == 2:  # 왼쪽 이동
                dist %= 2 * (m - 1)
                nc = c - dist
                if nc < 0:
                    nc = dist - c
                    if nc > m - 1:
                        over = nc - (m - 1)
                        nc = m - 1 - over
                sub.append((r + nc, r, nc))
                # print(r, nc)

            elif i == 3:  # 위쪽 이동
                dist %= 2 * (n - 1)
                nr = r - dist
                if nr < 0:
                    nr = dist - r
                    if nc > n - 1:
                        over = nc - (n - 1)
                        nc = n - 1 - over
                sub.append((nr + c, nr, c))
                # print(nr, c)

        # 가장 우선순위 높은 위치로 이동
        _, r_, c_ = sorted(sub, key=lambda x: (-x[0], -x[1], -x[2]))[0]
        # print('점프 후 id,r,c',id,r_,c_)

        # 토끼를 다시 힙에 넣고, 선택된 토끼 리스트에 추가
        heapq.heappush(rabbits, (jump_c, r_ + c_, r_, id))
        selected_rabbits.append((jump_c, r_ + c_, r_, id))

        # 모든 토끼의 점수를 갱신
        for key in score_dic.keys():
            if key != id:
                score_dic[key] += r_ + c_ + 2

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