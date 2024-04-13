dirs = [(-1,0),(0,1),(1,0),(0,-1)] # ↑, →, ↓, ←

n,m,k = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(n)]
for r in range(n):
    for c in range(n):
        maps[r][c] = [maps[r][c]]

p_list = []
p_dict = {}
score = [0]*m

for i in range(m):
    x,y,d,s = map(int, input().split())
    p_list.append(i)
    p_dict[i] = [(x-1,y-1),d,s,0] # 위치,방향,능력치,총

for _ in range(k):
    for i in p_list:
        (y,x),d,s,g = p_dict[i]
        while 1:
            ny,nx = y+dirs[d][0], x+dirs[d][1]
            if 0<=ny<n and 0<=nx<n:
                break
            else:
                d = (d+2)%4

        # ny,nx = y+dirs[d][0], x+dirs[d][1]
        # if 0 > ny or ny >= n or 0 > nx or nx >= n:
        #     d = (d+2)%4
        #     ny,nx = y+dirs[d][0],x+dirs[d][1]

        move_list = []
        for j in p_list:
            if (ny,nx) in p_dict[j]:
                (ey,ex),ed,es,eg = p_dict[j]

                if s+g>es+eg or (s+g==es+eg and s>es):
                    w = (i,ny,nx,d,s,g)
                    l = (j,ey,ex,ed,es,0)
                    maps[ey][ex].append(eg)
                else:
                    w = (j,ey,ex,ed,es,eg)
                    l = (i,ny,nx,d,s,0)
                    maps[ny][nx].append(g)
                score[w[0]] += abs(s+g-es-eg)

                # 패배자 이동
                lidx,ly,lx,ld,ls,lg = l
                # flag = False
                # while 1:
                #     lny,lnx = ly+dirs[ld][0],lx+dirs[ld][1]
                #     if 0<=lny<n and 0<=lnx<n:
                #         for p in p_list:
                #             if p in (i,j):
                #                 continue
                #             if (lny,lnx) in p_dict[p]:
                #                 ld = (ld+1)%4
                #             else:
                #                 flag = True
                #             break
                #     else:
                #         ld = (ld+1)%4
                #     if flag:
                #         break

                for _ in range(4):
                    lny,lnx = ly+dirs[ld][0],lx+dirs[ld][1]
                    if 0 > lny or lny >= n or 0 > lnx or lnx >= n:
                        ld = (ld+1)%4
                        lny,lnx = ly+dirs[ld][0], lx+dirs[ld][1]
                        continue
                    for p in p_list:
                        if p in (i,j):
                            continue
                        if (lny,lnx) in p_dict[p]:
                            ld = (ld+1)%4
                            lny,lnx = ly+dirs[ld][0],lx+dirs[ld][1]
                            break

                best_lg = max(maps[lny][lnx])
                maps[lny][lnx].remove(best_lg)
                maps[lny][lnx].append(lg)
                move_list.append((lidx,lny,lnx,ld,ls,best_lg))

                # 승리자 이동
                widx,wy,wx,wd,ws,wg = w
                best_wg = max(maps[wy][wx])
                if wg < best_wg:
                    maps[wy][wx].remove(best_wg)
                    maps[wy][wx].append(wg)
                    move_list.append((widx,wy,wx,wd,ws,best_wg))
                else:
                    move_list.append((widx,wy,wx,wd,ws,wg))
                break
        else:
            best_g = max(maps[ny][nx])
            if g < best_g:
                maps[ny][nx].remove(best_g)
                maps[ny][nx].append(g)
                p_dict[i] = [(ny,nx),d,s,best_g]
            else:
                p_dict[i] = [(ny,nx),d,s,g]

        if move_list:
            p_dict[move_list[0][0]] = [(move_list[0][1],move_list[0][2]),move_list[0][3],move_list[0][4],move_list[0][5]]
            p_dict[move_list[1][0]] = [(move_list[1][1],move_list[1][2]),move_list[1][3],move_list[1][4],move_list[1][5]]

print(*score)