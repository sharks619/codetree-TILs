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

def bfs(i, r, c, c_map):
    global max_cnt

    new_map = [row[:] for row in c_map]
    sub_map = [row[c - 1:c + 2] for row in new_map[r - 1:r + 2]]
    r_result = r_dic[i](sub_map)

    for idx in range(3):
        new_map[r - 1 + idx][c - 1:c + 2] = r_result[idx]

    remove_list = []
    v = [[0] * 5 for _ in range(5)]
    total_cnt = 0
    for cr in range(5):
        for cc in range(5):
            if v[cr][cc]:
                continue
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

    if total_cnt > max_cnt:
        max_cnt = total_cnt
        sub.append([total_cnt, i, c, r, remove_list, new_map])
    

def refill(mlst, n_map):
    for r, c in mlst:
        n_map[r][c] = 0

    for x in range(5):
        for y in range(4, -1, -1):
            if n_map[y][x] == 0:
                n_map[y][x] = nums.popleft()
    return n_map

def remove(n2_map):
    global ans

    while True:
        remove_list = []
        v = [[0] * 5 for _ in range(5)]
        for r in range(5):
            for c in range(5):
                if v[r][c]:
                    continue
                q = deque([(r, c)])
                r_lst = [(r, c)]
                v[r][c] = 1
                cnt = 1
                while q:
                    cr, cc = q.popleft()
                    for d in dirs:
                        nr, nc = cr + d[0], cc + d[1]
                        if 0 <= nr < 5 and 0 <= nc < 5 and not v[nr][nc]:
                            if n2_map[nr][nc] == n2_map[cr][cc]:
                                q.append((nr, nc))
                                r_lst.append((nr, nc))
                                v[nr][nc] = 1
                                cnt += 1
                if cnt >= 3:
                    remove_list.extend(r_lst)
        if remove_list:
            ans += len(remove_list)
            n2_map = refill(remove_list, n2_map)
        else:
            break
    return n2_map

answer = []
for _ in range(k):
    max_cnt = 0
    sub = []
    ans = 0
    for i in range(3):
        for c in range(1, 4):
            for r in range(1, 4):
                bfs(i, r, c, maps)

    if not sub:
        break

    m_cnt, mi, mc, mr, mlst, mmap = sorted(sub, key=lambda x: -x[0])[0]
    n_map = mmap

    ans += m_cnt
    n2_map = refill(mlst, n_map)

    n3_map = remove(n2_map)
    maps = n3_map

    if ans:
        answer.append(ans)

print(*answer)