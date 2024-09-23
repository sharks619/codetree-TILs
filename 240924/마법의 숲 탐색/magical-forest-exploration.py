from collections import deque

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 북, 동, 남, 서

r, c, k = map(int, input().split())
commands = [list(map(int, input().split())) for _ in range(k)]
maps = [[0] * c for _ in range(r + 3)]
exist_set = set()

def bfs(cr, cc):
    q = deque([(cr, cc)])
    visited = [[0] * c for _ in range(r + 3)]
    visited[cr][cc] = 1
    max_r = 0
    while q:
        cr, cc = q.popleft()
        max_r = max(cr, max_r)

        for di in dirs:
            nr, nc = cr + di[0], cc + di[1]
            if 0 <= nr < r + 3 and 0 <= nc < c and not visited[nr][nc] and (
                    maps[cr][cc] == maps[nr][nc] or ((cr, cc) in exist_set and maps[nr][nc])):
                q.append((nr, nc))
                visited[nr][nc] = 1
    return max_r-2

ans = 0
num = 1
for ci, di in commands:
    cr, cc, cd = 1, ci - 1, di
    while True:
        # 남
        if 0 < cr < r + 1 and 0 < cc < c - 1 and maps[cr + 1][cc - 1] + maps[cr + 1][cc + 1] + maps[cr + 2][cc] == 0:
            cr += 1
        # 서 -> 남
        elif 0 < cr < r + 1 and 1 < cc < c - 1 and maps[cr - 1][cc - 1] + maps[cr][cc - 2] + maps[cr + 1][cc - 2] + \
                maps[cr + 2][cc - 1] == 0:
            cr += 1
            cc -= 1
            cd = (cd + 3) % 4
        # 동 -> 남
        elif 0 < cr < r + 1 and 0 < cc < c - 2 and maps[cr - 1][cc + 1] + maps[cr][cc + 2] + maps[cr + 1][cc + 2] + \
                maps[cr + 2][cc + 1] == 0:
            cr += 1
            cc += 1
            cd = (cd + 1) % 4
        else:
            break
    if cr < 4:
        maps = [[0] * c for _ in range(r + 3)]
        exist_set = set()
        num = 1
    else:
        maps[cr + 1][cc] = num
        maps[cr - 1][cc] = num
        maps[cr][cc + 1] = num
        maps[cr][cc - 1] = num
        maps[cr][cc] = num

        num += 1
        exist_set.add((cr + dirs[cd][0], cc + dirs[cd][1]))
        ans += bfs(cr, cc)

print(ans)