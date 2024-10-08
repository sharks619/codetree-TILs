import sys
import heapq
from collections import defaultdict

input = sys.stdin.readline()
q = int(input())

waiting_q = [] # 채점 대기 큐에 있는 채점 task
waiting_q_cnt = 0 # 채점 대기 큐에 있는 채점 task 수
judging_dic = defaultdict()

waiting_u_dic = defaultdict(bool)  # 채점 대기 큐에 있는 url
judging_d_dic = defaultdict(bool)  # 채점 진행 큐에 있는 domain
history_d_dic = {}  # 채점 끝난 큐의 domain 처리 시작, 종료 시간 기록

_, n, u = list(map(str, input().split()))
n = int(n)
domain, id = u.split('/')
heapq.heappush(waiting_q, (1, 0, u))  # p, t, url
waiting_u_dic[u] = True
waiting_j_q = list(range(1, n+1)) # 채점기
heapq.heapify(waiting_j_q)
waiting_q_cnt += 1


for _ in range(q-1):
    cmd, *args = list(map(str, input().split()))
    cmd = int(cmd)
    # print()
    # print("cmd, *args:", cmd, *args)
    # print('작업전')
    # print("waiting_q:", waiting_q)
    # print("waiting_q_cnt:", waiting_q_cnt)
    # print("waiting_u_set:", waiting_u_set)
    # print()
    # print("judging_d_set:", judging_d_set)
    # print("judging_dic:", judging_dic)
    # print()
    # print("history_d_dic:", history_d_dic)
    # print()
    if cmd == 200:
        t, p, url = int(args[0]), int(args[1]), args[2]

        if not waiting_u_dic[url]:
            heapq.heappush(waiting_q, (p, t, url))
            waiting_u_dic[url] = True
            waiting_q_cnt += 1

    elif cmd == 300:
        t = int(args[0])

        if not waiting_j_q: # 쉬고 있는 채점기가 없다면 무시
            continue

        temp_q = []

        while waiting_q:
            cp, ct, cu = heapq.heappop(waiting_q)
            c_domain, c_id = cu.split('/')

            if judging_d_dic[c_domain]:
                temp_q.append((cp, ct, cu))
            elif (c_domain in history_d_dic) and (t < history_d_dic[c_domain][0] + 3 * (history_d_dic[c_domain][1] - history_d_dic[c_domain][0])):
                temp_q.append((cp, ct, cu))
            else:
                jid = heapq.heappop(waiting_j_q)
                judging_dic[jid] = (t, cu)
                del waiting_u_dic[cu]
                judging_d_dic[c_domain] = True
                waiting_q_cnt -= 1
                break
        for item in temp_q:
            heapq.heappush(waiting_q, item)

        if not temp_q:
            waiting_q_cnt += len(temp_q)

    elif cmd == 400:
        t, j_id = int(args[0]), int(args[1])

        # 채점 중이던 작업이 없으면 무시
        if j_id not in judging_dic:
            continue

        c_t, c_url = judging_dic[j_id]
        c_domain = c_url.split('/')[0]

        del judging_dic[j_id]
        del judging_d_dic[c_domain]

        heapq.heappush(waiting_j_q, j_id)
        history_d_dic[c_domain] = [c_t, t]

    elif cmd == 500:
        print(waiting_q_cnt)

    # print('작업후')
    # print("waiting_q:", waiting_q)
    # print("waiting_q_cnt:", waiting_q_cnt)
    # print("waiting_u_set:", waiting_u_set)
    # print()
    # print("judging_d_set:", judging_d_set)
    # print("judging_dic:", judging_dic)
    # print()
    # print("history_d_dic:", history_d_dic)
    # print()