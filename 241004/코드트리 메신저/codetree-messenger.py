from collections import deque, defaultdict

n,q = map(int, input().split())

_, *args = list(map(int, input().split()))

dic_c_node = defaultdict(list) # 자식 노드
dic_p_node = defaultdict(int) # 부모 노드
dic_on_off = defaultdict(bool)
dic_power = defaultdict(int)

for i in range(n):
    p, a = args[i], args[i+n]
    dic_c_node[p].append(i+1)
    dic_p_node[i+1] = p
    dic_on_off[i+1] = True
    dic_power[i+1] = a

def count(c,l):
    total_cnt = 0

    q = deque([c])
    while q:
        c_node = q.popleft()
        # print("c_node:", c_node)

        for i in dic_c_node[c_node]:
            if dic_on_off[i] and dic_power[i]>l:
                # print("i:", i)
                q.append(i)
                total_cnt += 1
        l += 1

    return total_cnt

for _ in range(q-1):
    cmd, *args = list(map(int, input().split()))

    # print()
    # print(cmd, *args)
    # print()
    # 
    # print("변경전")
    # print("dic_c_node:", dic_c_node)
    # print("dic_p_node:", dic_p_node)
    # print("dic_on_off:", dic_on_off)
    # print("dic_power:", dic_power)


    if cmd==200:
        c = args[0]
        if dic_on_off[c]:
            dic_on_off[c] = False
        else:
            dic_on_off[c] = True

    elif cmd == 300:
        c, power = args[0], args[1]
        dic_power[c] = power

    elif cmd == 400:
        c1, c2 = args[0], args[1]
        c1p = dic_p_node[c1]
        c2p = dic_p_node[c2]

        dic_c_node[c1p].remove(c1)
        dic_c_node[c1p].append(c2)

        dic_c_node[c2p].remove(c2)
        dic_c_node[c2p].append(c1)

        dic_p_node[c1], dic_p_node[c2] = dic_p_node[c2], dic_p_node[c1]
        # dic_on_off[c1], dic_on_off[c2] = dic_on_off[c2], dic_on_off[c1]

    elif cmd == 500:
        c = args[0]
        print(count(c,0))
        # print("답:", count(c,0))

    # print("변경후")
    # print("dic_c_node:", dic_c_node)
    # print("dic_p_node:", dic_p_node)
    # print("dic_on_off:", dic_on_off)
    # print("dic_power:", dic_power)