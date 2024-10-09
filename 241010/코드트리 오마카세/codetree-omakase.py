from collections import defaultdict

class Query:
    def __init__(self, cmd, t, x, name, n):
        self.cmd = cmd
        self.t = t
        self.x = x
        self.name = name
        self.n = n

queries = [] # 명령들을 관리합니다.
names = set() # 등장한 사람 목록을 관리합니다.
p_queries = defaultdict(list) # 각 사람마다 주어진 초밥 명령만을 관리합니다.
entry_time = {} # 각 사람마다 입장 시간을 관리합니다.
position = {} # 각 손님의 위치를 관리합니다.
exit_time = {} # 각 사람마다 퇴장 시간을 관리합니다.

l, q = map(int, input().split())
for _ in range(q):
    command = input().split()
    cmd, t, x, n = -1, -1, -1, -1
    name = ""
    cmd = int(command[0])
    if cmd == 100:
        t, x, name = command[1:]
        t, x = map(int, [t, x])
    elif cmd == 200:
        t, x, name, n = command[1:]
        t, x, n = map(int, [t, x, n])
    else:
        t = int(command[1])

    queries.append(Query(cmd, t, x, name, n))

    if cmd == 100:
        p_queries[name].append(Query(cmd, t, x, name, n))

    elif cmd == 200:
        names.add(name)
        entry_time[name] = t
        position[name] = x

for name in names:
    exit_time[name] = 0

    for q in p_queries[name]:
        # 초밥 먼저 등장
        time_to_removed = 0
        if q.t < entry_time[name]:
            t_sushi_x = (q.x + (entry_time[name] - q.t)) % l
            a_time = (position[name] - t_sushi_x + l) % l

            time_to_removed = entry_time[name] + a_time
        # 사람 먼저 등장
        else:
            a_time = (position[name] - q.x + l) % l
            time_to_removed = q.t + a_time

        if exit_time[name] < time_to_removed:
            exit_time[name] = time_to_removed

        queries.append(Query(111, time_to_removed, -1, name, -1))

for name in names:
    queries.append(Query(222, exit_time[name], -1, name, -1))

queries.sort(key=lambda x: (x.t, x.cmd))

p_num, s_num = 0, 0
for i in range(len(queries)):
    if queries[i].cmd == 100:
        s_num += 1
    elif queries[i].cmd == 111:
        s_num -= 1
    elif queries[i].cmd == 200:
        p_num += 1
    elif queries[i].cmd == 222:
        p_num -= 1
    else:
        print(p_num, s_num)