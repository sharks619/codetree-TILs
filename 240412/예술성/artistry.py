from itertools import combinations

dirs = [(0,1),(1,0),(0,-1),(-1,0)]

# 클러스터링
def grouping():
    group = [] # 모든 그룹 정보 저장 (번호, 개수, 그룹 별 각 위치 리스트)
    visited = [[0]*n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if not visited[r][c]:
                visited[r][c] = True
                color = maps[r][c]
                cnt = 1
                sub_group = [] # 같은 그룹 격자 위치 저장
                sub_group2 = [] # 같은 그룹 격자 위치 저장
                sub_group.append([r,c])
                sub_group2.append([r,c])
                while sub_group:
                    cr,cc = sub_group.pop()
                    for d in dirs:
                        nr, nc = cr+d[0], cc+d[1]
                        if 0<=nr<n and 0<=nc<n and not visited[nr][nc] and color==maps[nr][nc]:
                            visited[nr][nc] = True
                            cnt += 1
                            sub_group.append([nr,nc])
                            sub_group2.append([nr,nc])
                group.append([color,cnt,sub_group2])
    return group

# 점수 계산
def cal(arr):
    global score

    for a,b in combinations(range(len(arr)),2):
        adjacent = 0
        a_num, a_cnt, a_loc = arr[a]
        b_num, b_cnt, b_loc = arr[b]
        if a_cnt > b_cnt:
            for by,bx in b_loc:
                for d in dirs:
                    ny, nx = by+d[0], bx+d[1]
                    if 0<=ny<n and 0<=nx<n:
                        if [ny,nx] in a_loc:
                            adjacent += 1
        else:
            for ay,ax in a_loc:
                for d in dirs:
                    ny, nx = ay+d[0], ax+d[1]
                    if 0<=ny<n and 0<=nx<n:
                        if [ny,nx] in b_loc:
                            adjacent += 1
        if adjacent:
            score += (a_cnt+b_cnt)*a_num*b_num*adjacent


# 90회전
def ro90(arr):
    return [list(row) for row in list(zip(*arr[::-1]))]

# -90회전
def ro_90(arr):
    return [list(row) for row in list(reversed(list(zip(*arr))))]

# 십자가 반시계 방향 회전
def rotation1():
    global maps

    new = ro_90(maps)
    for r in range(n):
        for c in range(n):
            if r == (n - 1) // 2 or c == (n - 1) // 2:
                maps[r][c] = new[r][c]

# 정사각형 시계 방향 회전
def rotation2():
    global maps

    # 정사각형 추출 후 회전
    a2 = []
    for r in range(n//2):
        a2.append(maps[r][:n//2])
    a2 = ro90(a2)

    a1 = []
    for r in range(n//2):
        a1.append(maps[r][n//2+1:])
    a1 = ro90(a1)

    a3 = []
    for r in range(n//2 + 1, n):
        a3.append(maps[r][:n//2])
    a3 = ro90(a3)

    a4 = []
    for r in range(n//2 + 1, n):
        a4.append(maps[r][n//2+1:])
    a4 = ro90(a4)

    # 회전된 정사각형 넣기
    for i,r in enumerate(range(n//2)):
        maps[r][:n//2] = a2[i][:]

    for i,r in enumerate(range(n//2)):
        maps[r][n//2+1:n] = a1[i][:]

    for i,r in enumerate(range(n//2+1,n)):
        maps[r][:n//2] = a3[i][:]

    for i,r in enumerate(range(n//2+1,n)):
        maps[r][n//2+1:n] = a4[i][:]


n = int(input())
maps = [list(map(int, input().split())) for _ in range(n)]

score = 0
for _ in range(3):
    group = grouping()
    cal(group)
    rotation1()
    rotation2()
group = grouping()
cal(group)
print(score)