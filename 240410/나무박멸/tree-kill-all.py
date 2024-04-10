dirs = [(0,1),(0,-1),(1,0),(-1,0)]
d_dirs = [(1,1),(1,-1),(-1,1),(-1,-1)]

# 나무 성장 - 인접 4칸 중 나무 있는 칸 만큼 성장/ 격자 벽 체크
def grow():
    global maps

    new_map = [[0]*n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            if maps[y][x] > 0:
                cnt = 0
                for d in range(4):
                    ny,nx = y+dirs[d][0], x+dirs[d][1]
                    if 0 <= ny < n and 0 <= nx < n:
                        if maps[ny][nx] > 0:
                            cnt += 1
                new_map[y][x] += cnt

    for y in range(n):
        for x in range(n):
            maps[y][x] += new_map[y][x]

# 나무 번식 - (현 위치 나무 수//인접 4칸 중 번식 가능 칸 수)만큼 인접 칸 나무 번식 / 격자 나무 제초제 체크
def breed():
    global maps

    new_map = [[0]*n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            if maps[y][x] > 0:
                cnt = 0
                breed_lst = []
                for d in range(4):
                    ny,nx = y+dirs[d][0], x+dirs[d][1]
                    if 0 <= ny < n and 0 <= nx < n:
                        if maps[ny][nx] == 0:
                            breed_lst.append((ny,nx))
                            cnt += 1
                breed_num = maps[y][x]//cnt
                for by,bx in breed_lst:
                    new_map[by][bx] += breed_num

    for y in range(n):
        for x in range(n):
            maps[y][x] += new_map[y][x]

# 제초제 투여 - 가장 많이 박멸 시키는 위치, 작은 행, 작은 열 / 4개 대각선 방향으로 k만큼 전파 / 벽 or 나무 없는 칸까지는 뿌려짐 / c년 만큼 남아 있음
def deworm(y,x,cnt):
    global max_num, candidate, candidate_map

    for di in d_dirs:
        flag = False
        for s in range(1,k+1):
            ny, nx = y+di[0]*s, x+di[1]*s
            if 0<=ny<n and 0<=nx<n:
                if new_maps[ny][nx] > 0:
                    cnt += new_maps[ny][nx]
                    new_maps[ny][nx] = -c-1
                else:
                    if -c-1 <= new_maps[ny][nx] <= 0:
                        new_maps[ny][nx] = -c-1
                        flag = True
                        break
        if flag:
            continue

    if cnt > max_num:
        max_num = cnt
        candidate = [[-cnt,cr,cc]]
        candidate_map = [new_maps]
    elif cnt == max_num:
        candidate.append([-cnt,cr,cc])
        candidate_map.append(new_maps)

def deworm2():
    global answer, maps

    if len(candidate)==1:
        sorted_candidate = candidate[0]
    else:
        sorted_candidate = sorted(candidate)[0]
    idx = candidate.index(sorted_candidate)
    new = candidate_map[idx]
    answer += -sorted_candidate[0]
    maps = new

# 제초제 감소
def deworm3():
    global maps

    for y in range(n):
        for x in range(n):
            if -c-1 <= maps[y][x] < 0:
                maps[y][x] += 1


n,m,k,c = map(int, input().split())
maps = []
for _ in range(n):
    lst = list(map(int, input().split()))
    for i in range(n):
        if lst[i] == -1:
            lst[i] = -1001
    maps.append(lst)

answer = 0
for _ in range(m):
    grow()
    breed()
    candidate = []
    candidate_map = []
    max_num = 0
    for cr in range(n):
        for cc in range(n):
            if maps[cr][cc] > 0:
                new_maps = [row[:] for row in maps]
                new_maps[cr][cc] = -c-1
                deworm(cr,cc,maps[cr][cc])
    deworm2()
    deworm3()

print(answer)