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
        belt_q[i].append((args[j],args[j+n]))
        belt_s[i].add(args[j])
def down(x):
    ans = 0
    for i in range(m):
        c_id, c_w = belt_q[i].popleft()
        if c_w <= x:
            ans += c_w
            belt_s[i].remove(c_id)
        else:
            belt_q[i].append((c_id,c_w))
            belt_s[i].add(c_id)
    return ans

def remove_box(x):
    ans = 0
    flag = False
    for i in range(m):
        for c_id,c_w in belt_q[i]:
            if c_id==x:
                belt_q[i].remove((c_id,c_w))
                belt_s[i].remove(c_id)
                flag = True
                ans = c_id
                break
        if flag:
            break

    if not flag:
        return -1
    return ans

def check_box(x):
    ans = 0
    flag = False
    for i in range(m):
        cnt = 0
        for c_id,c_w in belt_q[i]:
            cnt += 1
            if c_id==x:
                belt_q[i].rotate(-1*cnt)
                ans = i+1
                flag = True
                break
        if flag:
            break

    if not flag:
        return -1
    else:
        return ans

def move_box(x):
    nxt_num = 0
    for i in range(1,m):
        if not belt_dic[(x-1+i)%m]:
            belt_dic[(x-1+i)%m] = True
            nxt_num = (x-1+i)%m

    belt_q[nxt_num].extend(belt_q[x-1])
    belt_q[x-1] = deque()

    belt_s[nxt_num].update(belt_s[x-1])
    belt_s[x-1] = set()



for _ in range(q-1):
    cmd, *args = list(map(int, input().split()))

    # print()
    # print(cmd, *args)
    # print("전")
    # print("belt_q", belt_q)
    # print("belt_s", belt_s)
    # print()

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
        if belt_dic[b_num-1]:
            print(-1)
        else:
            move_box(b_num)
            print(b_num)

    # print("후")
    # print("belt_q", belt_q)
    # print("belt_s", belt_s)