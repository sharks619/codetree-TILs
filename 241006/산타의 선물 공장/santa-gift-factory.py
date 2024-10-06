from collections import deque, defaultdict

q = int(input())

_, n, m, *args = list(map(int, input().split()))
num = n//m
belt_q = [deque() for _ in range(m)]
belt_s = [set() for _ in range(m)]
belt_dic = defaultdict(bool)


for i in range(m):
    belt_dic[i+1] = False
    for j in range(i*(n//m), (i+1)*(n//m)):
        belt_q[i].append((args[j], args[j+n]))
        belt_s[i].add(args[j])

def down(x):
    ans = 0
    for i in range(m):
        if belt_q[i]:  # q가 비어있지 않은 경우에만 pop 시도 (벨트 고장일 수도..!)
            c_id, c_w = belt_q[i].popleft()
            if c_w <= x:
                ans += c_w
                belt_s[i].remove(c_id)
            else:
                belt_q[i].appendleft((c_id, c_w))  # 다시 앞에 넣기
    return ans

def remove_box(x):
    for i in range(m):
        for c_id, c_w in belt_q[i]:
            if c_id == x:
                belt_q[i].remove((c_id, c_w))
                belt_s[i].remove(c_id)
                return c_id
    return -1

def check_box(x):
    for i in range(m):
        cnt = 0
        for c_id, c_w in belt_q[i]:
            cnt += 1
            if c_id == x:
                belt_q[i].rotate(-1 * cnt)
                return i + 1
    return -1

def move_box(x):
    nxt_num = -1
    for i in range(1, m):
        nxt_num = (x - 1 + i) % m
        if not belt_dic[nxt_num + 1]:
            belt_dic[nxt_num + 1] = True
            break

    if nxt_num != -1:
        belt_q[nxt_num].extend(belt_q[x-1])
        belt_q[x-1] = deque()

        belt_s[nxt_num].update(belt_s[x-1])
        belt_s[x-1] = set()

        belt_dic[x] = False  # 벨트 이동 후 상태 초기화

    return x


for _ in range(q-1):
    cmd, *args = list(map(int, input().split()))

    if cmd == 200:
        w_max = args[0]
        print(down(w_max))

    elif cmd == 300:
        r_id = args[0]
        print(remove_box(r_id))

    elif cmd == 400:
        f_id = args[0]
        print(check_box(f_id))

    elif cmd == 500:
        b_num = args[0]
        if belt_dic[b_num]:
            print(-1)
        else:
            print(move_box(b_num))