from collections import deque,defaultdict

dirs = [(0,1),(0,-1),(1,0),(-1,0)] # d=1 우->좌 / d=2 하->상
f_dirs = [(-1,0),(0,1),(1,0),(0,-1)]

def d_check(): # 거리 3 이하 도망자 찾기
    escape_lst = []
    for r in range(n):
        for c in range(n):
            if maps[r][c]:
                if (abs(r-fy)+abs(c-fx)) <= 3:
                    for k,v in maps[r][c].items():
                        escape_lst.append([r,c,k,v])
    return escape_lst

def escape(): # 도망가기
    for ey,ex,di,num in escape_list:
        orig_di = di
        while True:
            d = dirs[di]
            ny, nx = ey+d[0], ex+d[1]
            if 0<=ny<n and 0<=nx<n:
                if (ny,nx) == (fy,fx):
                    break
                else:
                    if di in maps[ny][nx].keys():
                        maps[ny][nx][di] += num
                    else:
                        maps[ny][nx][di] = num
                    del maps[ey][ex][orig_di]
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
                flag = True
                break
        follow_list.pop()
        fd = (fd+1)%4
        follow_list.append([fy, fx, fd])
        if flag:
            break

def follow2():
    re_follow_list = list(reversed(follow_list))
    follow_list.pop()
    for f_r,f_c,f_d in re_follow_list:
        follow_list.append([f_r,f_c,(f_d+1)%4])
    follow_list.append([0,0,0])

def catch(): # 도망자 잡기
    global answer
    # print("fy,fx,fd,fc:",fy,fx,fd,fc)
    if fd==0: # 상
        for r in range(fy,min(-1,fy-3),-1):
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
        for c in range(fx,min(-1,fx-3),-1):
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
    escape_list = d_check()
    escape()
    fy, fx, fd = follow_list[i % len(follow_list)]
    catch()
    fc += 1
print(answer)