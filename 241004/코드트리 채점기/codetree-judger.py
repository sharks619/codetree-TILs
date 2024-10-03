import heapq
from collections import defaultdict
q = int(input())

waiting_q = []
waiting_c = 0
judging_dic = defaultdict()

waiting_u_set = set()  # URL을 빠르게 조회하기 위해 집합 사용
judging_d_set = set()  # Domain을 빠르게 조회하기 위해 집합 사용
history_d_dic = {}  # Domain의 처리 시작/종료 시간을 기록

_, n, u = list(map(str, input().split()))
n = int(n)
domain, id = u.split('/')
heapq.heappush(waiting_q, (1, 0, u))
waiting_u_set.add(u)
waiting_j_q = list(range(1, n + 1))
heapq.heapify(waiting_j_q)
waiting_c += 1


for _ in range(q-1):
    cmd, *args = list(map(str, input().split()))
    cmd = int(cmd)
    # print("cmd, *args:", cmd, *args)
    # print('작업전')
    # print("waiting_q:", waiting_q)
    # print("judging_dic:", judging_dic)
    # print("history_d_dic:", history_d_dic)

    if cmd == 200:
        t, p, url = int(args[0]), int(args[1]), args[2]

        if url not in waiting_u_set:
            heapq.heappush(waiting_q, (p, t, url))
            waiting_u_set.add(url)
            waiting_c += 1

    elif cmd == 300:
        t = int(args[0])

        if not waiting_j_q: # 쉬고 있는 채점기가 없다면 무시
            continue

        cp, ct, cu = heapq.heappop(waiting_q)
        waiting_c -= 1
        c_domain, c_id = cu.split('/')

        if c_domain in judging_d_set:
            heapq.heappush(waiting_q, (cp, ct, cu))
            waiting_c += 1
            continue
        if c_domain in history_d_dic.keys():
            s, e = history_d_dic[c_domain]
            if t < s + 3*(e-s):
                heapq.heappush(waiting_q, (cp, ct, cu))
                waiting_c += 1
                continue
            else:
                jid = heapq.heappop(waiting_j_q)
                judging_dic[jid] = (t, cu)
                waiting_u_set.remove(cu)
                judging_d_set.add(c_domain)

        else:
            jid = heapq.heappop(waiting_j_q)
            judging_dic[jid] = (t, cu)
            waiting_u_set.remove(cu)
            judging_d_set.add(c_domain)

    elif cmd == 400:
        t, j_id = int(args[0]), int(args[1])

        # J_id 번 채점기가 진행하던 채점이 없으면 무시
        if j_id not in judging_dic:
            continue

        # 진행 중이던 채점이 있었다면 해당 작업을 마무리
        c_t, c_url = judging_dic[j_id]
        c_domain = c_url.split('/')[0]

        del judging_dic[j_id]
        judging_d_set.remove(c_domain)

        heapq.heappush(waiting_j_q, j_id)
        history_d_dic[c_domain] = [c_t, t]

    elif cmd == 500:
        print(waiting_c)

    # print('작업후')
    # print("waiting_q:", waiting_q)
    # print("judging_dic:", judging_dic)
    # print("history_d_dic:", history_d_dic)