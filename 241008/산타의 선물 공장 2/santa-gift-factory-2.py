from collections import defaultdict

q = int(input())
_,n,m,*args = list(map(int, input().split()))

MAX_N = 100000

prv = defaultdict(lambda: 0)
nxt = defaultdict(lambda: 0)
head = [0] * MAX_N  # 각 벨트의 첫 번째 상자
tail = [0] * MAX_N  # 각 벨트의 마지막 상자
num_gift = [0] * MAX_N


boxes = [[] for _ in range(n)]
for i in range(m):
    box_loc = args[i]-1
    box_id = i+1

    boxes[box_loc].append(box_id)

    if head[box_loc] == 0:
        head[box_loc] = box_id
        prv[box_id] = 0
    else:
        nxt[tail[box_loc]] = box_id
        prv[box_id] = tail[box_loc]
    tail[box_loc] = box_id
    nxt[box_id] = 0

for i in range(n):
    num_gift[i] = len(boxes[i])


def move_all(a,b):
    # a 선물 x
    if num_gift[a-1]==0:
        return num_gift[b-1]

    # b 선물 x
    if num_gift[b-1]==0:
        head[b-1] = head[a-1]
        tail[b-1] = tail[a-1]

    # 둘 다 선물 존재
    else:
        ah_id = head[a-1]
        bh_id = head[b-1]
        at_id = tail[a-1]

        head[b-1] = ah_id
        prv[bh_id] = at_id
        nxt[at_id] = bh_id

    head[a-1] = tail[a-1] = 0

    num_gift[b-1] += num_gift[a-1]
    num_gift[a-1] = 0

    return num_gift[b-1]

def replace_first(a,b):
    ah_id = head[a-1]
    bh_id = head[b-1]

    # 둘 다 선물 x
    if ah_id == 0 and bh_id == 0:
        return 0

    # a 만 없음
    if ah_id == 0:
        bn_id = nxt[bh_id]

        # a 벨트 정보 변경
        head[a-1] = bh_id
        tail[a-1] = bh_id
        prv[bh_id] = 0
        nxt[bh_id] = 0

        # b 벨트 정보 변경
        # b 박스 1개 인지 확인
        if head[b-1] == tail[b-1]:
            head[b-1] = tail[b-1] = 0
        else:
            head[b-1] = bn_id
            prv[bn_id] = 0

        num_gift[a-1] += 1
        num_gift[b-1] -= 1

    # b 만 없음
    elif bh_id == 0:
        an_id = nxt[ah_id]

        # a 벨트 정보 변경
        # a 박스 1개 인지 확인
        if head[a-1] == tail[a-1]:
            head[a-1] = tail[a-1] = 0
        else:
            head[a-1] = an_id
            prv[an_id] = 0

        # b 벨트 정보 변경
        head[b-1] = ah_id
        tail[b-1] = ah_id
        prv[ah_id] = 0
        nxt[ah_id] = 0

        num_gift[a-1] -= 1
        num_gift[b-1] += 1

    else:
        an_id = nxt[ah_id]
        bn_id = nxt[bh_id]

        # a 벨트 정보 변경
        head[a - 1] = bh_id
        prv[bh_id] = 0
        nxt[bh_id] = an_id

        # a 박스 1개 인지 확인
        if an_id == 0:
            tail[a-1] = bh_id
        else:
            prv[an_id] = bh_id

        # b 벨트 정보 변경
        head[b - 1] = ah_id
        prv[ah_id] = 0
        nxt[ah_id] = bn_id

        # b 박스 1개 인지 확인
        if bn_id == 0:
            tail[b-1] = ah_id
        else:
            prv[bn_id] = ah_id

    return num_gift[b-1]

def box_share(a,b):
    num = num_gift[a-1]//2

    if num==0:
        return num_gift[b-1]

    # 이동할 a 박스 id 추출 / 시작:a_id, 끝: new_b_id
    a_id = head[a-1]

    c = 0
    a_num = a_id
    while True:
        a_num = nxt[a_num]
        c += 1
        if c == num:
            break

    new_ah_id = a_num
    new_b_id = prv[a_num]

    # a 정보 변경
    head[a-1] = new_ah_id
    prv[new_ah_id] = 0

    # b 선물 x
    if head[b-1]==0:
        # b 정보 변경
        head[b-1] = a_id
        tail[b-1] = new_b_id
        prv[new_ah_id] = 0
        nxt[new_b_id] = 0

    # 둘 다 선물 존재
    else:
        bh_id = head[b-1]

        head[b-1] = a_id

        prv[a_id] = 0
        nxt[new_b_id] = bh_id
        prv[bh_id] = new_b_id

    num_gift[a - 1] -= num
    num_gift[b - 1] += num

    return num_gift[b-1]

def box_info(x):
    a = prv[x]
    b = nxt[x]
    if a == 0:
        a = -1
    if b == 0:
        b = -1

    return a+2*b

def belt_info(x):
    a = head[x-1]
    b = tail[x-1]
    c = num_gift[x-1]
    if a == 0:
        a = -1
    if b == 0:
        b = -1

    return a+2*b+3*c

for _ in range(q-1):
    cmd, *args = list(map(int, input().split()))

    # print()
    # print(cmd, args)
    # print("전")
    # print("head", head)
    # print("tail", tail)
    # print("belt_num", belt_num)
    # print("prv", prv)
    # print("nxt", nxt)
    # print()

    if cmd == 200:
        m_src, m_dst = args
        print(move_all(m_src, m_dst))

    elif cmd == 300:
        m_src, m_dst = args
        print(replace_first(m_src, m_dst))

    elif cmd == 400:
        m_src, m_dst = args
        print(box_share(m_src, m_dst))

    elif cmd == 500:
        p_num = args[0]
        print(box_info(p_num))

    elif cmd == 600:
        b_num = args[0]
        print(belt_info(b_num))


    # print("후")
    # print("head", head)
    # print("tail", tail)
    # print("belt_num", belt_num)
    # print("prv", prv)
    # print("nxt", nxt)