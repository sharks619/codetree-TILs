dirs = [(0,1),(0,-1),(1,0),(-1,0)] # d=1 우->좌 / d=2 하->상
f_dirs = [(-1,0),(0,1),(1,0),(0,-1)]

def d_check(): # 거리 3 이하 도망자 찾기
    escape_lst = []
    remain_lst = []
    for r in range(n):
        for c in range(n):
            if maps[r][c]:
                if (abs(r-fy)+abs(c-fx)) <= 3:
                    for k,v in maps[r][c].items():
                        escape_lst.append([r,c,k,v])
                else:
                    for k,v in maps[r][c].items():
                        remain_lst.append([r,c,k,v])
    return escape_lst,remain_lst

def escape(): # 도망가기
    global maps

    new_map = [[{} for _ in range(n)] for _ in range(n)]
    for ey,ex,di,num in escape_list:
        while True:
            d = dirs[di]
            ny, nx = ey+d[0], ex+d[1]
            if 0<=ny<n and 0<=nx<n:
                if (ny,nx) == (fy,fx):
                    if di in new_map[ey][ex].keys():
                        new_map[ey][ex][di] += num
                    else:
                        new_map[ey][ex][di] = num
                    break
                else:
                    if di in new_map[ny][nx].keys():
                        new_map[ny][nx][di] += num
                    else:
                        new_map[ny][nx][di] = num
                    break
            else:
                if di==0:
                    di=1
                elif di==2:
                    di=3
                elif di==1:
                    di=0
                elif di==3:
                    di=2
    for ry,rx,rd,rn in remain_list:
        if rd in new_map[ry][rx].keys():
            new_map[ry][rx][rd] += rn
        else:
            new_map[ry][rx][rd] = rn

    maps = new_map

def follow(fy,fx,fd): # 술래 움직임
    t=0
    flag = False
    while True:
        if fd in [0,2]:
            t += 1
        for _ in range(t):
            fy += f_dirs[fd][0]
            fx += f_dirs[fd][1]
            follow_list.append([fy,fx,fd])
            if (fy, fx) == (0, 0):
                follow_list.pop()
                follow_list.append([fy, fx, (fd+2)%4])
                flag = True
                break
        if flag:
            break
        follow_list.pop()
        fd = (fd+1)%4
        follow_list.append([fy,fx,fd])

def follow2(): # 술래 움직임2
    f2y,f2x = 0,0
    f2d = 2
    visited = [[0] * n for _ in range(n)]
    visited[f2y][f2x] = 1
    q = []
    q.append([f2y,f2x,f2d])

    while True:
        ny, nx = f2y+f_dirs[f2d][0], f2x+f_dirs[f2d][1]
        if 0<=ny<n and 0<=nx<n and not visited[ny][nx]:
            visited[ny][nx] = 1
            q.append([ny, nx, f2d])
            f2y,f2x = ny,nx
            if (f2y,f2x) == ((n-1)//2, (n-1)//2):
                q.pop()
                q.append([f2y, f2x, (f2d+2)%4])
                break
        else:
            f2d = (f2d+3)%4
            q.pop()
            q.append([f2y, f2x, f2d])

    follow_list.pop()
    follow_list.extend(q)
    
def catch(): # 도망자 잡기
    global answer
    # print("fy,fx,fd,fc:",fy,fx,fd,fc)
    if fd==0: # 상
        for r in range(fy,max(-1,fy-3),-1):
            if maps[r][fx]:
                if not tree[r][fx]:
                    answer += fc*sum([v for v in maps[r][fx].values()])
                    maps[r][fx] = {}
    elif fd==1: # 우
        for c in range(fx,min(n,fx+3)):
            if maps[fy][c]:
                if not tree[fy][c]:
                    answer += fc*sum([v for v in maps[fy][c].values()])
                    maps[fy][c] = {}
    elif fd==2: #하
        for r in range(fy,min(n,fy+3)):
            if maps[r][fx]:
                if not tree[r][fx]:
                    answer += fc*sum([v for v in maps[r][fx].values()])
                    maps[r][fx] = {}
    elif fd==3: # 좌
        for c in range(fx,max(-1,fx-3),-1):
            if maps[fy][c]:
                if not tree[fy][c]:
                    answer += fc*sum([v for v in maps[fy][c].values()])
                    maps[fy][c] = {}

n,m,h,k = map(int, input().split())
maps = [[{} for _ in range(n)] for _ in range(n)] # 도망자 위치
tree = [[0]*n for _ in range(n)] # 나무 위치

for _ in range(m):
    x,y,d = map(int, input().split()) # d=1 0우->1좌 / d=2 2하->3상
    if d == 1:
        maps[x-1][y-1][d-1] = 1
    elif d == 2:
        maps[x-1][y-1][d] = 1

for _ in range(h):
    tx,ty = map(int, input().split())
    tree[tx-1][ty-1] = 1

fy = fx = (n-1)//2 # 현 위치
fd = 0 # 현 방향
fc = 1 # 턴 수

answer = 0

follow_list = []
follow(fy,fx,fd)
follow2()

fy = fx = (n-1)//2 # 현 위치

for i in range(k):
    escape_list,remain_list = d_check()
    # print("시작")
    # for ma in maps:
    #     print(ma)
    # print()
    escape()
    # print("escape")
    # for ma in maps:
    #     print(ma)
    # print()
    fy, fx, fd = follow_list[i % len(follow_list)]
    catch()
    # print("catch")
    # for ma in maps:
    #     print(ma)
    # print()
    fc += 1
    # print("ans:",answer)
print(answer)