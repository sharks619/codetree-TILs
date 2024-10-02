from collections import deque

l, q = map(int, input().split())

qeque = deque()
# 초밥을 담을 배열 추가
for _ in range(l):
    qeque.append(deque())

people_dict = {}
# 이전 시간 기록 ( 초밥 회전을 위해 ), 초밥 갯수
prev_time, cnt = 0, 0

for _ in range(q):
    cmd, *args = list(map(str, input().split()))
    t = int(args[0])
    # 시간만큼 초밥 회전하기
    qeque.rotate(t - prev_time)
    prev_time = t

    # 초밥 만들기
    if cmd == '100':
        x, name = args[1:]
        x = int(x)
        qeque[x].append(name)
        cnt += 1
    # 손님
    if cmd == '200':
        # 손님 추가하기
        x, name, n = args[1:]
        x = int(x)
        n = int(n)

        if x not in people_dict:
            people_dict[x] = [name, n]
        elif people_dict[x][0] == "":
            people_dict[x] = [name, n]
    # 초밥 먹기
    for i in range(l):
        sub_list = []
        while qeque[i]:
            now_name = qeque[i].popleft()

            # 사람이 있을 경우
            if i in people_dict and people_dict[i][0] == now_name:
                if people_dict[i][1] > 0:
                    people_dict[i][1] -= 1
                    cnt -= 1
                # 초기화
                if people_dict[i][1] == 0:
                    people_dict[i][0] = ""
            else:
                sub_list.append(now_name)
        # 먹지 못한 초밥 다시 넣어놓기
        for sub in sub_list:
            qeque[i].append(sub)

    # 사진 찍기
    if cmd == '300':
        people_cnt = 0

        for k, v in people_dict.items():
            if v[0] != "":
                people_cnt += 1

        print(people_cnt, cnt)