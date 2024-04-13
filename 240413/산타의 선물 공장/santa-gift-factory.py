from collections import defaultdict

max_m = 10
weight = {} # id별 상자 무게 저장
n,m,q = 0,0,0

prv = defaultdict(lambda: 0)
nxt = defaultdict(lambda: 0)

head = [0]*max_m
tail = [0]*max_m

broken_belt = [0]*max_m
belt_num = defaultdict(lambda: -1) # {id:belt 번호}

def build(info):
    global n,m

    n,m = info[1],info[2]
    ids = info[3:3+n]
    ws = info[3+n:3+n+n]

    for i in range(n):
        weight[ids[i]] = ws[i]

        size = n//m
        for i in range(m):
            head[i] = ids[i*size]
            tail[i] = ids[(i+1)*size-1]
            for j in range(i*size,(i+1)*size):
                belt_num[ids[j]]=i
                if j < (i+1)*size-1:
                    nxt[ids[j]] = ids[j+1]
                    prv[ids[j+1]] = ids[j]

def remove_id(id,removebelt):
    b_num = belt_num[id]

    if removebelt:
        belt_num[id]=-1

    # 제거하려는게 하나만 남은 상황
    if head[b_num]==tail[b_num]:
        head[b_num] = tail[b_num] = 0

    # 맨 앞 하나만 삭제
    elif id == head[b_num]:
        nid = nxt[id]
        head[b_num] = nid
        prv[nid] = 0

    # 맨 뒤 하나만 삭제
    elif id == tail[b_num]:
        pid = prv[id]
        tail[b_num] = pid
        nxt[pid] = 0

    # 중간 하나만 삭제
    else:
        pid = prv[id]
        nid = nxt[id]
        nxt[pid] = nid
        prv[nid] = pid

    nxt[id]=prv[id]=0

# tgt_id 뒤에 id 넣음
# 근데 이렇게만 해도 되나..?
def push_id(tgt_id, id):
    nxt[tgt_id]=id
    prv[id]=tgt_id

    b_num = belt_num[tgt_id]
    if tail[b_num]==tgt_id:
        tail[b_num] = id

def drop_off(info):
    w_max = info[1]

    w_sum = 0
    for i in range(m):
        if broken_belt[i]:
            continue

        if head[i] != 0:
            _id = head[i]
            w = weight[_id]

            if w <= w_max:
                w_sum += w
                remove_id(_id,True)
            elif nxt[_id] != 0:
                remove_id(_id,False)
                push_id(tail[i],_id)
    print(w_sum)

def remove(info):
    r_id = info[1]
    if belt_num[r_id] == -1:
        print(-1)
        return
    remove_id(r_id,True)
    print(r_id)

def check(info):
    f_id = info[1]

    if belt_num[f_id]==-1:
        print(-1)
        return

    b_num = belt_num[f_id]
    if head[b_num] != f_id:
        orig_tail = tail[b_num]
        orig_head = head[b_num]
        new_tail = prv[f_id]
        tail[b_num] = new_tail
        nxt[new_tail] = 0

        nxt[orig_tail] = orig_head
        prv[orig_head] = orig_tail

        head[b_num] = f_id

    print(b_num+1)

def broken(info):
    b_num = info[1]
    b_num -= 1

    if broken_belt[b_num]:
        print(-1)
        return

    broken_belt[b_num] = 1

    # 빈 belt
    if head[b_num] == 0:
        print(b_num+1)
        return

    nxt_num = b_num
    while True:
        nxt_num = (nxt_num+1)%m

        if not broken_belt[nxt_num]:
            if tail[nxt_num] == 0:
                head[nxt_num] = head[b_num]
                tail[nxt_num] = tail[b_num]
            else:
                push_id(tail[nxt_num],head[b_num])
                tail[nxt_num] = tail[b_num]

            h_id = head[b_num]
            while h_id != 0 :
                belt_num[h_id] = nxt_num
                h_id = nxt[h_id]

            head[b_num] = tail[b_num] = 0
            break
    print(b_num+1)

q = int(input())
for _ in range(q):
    info = list(map(int, input().split()))
    type = info[0]

    if type == 100:
        build(info)
    elif type == 200:
        drop_off(info)
    elif type == 300:
        remove(info)
    elif type == 400:
        check(info)
    elif type == 500:
        broken(info)