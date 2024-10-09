import bisect

L, Q = [int(x) for x in input().split()]
cmds = []

class Sushi:
    def __init__(self, t, x, name):
        self.t = t
        self.x = x
        self.name = name

sushies_info = dict()
sushies_n = 0
customers_n = 0
eat = []
go = []

for q in range(Q):
    line = [x for x in input().split()]
    cmds.append(line)
    if int(line[0]) == 100:
        t, x, name = [int(line[1]), int(line[2]), line[3]]
        sushi = Sushi(t, x, name)
        if name in sushies_info:
            sushies_info[name].append(sushi)
        else:
            sushies_info[name] = [sushi]


for q in range(Q):
    line = cmds[q]
    cmd = int(line[0])

    if cmd == 100:
        sushies_n += 1

    elif cmd == 200:
        t, x, name, n = [int(line[1]), int(line[2]), line[3], int(line[4])]
        customers_n += 1
        max_time = -1

        for sushi in sushies_info[name]:
            if sushi.t <= t:
                time = t + (sushi.t - t + x - sushi.x) % L
            else:
                time = sushi.t + (x - sushi.x) % L
            eat.append(time)
            if max_time < time:
                max_time = time

        eat.sort()
        go.append(max_time)
        go.sort()

    elif cmd == 300:
        t = int(line[1])

        idx = bisect.bisect_right(eat, t)
        # print("aaa:", sushies_n, idx)
        sushies_left = sushies_n - idx

        idx = bisect.bisect_right(go, t)
        customers_n = len(go) - idx

        print(customers_n, sushies_left)
    # print(sushies_n, customers_n, go, eat)