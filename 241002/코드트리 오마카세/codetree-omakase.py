import heapq 
from collections import defaultdict

l, q = map(int,input().split())
# 전체 쿼리 저장 
query = []
# 사람 별 도착 시간 저장 
entry_time = {}
# 사람 별 위치 저장 
position = {}
# 사람 별 떠나는 시간 저장 
exit_time = defaultdict(int)
# 사람 이름 저장 
names = set()
# 사람 별 쿼리 저장 
p_queries = defaultdict(list)

for _ in range(q):
    data = list(map(str,input().split()))
    q_type = int(data[0])
    t, x, n = -1 ,-1 ,-1
    name = ""
    # 스시 들어옴 
    if q_type == 100 :
        # 들어온 시간, 위치, 사람 이름 
        t, x, name = data[1:]
        t = int(t)
        x = int(x)
    if q_type == 200 :
        # 들어온 시간, 위치, 사람 이름, 초밥 개수 
        t, x, name, n = data[1:]
        t = int(t)
        x = int(x)
        n = int(n)
    if q_type == 300 :
        # 사진 촬영 
        t = int(data[1])

    # t와 cmd 순서대로 
    # t가 같다면 초밥 만들고 -> 즉시 초밥 사라지고 -> 새로운 손님 입장하고 -> 손님 사라지고 -> 사진 촬영 순으로
    heapq.heappush(query, (t, q_type, x, name, n))

    if q_type == 100 :
        p_queries[name].append((t, q_type, x, name,n))
    if q_type == 200 :
        names.add(name)
        entry_time[name] = t 
        position[name] = x


for name in names :

    for t, cmd, x, p_n, n in p_queries[name]:
        #print(t, cmd, x, p_n, n, entry_time[name], position[name])
        # 초밥과 손님이 만나는 시간 
        match_time = 0 

        # 초밥이 사람이 오기 전에 주어짐 
        if t < entry_time[name]:
            t_diff = entry_time[name] - t 
            # 사람이 들어왔을 때 스시 위치 
            s_pos = (x + t_diff) % l
            match_time = entry_time[name]
            if position[name] > s_pos :
                add_time = position[name] - s_pos
                match_time += add_time
            elif s_pos > position[name]:
                add_time = l - (s_pos - position[name])
                match_time += add_time
        else :
            match_time = t
            if position[name] > x :
                add_time = position[name] - x
                match_time += add_time
            elif x > position[name]:
                add_time = l - (x - position[name])
                match_time += add_time
        
        # 초밥 먹는 가장 늦은 시간 갱신
        exit_time[name] = max(exit_time[name], match_time)

        # 초밥 사라지는 쿼리 추가 
        heapq.heappush(query, (match_time, 111, -1, name, -1))

# 사람 떠나는 쿼리 추가 
for name in names:
    heapq.heappush(query, (exit_time[name], 222, -1, name, -1))

p_num = 0
s_num = 0 

while query:
    data = heapq.heappop(query)
    cmd = data[1]

    if cmd == 100:
        s_num += 1 
    elif cmd == 111 :
        s_num -=1 
    elif cmd == 200:
        p_num += 1 
    elif cmd == 222 :
        p_num -= 1 
    else :
        print(p_num, s_num)