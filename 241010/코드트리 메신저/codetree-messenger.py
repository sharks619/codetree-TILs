n,q = map(int, input().split())

_, *args = list(map(int, input().split()))

parents = [0] * (n + 1)
children = [[] for _ in range(n + 1)]
turn_on = [True] * (n + 1)
power = [0] * (n + 1)
authorities = [[0] * 21 for _ in range(n + 1)]

for i in range(n):
    parents[i + 1] = args[i]
    power[i + 1] = min(20, args[i + n])

for i in range(1, n + 1):
    children[parents[i]].append(i)

    p, idx = power[i], i
    while p >= 0:
        authorities[idx][p] += 1
        p -= 1
        if idx == parents[idx]: break
        idx = parents[idx]

def update(idx):
    authorities[idx] = [0] * 21
    if idx!=0:
        authorities[idx][power[idx]] += 1

    for child in children[idx]:
        if not turn_on[child]: continue
        for i, val in enumerate(authorities[child][1:]):
            authorities[idx][i] += val

    if idx != parents[idx]:
        update(parents[idx])

def power_change(idx, p):
    power[idx] = min(20, p)
    update(idx)

for _ in range(q-1):
    cmd, *args = list(map(int, input().split()))

    if cmd==200:
        c = args[0]
        turn_on[c] = False if turn_on[c] else True
        update(parents[c])

    elif cmd == 300:
        c, p = args[0], args[1]
        power_change(c, p)

    elif cmd == 400:
        c1, c2 = args[0], args[1]

        c1p = parents[c1]
        c2p = parents[c2]

        if c1p == c2p:
            continue

        parents[c1], parents[c2] = parents[c2], parents[c1]

        children[c1p].remove(c1)
        children[c1p].append(c2)

        children[c2p].remove(c2)
        children[c2p].append(c1)

        update(c1p)
        update(c2p)

    elif cmd == 500:
        c = args[0]
        print(sum(authorities[c])-1)