from collections import deque

dirs = [(-1,0),(0,1),(1,0),(0,-1)] # 북:0, 동:1, 남:2, 서:3

r,c,k = map(int, input().split())
maps = [[0]*c for _ in range(r+3)]
exit_set = set()

def g_move(ci,di,i):
    max_r, max_c, max_d = 0, 0, 0

    q = deque()
    q.append((1,ci,di)) # r,c,d
    while q:
        cr, cc, cd = q.popleft()
        if max_r < cr:
            max_r = cr
            max_c = cc
            max_d = cd

        # 남
        if (1<=cr<r+1 and 1<=cc<c-1 and
                maps[cr+1][cc-1] + maps[cr+2][cc] + maps[cr+1][cc+1] == 0):
            nr,nc = cr+1,cc
            q.append((nr,nc,cd))

        # 서 + 남
        elif (1<=cr<r+1 and 2<=cc<c-1 and
              maps[cr-1][cc-1] + maps[cr][cc-2] + maps[cr+1][cc-2] + maps[cr+2][cc-1] == 0):
            nr,nc = cr+1,cc-1
            cd = (cd+3)%4
            q.append((nr,nc,cd))

        # 동 + 남
        elif (1<=cr<r+1 and 1<=cc<c-2 and
              maps[cr-1][cc+1] + maps[cr][cc+2] + maps[cr+1][cc+2] + maps[cr+2][cc+1] == 0):
            nr,nc = cr+1,cc+1
            cd = (cd+1)%4
            q.append((nr,nc,cd))

    if max_r < 4:
        return -1,-1

    er,ec = max_r + dirs[max_d][0], max_c + dirs[max_d][1]
    exit_set.add((er,ec))

    maps[max_r][max_c+1] = i+1
    maps[max_r+1][max_c] = i+1
    maps[max_r][max_c-1] = i+1
    maps[max_r-1][max_c] = i+1
    maps[max_r][max_c] = i+1
    return max_r, max_c

def j_move(gr,gc):
    max_r = 0
    q = deque()
    q.append((gr,gc))
    v = [[0] * c for _ in range(r + 3)]
    v[gr][gc] = 1
    while q:
        cr, cc = q.popleft()
        max_r = max(max_r, cr)
        for d in dirs:
            nr, nc = cr+d[0], cc+d[1]
            if 0<=nr<r+3 and 0<=nc<c:
                if maps[nr][nc] == maps[cr][cc] or ((cr,cc) in exit_set and maps[nr][nc] != 0):
                    if not v[nr][nc]:
                        q.append((nr,nc))
                        v[nr][nc] = 1
    return max_r-2

score = 0
for i in range(k):
    ci, di = map(int, input().split())
    gr, gc = g_move(ci-1, di, i)

    if gr == gc == -1:
        maps = [[0] * c for _ in range(r + 3)]
        exit_set = set()
        continue
    else:
        score += j_move(gr,gc)

print(score)