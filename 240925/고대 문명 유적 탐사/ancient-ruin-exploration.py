from collections import deque

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 입력 받기
k, m = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(5)]
nums = deque(list(map(int, input().split())))

# 90, 180, 270도 회전 함수
def r_90(arr):
    return [list(a[::-1]) for a in zip(*arr)]

def r_180(arr):
    return [list(a[::-1]) for a in arr][::-1]

def r_270(arr):
    return [list(a) for a in zip(*arr)][::-1]

# 회전 딕셔너리
r_dic = {0: r_90, 1: r_180, 2: r_270}

# bfs 함수에서 탐색과 제거 리스트 생성
def bfs(i, r, c, maps, max_cnt):

    new_map = [row[:] for row in maps]

    # 회전할 3x3 영역 선택 및 회전
    sub_map = [row[c-1:c+2] for row in new_map[r-1:r+2]]
    r_result = r_dic[i](sub_map)

    for idx in range(3):
        new_map[r-1+idx][c-1:c+2] = r_result[idx]

    remove_list = []
    v = [[0] * 5 for _ in range(5)]
    total_cnt = 0

    # 5x5 탐색
    for cc in range(5):
        for cr in range(5):
            if v[cr][cc] == 0:  # 방문 안한 좌표만
                q = deque([(cr, cc)])
                r_lst = [(cr, cc)]
                v[cr][cc] = 1
                cnt = 1
                while q:
                    cr, cc = q.popleft()
                    for d in dirs:
                        nr, nc = cr + d[0], cc + d[1]
                        if 0 <= nr < 5 and 0 <= nc < 5 and not v[nr][nc] and new_map[nr][nc] == new_map[cr][cc]:
                            q.append((nr, nc))
                            r_lst.append((nr, nc))
                            v[nr][nc] = 1
                            cnt += 1

                if cnt >= 3:
                    total_cnt += cnt
                    remove_list.extend(r_lst)

    # 최대 획득 카운트 업데이트
    if total_cnt >= max_cnt:
        max_cnt = total_cnt
        return max_cnt, [total_cnt, i, r, c, remove_list]
    return max_cnt, None

# 채우기 함수
def refill(new_map, nums, mlst):
    for r, c in mlst:
        new_map[r][c] = 0

    for x in range(5):
        for y in range(4, -1, -1):
            if new_map[y][x] == 0:
                new_map[y][x] = nums.popleft()

# 유물 제거 함수
def remove(new_map, nums):
    ans = 0
    while True:
        remove_list = []
        v = [[0] * 5 for _ in range(5)]
        for c in range(5):
            for r in range(5):
                if v[r][c] == 0:
                    q = deque([(r, c)])
                    r_lst = [(r, c)]
                    v[r][c] = 1
                    cnt = 1
                    while q:
                        cr, cc = q.popleft()
                        for d in dirs:
                            nr, nc = cr + d[0], cc + d[1]
                            if 0 <= nr < 5 and 0 <= nc < 5 and not v[nr][nc] and new_map[nr][nc] == new_map[cr][cc]:
                                q.append((nr, nc))
                                r_lst.append((nr, nc))
                                v[nr][nc] = 1
                                cnt += 1
                    if cnt >= 3:
                        remove_list.extend(r_lst)
        if remove_list:
            ans += len(remove_list)
            refill(new_map, nums, remove_list)
        else:
            break
    return ans

# 탐사 진행
answer = []
for _ in range(k):
    max_cnt = 0
    sub = []
    for i in range(3):  # 90도, 180도, 270도
        for c in range(1, 4):
            for r in range(1, 4):
                max_cnt, result = bfs(i, r, c, maps, max_cnt)
                if result:
                    sub.append(result)

    if not sub:
        break
    else:
        m_cnt, mi, mr, mc, mlst = sorted(sub, key=lambda x: -x[0])[0]
        new_map = [row[:] for row in maps]

        # 선택된 회전 적용
        sub_map = [row[mc-1:mc+2] for row in new_map[mr-1:mr+2]]
        r_result = r_dic[mi](sub_map)
        for idx in range(3):
            new_map[mr-1+idx][mc-1:mc+2] = r_result[idx]

        ans = m_cnt
        refill(new_map, nums, mlst)

        ans += remove(new_map, nums)
        maps = new_map

    if ans:
        answer.append(ans)

# 결과 출력
print(*answer)