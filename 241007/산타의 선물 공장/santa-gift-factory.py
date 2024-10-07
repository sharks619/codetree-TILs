from collections import defaultdict

max_m = 10
weight = {} # id:weight
prv, nxt = defaultdict(lambda: 0), defaultdict(lambda: 0) # 0은 없다는 뜻
head = [0] * max_m
tail = [0] * max_m
broken = [False] * max_m
belt_num = defaultdict(lambda: -1) # id:belt num, -1이면 사라진 것


q = int(input())
_, n, m, *args = list(map(int, input().split()))
ids, ws = args[:n], args[n:]

for i in range(n):
    weight[ids[i]] = ws[i]

for i in range(m):
    head[i] = ids[i*(n//m)]
    tail[i] = ids[(i+1)*(n//m)-1]
    for j in range(i*(n//m), (i+1)*(n//m)):
        belt_num[ids[j]] = i
        if j < (i+1)*(n//m)-1:
            nxt[ids[j]] = ids[j+1]
            prv[ids[j+1]] = ids[j]


def box_down(x):
    ans = 0
    for i in range(m):
        if not broken[i]:
            h_id, t_id = head[i], tail[i]
            if h_id == 0:
                continue
            # w_max 이하라면 하차
            if weight[h_id] <= x:
                ans += weight[h_id]
                head[i] = nxt[h_id]
                # 벨트 위 박스 2개 이상인 경우
                if head[i] != 0:
                    prv[head[i]] = 0
                # 벨트 위 박스 1개인 경우
                else:
                    tail[i] = 0
            # 아니면 맨 뒤로 이동
            else:
                tail[i] = h_id
                head[i] = nxt[h_id]
                prv[h_id] = t_id
                nxt[t_id] = h_id
            nxt[h_id] = 0
            belt_num[h_id] = -1

    return ans

def box_remove(x):
    belt_n = belt_num[x]

    if belt_n == -1:
        return -1

    h_id, t_id = head[belt_n], tail[belt_n]
    p_id, n_id = prv[x], nxt[x]

    # 삭제하는 박스가
    # 하나 남은 원소라면
    if h_id==n_id:
        head[belt_n] = tail[belt_n] = 0

    # head일 경우
    elif x == h_id:
        head[belt_n] = n_id
        prv[n_id] = 0

    # tail일 경우
    elif x == t_id:
        tail[belt_n] = p_id
        nxt[p_id] = 0

    # 중간 원소일 경우
    else:
        nxt[p_id] = n_id
        prv[n_id] = p_id

    prv[x] = nxt[x] = 0
    belt_num[x] = -1

    return x

def box_check(x):
    belt_n = belt_num[x]

    if belt_n == -1:
        return -1

    h_id, t_id = head[belt_n], tail[belt_n]
    p_id, n_id = prv[x], nxt[x]

    # head가 아닌 경우만 변경
    if x != h_id:

        # head 갱신
        head[belt_n] = x
        prv[x] = 0

        # tail 갱신
        tail[belt_n] = p_id
        nxt[p_id] = 0

        nxt[t_id] = h_id
        prv[h_id] = t_id

    return belt_n+1

def box_move(x):
    # 이미 망가졌으면 패스
    if broken[x-1]:
        return -1

    broken[x-1] = True

    # 빈 벨트라면 패스
    if head[x-1] == 0:
        return x

    nxt_n = 0
    for i in range(1,m):
        nxt_n = (x-1+i)%m
        if not broken[nxt_n]:
            break

    h_id, t_id = head[x-1], tail[x-1]
    n_h_id, n_t_id = head[nxt_n], tail[nxt_n]

    # 옮기려는 정상 벨트가 비어 있으면
    if n_h_id == 0:
        head[nxt_n] = head[x-1]
        tail[nxt_n] = tail[x-1]

    else:
        tail[nxt_n] = t_id
        nxt[n_t_id] = h_id
        prv[h_id] = n_t_id

    # head부터 tail까지 belt_num 갱신
    while True:
        belt_num[h_id] = nxt_n
        n_id = nxt[h_id]
        if n_id != 0:
            belt_num[n_id] = nxt_n
            h_id = n_id
        else:
            break

    head[x-1] = tail[x-1] = 0

    return x

for _ in range(q-1):
    cmd, *args = list(map(int, input().split()))

    # print()
    # print(cmd, *args)
    # print("전")
    # print("head", head)
    # print("tail", tail)
    # print("prv", prv)
    # print("nxt", nxt)
    # print()

    if cmd == 200:
        w_max = args[0]
        print(box_down(w_max))

    elif cmd == 300:
        r_id = args[0]
        print(box_remove(r_id))

    elif cmd == 400:
        f_id = args[0]
        print(box_check(f_id))

    elif cmd == 500:
        b_num = args[0]
        print(box_move(b_num))

    # print()
    # print(cmd, *args)
    # print("후")
    # print("head", head)
    # print("tail", tail)
    # print("prv", prv)
    # print("nxt", nxt)
    # print()