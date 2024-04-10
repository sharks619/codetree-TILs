from collections import deque

dirs = [(0,1),(1,0),(0,-1),(-1,0)]

def find_one():
    for j in range(n):
        for i in range(n):
            if team[j][i] == 1:
                one.append((j, i))

def team_search():
    visited = [[0] * n for _ in range(n)]
    for y,x in one:
        q = deque()
        q2 = deque()
        q.append((y,x))
        q2.append((y,x))
        while q:
            cy,cx = q.popleft()
            visited[cy][cx] = True
            for di in dirs:
                ny, nx = cy+di[0], cx+di[1]
                if 0<=ny<n and 0<=nx<n and maps[ny][nx]:
                    if not visited[ny][nx]:
                        if team[cy][cx] == 1:
                            if team[ny][nx] == 2:
                                visited[ny][nx] = True
                                q.append((ny,nx))
                                q2.append((ny,nx))
                        elif team[cy][cx] == 2:
                            if team[ny][nx] in [2,3]:
                                visited[ny][nx] = True
                                q.append((ny,nx))
                                q2.append((ny,nx))
        team_q.append(q2)

def move():
    global team

    # 사람 이동
    for i in range(len(team_q)):
        y,x = team_q[i][0]
        for di in dirs:
            ny, nx = y+di[0], x+di[1]
            if 0<=ny<n and 0<=nx<n and maps[ny][nx]:
                if (ny,nx) != team_q[i][1]:
                    team_q[i].appendleft((ny,nx))
                    team_q[i].pop()
                    break
    # 지도에 표시
    for i in range(len(team_q)):
        for j in range(len(team_q[i])):
            ty,tx = team_q[i][j]
            if j == 0:
                new_team[ty][tx] = 1
            elif j==len(team_q[i])-1:
                new_team[ty][tx] = 3
            else:
                new_team[ty][tx] = 2
    team = new_team

def round(k):
    global answer

    a,b = divmod(k,4*n)
    b-=1
    if 0 <= b < n:
        for i in range(n):
            if team[b][i]:
                answer += team[b][i]**2
                team_info_change(b,i)
                break
    elif n <= b < 2*n:
        b = b-n
        for j in range(n-1,-1,-1):
            if team[j][b]:
                answer += team[j][b] ** 2
                team_info_change(j,b)
                break
    elif 2*n <= b < 3*n:
        b = 3*n-b-1
        for i in range(n-1,-1,-1):
            if team[b][i]:
                answer += team[b][i] ** 2
                team_info_change(b,i)
                break
    elif 3*n <= b < 4*n:
        b = 4*n-b-1
        for j in range(n):
            if team[j][b]:
                answer += team[j][b] ** 2
                team_info_change(j,b)
                break

def team_info_change(r,c):
    global team
    idx = 0
    for i in range(len(team_q)):
        if (r,c) in team_q[i]:
            idx = i
            break
    team_q[idx].reverse()

    # 1,3 변경
    sy,sx = team_q[idx][0]
    ey,ex = team_q[idx][-1]
    team[sy][sx] = 1
    team[ey][ex] = 3

n,m,k = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(n)] # 이동 선
team = [row[:] for row in maps] # 사람

for t in team:
    for i in range(n):
        if t[i] not in [1,2,3]:
            t[i] = 0

for j in range(n):
    for i in range(n):
        if maps[j][i] != 0:
            maps[j][i] = 1

answer = 0
for i in range(k):
    one = []  # 1번 위치
    find_one()
    # print("one")
    # print(one)
    team_q = []
    team_search()
    # print("team_q")
    # print(team_q)
    new_team = [[0]*n for _ in range(n)]
    move()
    # print("new_team")
    # for nt in team:
    #     print(nt)
    round(i+1)
    # print("new_team2")
    # for nt in team:
    #     print(nt)
print(answer)