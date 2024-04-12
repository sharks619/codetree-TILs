dir = [(-1,0),(0,1),(1,0),(0,-1)]

N, M, K = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    for j in range(N):
        graph[i][j] = [graph[i][j]]
playerlist = []
playerdict = {}
scorelist = [0]*M
for t in range(M):
    x, y, d, s = map(int, input().split())
    playerlist.append(t)
    playerdict[t] = [(x-1,y-1),d,s,0]  # 좌표, 방향, 공격력, 총

for _ in range(K):
    # ======= 여기부터 한 턴 시작 =======
    for i in playerlist:

        # 1-1. 첫번째 플레이어부터 이동
        (x,y),d,s,g = playerdict[i]  # 현재 움직이는 녀석의 좌표, 방향, 공격력, 총
        nx, ny = x+dir[d][0], y+dir[d][1]
        if 0>nx or N-1<nx or 0>ny or N-1<ny:
            d = (d+2)%4
            nx, ny = x+dir[d][0], y+dir[d][1]

        movelist = []
        for j in playerlist:
            if (nx,ny) in playerdict[j]:  # 2-2-1. 플레이어가 있다면
                (ex,ey),ed,es,eg = playerdict[j]  # enemy의 줄임말임 ㅋㅋ

                if s+g>es+eg or (s+g==es+eg and s>g):  # 현재 플레이어가 이긴다면
                    winner = (i, nx, ny, d, s, g)
                    loser = (j, ex, ey, ed, es, 0)
                    graph[nx][ny].append(eg)
                else:
                    winner = (j, ex, ey, ed, es, eg)
                    loser = (i, nx, ny, d, s, 0)
                    graph[nx][ny].append(g)
                scorelist[winner[0]] += abs(s+g-es-eg)

                # 2-2-2. 진 플레이어의 이동
                l, lx, ly, ld, ls, lg = loser
                for kk in range(4):
                    lnx, lny = lx+dir[ld][0], ly+dir[ld][1]
                    if 0>lnx or N-1<lnx or 0>lny or N-1<lny:
                        ld = (ld+1)%4
                        lnx, lny = lx+dir[ld][0], ly+dir[ld][1]
                        continue
                    for k in playerlist:
                        if k in (i,j): continue
                        if (lnx,lny) in playerdict[k]:
                            ld = (ld+1)%4
                            lnx, lny = lx+dir[ld][0], ly+dir[ld][1]
                            break
                maxx = max(graph[lnx][lny])
                graph[lnx][lny].remove(maxx)
                lg, maxx = maxx, lg
                graph[lnx][lny].append(maxx)
                movelist.append((l,lnx,lny,ld,ls,lg))

                # 2-2-3. 이긴 플레이어의 이동
                w, wx, wy, wd, ws, wg = winner
                maxx = max(graph[wx][wy])
                graph[wx][wy].remove(maxx)
                if wg<maxx:
                    wg, maxx = maxx, wg
                graph[wx][wy].append(maxx)
                movelist.append((w,wx,wy,wd,ws,wg))
                break

        else:  # 2-1. 플레이어 중에 겹치는 녀석이 없다면
            maxx = max(graph[nx][ny])
            graph[nx][ny].remove(maxx)
            if g<maxx:  # 내 총이 바닥의 큰 것보다 작다면
                g, maxx = maxx, g
            graph[nx][ny].append(maxx)
            playerdict[i] = [(nx,ny),d,s,g]

        if movelist:
            playerdict[movelist[0][0]] = [(movelist[0][1],movelist[0][2]),movelist[0][3],movelist[0][4],movelist[0][5]]
            playerdict[movelist[1][0]] = [(movelist[1][1],movelist[1][2]),movelist[1][3],movelist[1][4],movelist[1][5]]

print(*scorelist)