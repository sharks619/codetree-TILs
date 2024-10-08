import heapq
from collections import defaultdict

q = int(input())

waiting_q = defaultdict(list)  # 채점 대기 큐에 있는 채점 task
waiting_q_cnt = 0  # 채점 대기 큐에 있는 채점 task 수
judging_dic = defaultdict(dict)

waiting_u_dic = defaultdict(bool)  # 채점 대기 큐에 있는 url
judging_d_dic = defaultdict(bool)  # 채점 진행 큐에 있는 domain
history_d_dic = defaultdict(dict)  # 채점 끝난 큐의 domain 처리 시작, 종료 시간 기록

_, n, u = list(map(str, input().split()))
n = int(n)
domain, id = u.split('/')
heapq.heappush(waiting_q[domain], (1, 0, u))  # p, t, url
waiting_u_dic[u] = True
waiting_j_q = list(range(1, n+1)) # 채점기
heapq.heapify(waiting_j_q)
waiting_q_cnt += 1

for _ in range(q-1):
    cmd, *args = list(map(str, input().split()))
    cmd = int(cmd)

    if cmd == 200:
        t, p, url = int(args[0]), int(args[1]), args[2]
        if not waiting_u_dic[url]:
            domain = url.split('/')[0]
            heapq.heappush(waiting_q[domain], (p, t, url))
            waiting_u_dic[url] = True
            waiting_q_cnt += 1

    elif cmd == 300:
        t = int(args[0])

        if not waiting_j_q: # 쉬고 있는 채점기가 없다면 무시
            continue

        temp_q = []

        for d, pq in waiting_q.items(): # domain, pq list
            if (not judging_d_dic[d]
                    and not (history_d_dic[d] and t < (history_d_dic[d][0]+3*(history_d_dic[d][1]-history_d_dic[d][0])))
                    and pq):
                heapq.heappush(temp_q, heapq.heappop(waiting_q[d]))

        if temp_q:
            cp, ct, cu = heapq.heappop(temp_q)
            jid = heapq.heappop(waiting_j_q)
            judging_dic[jid] = (t, cu)
            waiting_u_dic[cu] = False
            judging_d_dic[cu.split('/')[0]] = True
            waiting_q_cnt -= 1
            for tmp in temp_q:
                heapq.heappush(waiting_q[tmp[2].split('/')[0]], tmp)

        if not temp_q:
            waiting_q_cnt += len(temp_q)

    elif cmd == 400:
        t, j_id = int(args[0]), int(args[1])

        # 채점 중이던 작업이 없으면 무시
        if not judging_dic[j_id]:
            continue

        c_t, c_url = judging_dic[j_id]
        c_domain = c_url.split('/')[0]

        judging_dic[j_id] = False
        judging_d_dic[c_domain] = False

        heapq.heappush(waiting_j_q, j_id)
        history_d_dic[c_domain] = [c_t, t]

    elif cmd == 500:
        print(waiting_q_cnt)