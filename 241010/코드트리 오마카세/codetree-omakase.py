import heapq
from collections import defaultdict


cmds = [] # 명령
names = set() # 사람 이름
food_info = defaultdict(list) # {음식 이름: [시간, 위치]}
entry_time = {} # {사람 : 입장 시간}
position = {} # {사람 : 위치}
exit_time = {} # {사람 : 퇴장 시간}


l, q = map(int, input().split())

for _ in range(q):
    cmd, *args = input().split()
    cmd = int(cmd)

    if cmd == 100:
        t, x, name = args
        t, x = map(int, [t, x])
        food_info[name].append((t, x))
        heapq.heappush(cmds, (t, cmd))

    elif cmd == 200:
        t, x, name, n = args
        t, x, n = map(int, [t, x, n])
        names.add(name)
        entry_time[name] = t
        position[name] = x
        heapq.heappush(cmds, (t, cmd))

    else:
        t = int(args[0])
        heapq.heappush(cmds, (t, cmd))


for name in names:
    exit_time[name] = 0

    for ft, fx in food_info[name]: # time, position
        # 초밥 먼저 등장
        time_to_removed = 0
        if ft < entry_time[name]:
            t_sushi_x = (fx + (entry_time[name] - ft)) % l
            a_time = (position[name] - t_sushi_x + l) % l

            time_to_removed = entry_time[name] + a_time
        # 사람 먼저 등장
        else:
            a_time = (position[name] - fx + l) % l
            time_to_removed = ft + a_time

        if exit_time[name] < time_to_removed:
            exit_time[name] = time_to_removed

        heapq.heappush(cmds,(time_to_removed, 111))

for name in names:
    heapq.heappush(cmds,(exit_time[name], 222))

p_num, s_num = 0, 0
while cmds:
    _, cmd = heapq.heappop(cmds)
    if cmd == 100:
        s_num += 1
    elif cmd == 111:
        s_num -= 1
    elif cmd == 200:
        p_num += 1
    elif cmd == 222:
        p_num -= 1
    else:
        print(p_num, s_num)