from collections import defaultdict

max_m = 10
weight = {}  # id:weight
prv, nxt = defaultdict(lambda: 0), defaultdict(lambda: 0)  # 0은 없다는 뜻
head = [0] * max_m
tail = [0] * max_m
broken = [False] * max_m
belt_num = defaultdict(lambda: -1)  # id:belt num, -1이면 사라진 것

q = int(input())
_, n, m, *args = list(map(int, input().split()))
ids, ws = args[:n], args[n:]

for i in range(n):
    weight[ids[i]] = ws[i]

for i in range(m):
    head[i] = ids[i * (n // m)]
    tail[i] = ids[(i + 1) * (n // m) - 1]
    for j in range(i * (n // m), (i + 1) * (n // m)):
        belt_num[ids[j]] = i
        if j < (i + 1) * (n // m) - 1:
            nxt[ids[j]] = ids[j + 1]
            prv[ids[j + 1]] = ids[j]

def box_down(x):
    ans = 0
    for i in range(m):
        if not broken[i]:
            h_id = head[i]
            if h_id == 0:  # 벨트가 비어있을 때 처리
                continue
            if weight[h_id] <= x:
                ans += weight[h_id]
                belt_num[h_id] = -1  # 벨트에서 제거
                head[i] = nxt[h_id]  # head 업데이트
                if head[i] != 0:
                    prv[head[i]] = 0  # 새로운 head의 prv를 0으로 설정
                else:
                    tail[i] = 0  # 벨트가 비었으면 tail도 0으로 설정
                nxt[h_id] = 0  # 제거된 상자의 nxt 초기화
            else:
                # 맨 뒤로 보내기
                tail[i] = h_id
                head[i] = nxt[h_id]
                nxt[tail[i]] = h_id
                prv[h_id] = tail[i]
                nxt[h_id] = 0
    return ans

def box_remove(x):
    belt_n = belt_num[x]

    if belt_n == -1:
        return -1

    h_id, t_id = head[belt_n], tail[belt_n]
    p_id, n_id = prv[x], nxt[x]

    if x == h_id:
        head[belt_n] = n_id
    elif x == t_id:
        tail[belt_n] = p_id

    if n_id != 0:
        prv[n_id] = p_id
    if p_id != 0:
        nxt[p_id] = n_id

    prv[x], nxt[x] = 0, 0
    belt_num[x] = -1

    return x

def box_check(x):
    belt_n = belt_num[x]

    if belt_n == -1:
        return -1

    h_id = head[belt_n]

    if x != h_id:
        # 상자를 앞으로 보내기
        p_id, n_id = prv[x], nxt[x]

        if x == tail[belt_n]:
            tail[belt_n] = p_id
        if p_id != 0:
            nxt[p_id] = n_id
        if n_id != 0:
            prv[n_id] = p_id

        nxt[x] = h_id
        prv[h_id] = x
        head[belt_n] = x
        prv[x] = 0

    return belt_n + 1

def box_move(x):
    if broken[x - 1]:
        return -1

    broken[x - 1] = True

    nxt_n = 0
    for i in range(1, m):
        nxt_n = (x - 1 + i) % m
        if not broken[nxt_n]:
            break

    h_id, t_id = head[x - 1], tail[x - 1]

    if h_id == 0:  # 고장난 벨트가 비어있는 경우
        return x

    while h_id != 0:
        belt_num[h_id] = nxt_n
        h_id = nxt[h_id]

    # 벨트 병합
    if head[nxt_n] == 0:
        head[nxt_n] = head[x - 1]
    else:
        nxt[tail[nxt_n]] = head[x - 1]
        prv[head[x - 1]] = tail[nxt_n]

    tail[nxt_n] = tail[x - 1]

    # 고장난 벨트 초기화
    head[x - 1], tail[x - 1] = 0, 0

    return x

for _ in range(q - 1):
    cmd, *args = list(map(int, input().split()))

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