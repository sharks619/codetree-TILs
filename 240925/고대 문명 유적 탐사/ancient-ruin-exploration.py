from collections import deque

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

k, m = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(5)]
nums = deque(list(map(int, input().split())))

def r_90(arr):
    return [list(a[::-1]) for a in zip(*arr)]

def r_180(arr):
    return [list(a[::-1]) for a in arr][::-1]

def r_270(arr):
    return [list(a) for a in zip(*arr)][::-1]

r_dic = {0: r_90, 1: r_180, 2: r_270}

def bfs(i, r, c, maps):

    global max_cnt

    new_map = [row[:] for row in maps]

    sub_map = [row[c-1:c+2] for row in new_map[r-1:r+2]]
    r_result = r_dic[i](sub_map)

    for idx in range(3):
        new_map[r-1+idx][c-1:c+2] = r_result[idx]

    remove_list = []
    v = [[0] * 5 for _ in range(5)]
    total_cnt = 0
    for cc in range(5):
        for cr in range(5):
            q = deque([(cr, cc)])
            r_lst = [(cr, cc)]
            v[cr][cc] = 1
            cnt = 1
            while q:
                cr, cc = q.popleft()
                for d in dirs:
                    nr, nc = cr + d[0], cc + d[1]
                    if 0 <= nr < 5 and 0 <= nc < 5 and not v[nr][nc]:
                        if new_map[nr][nc] == new_map[cr][cc]:
                            q.append((nr, nc))
                            r_lst.append((nr, nc))
                            v[nr][nc] = 1
                            cnt += 1

            if cnt >= 3:
                total_cnt += cnt
                remove_list.extend(r_lst)

    if total_cnt >= max_cnt:
        max_cnt = total_cnt
        sub.append([total_cnt, i, r, c, remove_list])

def refill(mlst):
    for i in range(len(mlst)):
        r, c = mlst[i]
        new_map[r][c] = 0

    for x in range(5):
        for y in range(4,-1,-1):
            if new_map[y][x]==0:
                new_map[y][x] = nums.popleft()


def remove():
    global ans

    while True:
        remove_list = []
        v = [[0] * 5 for _ in range(5)]
        for c in range(5):
            for r in range(5):
                q = deque([(r, c)])
                r_lst = [(r, c)]
                v[r][c] = 1
                cnt = 1
                while q:
                    cr, cc = q.popleft()
                    for d in dirs:
                        nr, nc = cr + d[0], cc + d[1]
                        if 0 <= nr < 5 and 0 <= nc < 5 and not v[nr][nc]:
                            if new_map[nr][nc] == new_map[cr][cc]:
                                q.append((nr, nc))
                                r_lst.append((nr, nc))
                                v[nr][nc] = 1
                                cnt += 1
                if cnt >= 3:
                    remove_list.extend(r_lst)
        if remove_list:
            ans += len(remove_list)
            refill(remove_list)
        else:
            break

answer = []
for _ in range(k):
    max_cnt = 0
    sub = []
    ans = 0
    for i in range(3):
        for c in range(1,4):
            for r in range(1,4):
                bfs(i, r, c, maps)
    if not sub:
        break
    else:
        m_cnt, mi, mr, mc, mlst = sorted(sub, key=lambda x: -x[0])[0]
        mlst.sort(key=lambda x: -x[0])

        new_map = [row[:] for row in maps]

        sub_map = [row[mc-1:mc+2] for row in new_map[mr-1:mr+2]]
        r_result = r_dic[mi](sub_map)

        for idx in range(3):
            new_map[mr-1+idx][mc-1:mc+2] = r_result[idx]

        ans += m_cnt
        refill(mlst)

        remove()
        maps = new_map
    if ans:
        answer.append(ans)

print(*answer)