import sys
from collections import deque

INT_MAX = sys.maxsize
EMPTY = (-1, -1)

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)] # 0: 빈 칸, 1: 베이스 캠프, 2: 갈 수 없음
cvs_list = []
for _ in range(m):
    x, y = tuple(map(int, input().split()))
    cvs_list.append((x-1, y-1))

people = [EMPTY] * m
curr_t = 0
dxs = [-1, 0, 0, 1]
dys = [0, -1, 1, 0]
# 최단거리 결과 기록
step = [[0] * n for _ in range(n)]
visited = [[False] * n for _ in range(n)]

def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

def can_go(x, y):
    return in_range(x, y) and not visited[x][y] and grid[x][y] != 2

def bfs(s_pos):
    for i in range(n):
        for j in range(n):
            visited[i][j] = False
            step[i][j] = 0

    q = deque()
    q.append(s_pos)
    sx,sy = s_pos
    visited[sx][sy] = True
    step[sx][sy] = 0

    while q:
        x,y = q.popleft()

        for dx, dy in zip(dxs, dys):
            nx, ny = x + dx, y + dy
            if can_go(nx,ny):
                visited[nx][ny] = True
                step[nx][ny] = step[x][y] + 1
                q.append((nx,ny))

def simulation():
    # step 1
    for i in range(m):
        if people[i]==EMPTY or people[i]==cvs_list[i]:
            continue
        bfs(cvs_list[i])

        px,py = people[i]
        min_d = INT_MAX
        m_x,m_y = -1,-1
        for dx, dy in zip(dxs, dys):
            nx, ny = px + dx, py + dy
            if in_range(nx,ny) and visited[nx][ny] and min_d>step[nx][ny]:
                min_d = step[nx][ny]
                m_x, m_y = nx,ny
        people[i] = (m_x, m_y)

    # step 2
    for i in range(m):
        if people[i] == cvs_list[i]:
            px,py = people[i]
            grid[px][py] = 2

    # step 3
    if curr_t > m:
        return

    bfs(cvs_list[curr_t-1])

    # Step 3-2. 편의점에서 가장 가까운 베이스 캠프를 선택합니다.
    #           i, j가 증가하는 순으로 돌리기 때문에
    #           가장 가까운 베이스 캠프가 여러 가지여도
    #           알아서 (행, 열) 우선순위대로 골라집니다.
    min_d = INT_MAX
    m_x,m_y = -1,-1

    for i in range(n):
        for j in range(n):
            if visited[i][j] and grid[i][j]==1 and min_d>step[i][j]:
                min_d = step[i][j]
                m_x,m_y = i,j

    people[curr_t-1] = (m_x,m_y)
    grid[m_x][m_y] = 2

def end():
    for i in range(m):
        if people[i]!=cvs_list[i]:
            return False
    return True

while 1:
    curr_t += 1
    simulation()
    if end():
        break
print(curr_t)