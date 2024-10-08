import sys
import heapq
from collections import OrderedDict, defaultdict
from typing import Optional

class Task:
    def __init__(self, t, p, url):
        self.domain = url.split("/")[0]
        self.id = url.split("/")[1]
        self.p = p
        self.t = t

    def __lt__(self, other):
        if self.p != other.p:
            return self.p < other.p
        return self.t < other.t

# 채점기 정보 {J_id: Task}
J_dict = OrderedDict()
# 대기 큐 Priority Queue (Task) dict
domain_wait_q = defaultdict(list)
# 대기 큐 안에 있는 url dict {url: T/F}
wait_q_url_dict = defaultdict(bool)
# 도메인 시간 정보 {domain: {start: int, end: int}}
domain_time_dict = defaultdict(dict)
# 현재 채점 중인 도메인 리스트 {domain: T/F}
domain_judging_dict = defaultdict(bool)

def set_j(input_data):
    """
    Step 1
    input_data: [N, u0]
    채점기 세팅
    u0 wait Q에 넣기
    """
    N = int(input_data[0])
    u = input_data[1]
    for i in range(1, N + 1):
        J_dict[i] = None
    heapq.heappush(domain_wait_q[u.split("/")[0]], Task(0, 1, u))
    wait_q_url_dict[u] = True

def insert_task_wait_q(input_data):
    """
    step 2
    input_data = [t, p ,u]
    waitQ에 새로운 task 넣기
    """
    t, p = map(int, input_data[:2])
    u = input_data[2]
    if not wait_q_url_dict[u]:
        heapq.heappush(domain_wait_q[u.split("/")[0]], Task(t, p, u))
        wait_q_url_dict[u] = True

def pop_task_wait_q(t) -> Optional[Task]:
    task_tmp_list = []

    for domain, pq in domain_wait_q.items():
        if not domain_judging_dict[domain] and domain_wait_q[domain]:
            curr_domain_time = domain_time_dict.get(domain, {"start": 0, "gap": 0})
            if curr_domain_time["start"] + 3 * curr_domain_time["gap"] <= t:
                heapq.heappush(task_tmp_list, heapq.heappop(domain_wait_q[domain]))

    if task_tmp_list:
        task = heapq.heappop(task_tmp_list)
        for tmp in task_tmp_list:
            heapq.heappush(domain_wait_q[tmp.domain], tmp)
        return task
    else:
        return None

def try_task(input_data):
    """
    step 3
    input_data = [t]
    """
    t = int(input_data[0])

    j_id = None
    for i, v in J_dict.items():
        if v is None:
            j_id = i
            break

    if j_id is not None:
        task: Optional[Task] = pop_task_wait_q(t)
        if task is not None:
            J_dict[j_id] = task
            domain_judging_dict[task.domain] = True
            domain_time_dict[task.domain]["start"] = t
            wait_q_url_dict[f"{task.domain}/{task.id}"] = False

def end_task(input_data):
    """
    step 4
    input_data = [t J_id]
    """
    t, j_id = map(int, input_data)
    if J_dict[j_id] is not None:
        task = J_dict[j_id]
        J_dict[j_id] = None
        domain_judging_dict[task.domain] = False
        domain_time_dict[task.domain]["gap"] = t - domain_time_dict[task.domain]["start"]

def print_wait_q():
    """
    step5
    """
    answer = 0
    for v in domain_wait_q.values():
        answer += len(v)
    print(answer)

Q = int(sys.stdin.readline())
for _ in range(Q):
    query, *data = sys.stdin.readline().split()

    # 100 N u0
    if int(query) == 100:
        set_j(data)

    # 200 t p u
    elif int(query) == 200:
        insert_task_wait_q(data)

    # 300 t
    elif int(query) == 300:
        try_task(data)

    # 400 t J_id
    elif int(query) == 400:
        end_task(data)

    else:
        # 500 t
        print_wait_q()