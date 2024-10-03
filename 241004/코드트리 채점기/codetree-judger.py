import heapq
from collections import defaultdict

INF = float('inf')

# 입력 수
q = int(input())

# 대기 중인 작업 수
waiting_tasks_count = 0
# 도메인별 대기 작업 관리
waiting_tasks = defaultdict(list)
# 각 도메인의 채점 상태 (True: 채점 중, False: 대기 중)
is_domain_in_judging = defaultdict(bool)
# 각 도메인의 마지막 작업이 끝난 시간
domain_last_end_time = defaultdict(int)
# 이미 대기 중인 URL 집합
waiting_urls = set()

# 첫 번째 명령 처리 (채점기 수 및 첫 작업)
_, grader_count, first_url = list(map(str, input().split()))
grader_count = int(grader_count)
first_domain = first_url.split('/')[0]

# 채점기 상태 관리 (쉬고 있는 채점기들)
graders = [(-1, -1) for _ in range(grader_count)]
available_graders = list(range(grader_count))
heapq.heapify(available_graders)

# 첫 작업을 대기 큐에 추가
heapq.heappush(waiting_tasks[first_domain], (1, 0, first_url))
waiting_urls.add(first_url)
waiting_tasks_count += 1

# 명령 처리 루프
for _ in range(q - 1):
    cmd, *args = list(map(str, input().split()))
    cmd = int(cmd)

    if cmd == 200:
        # 새로운 작업 추가
        submit_time, priority, url = int(args[0]), int(args[1]), args[2]
        domain = url.split('/')[0]

        if url in waiting_urls:
            continue
        waiting_urls.add(url)
        heapq.heappush(waiting_tasks[domain], (priority, submit_time, url))
        waiting_tasks_count += 1

    elif cmd == 300:
        # 채점기 배정
        current_time = int(args[0])

        if not available_graders or not waiting_tasks_count:
            continue

        best_domain = ''
        best_priority = (INF, INF)
        best_url = ''

        # 도메인별로 대기 중인 작업을 확인하여 채점 가능한 작업 찾기
        for domain in waiting_tasks:
            # 해당 도메인이 이미 채점 중이거나, 마지막 작업이 끝난 시간이 현재보다 크면 무시
            if is_domain_in_judging[domain] or domain_last_end_time[domain] > current_time or not waiting_tasks[domain]:
                continue

            # 대기 중인 작업 확인
            task_priority, task_time, task_url = waiting_tasks[domain][0]

            # 더 높은 우선순위 작업 선택
            if best_priority <= (task_priority, task_time):
                continue

            best_domain = domain
            best_priority = (task_priority, task_time)
            best_url = task_url

        # 채점 가능한 작업이 있는 경우
        if best_priority < (INF, INF):
            # 사용할 수 있는 채점기 배정
            grader_idx = heapq.heappop(available_graders)
            is_domain_in_judging[best_domain] = True
            graders[grader_idx] = (current_time, best_domain)
            
            # 대기 작업 큐에서 제거
            heapq.heappop(waiting_tasks[best_domain])
            waiting_urls.remove(best_url)
            waiting_tasks_count -= 1

    elif cmd == 400:
        # 작업 완료 처리
        complete_time = int(args[0])
        grader_idx = int(args[1]) - 1

        if graders[grader_idx] == (-1, -1):
            continue

        start_time, domain = graders[grader_idx]
        graders[grader_idx] = (-1, -1)
        is_domain_in_judging[domain] = False
        domain_last_end_time[domain] = start_time + (complete_time - start_time) * 3

        # 채점기 다시 사용 가능 상태로 추가
        heapq.heappush(available_graders, grader_idx)

    elif cmd == 500:
        # 대기 중인 작업 수 출력
        print(waiting_tasks_count)