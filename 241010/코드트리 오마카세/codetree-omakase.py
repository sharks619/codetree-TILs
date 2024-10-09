from collections import defaultdict

l, q = map(int, input().split())
ccount, scount = 0, 0  # customer, sushi count
customer = defaultdict(list)
# name: [t, p, 남은 할당량] 저장
sushi = defaultdict(dict)
# name: {t: p, t: p} 저장

# t초에 x위치에 앉은 손님이 먹을 수 있는 초밥: t-1초에 x-1위치의 초밥... t초~미래에는 x위치의 초밥 놓여지면 바로
commands = []
# 모든 명령 바로바로 실행하지 말고,
# 초밥이 손님 온 뒤로 언제 먹혀지는지부터 알아낸 다음에, 명령 실행하며 명령 시점 비교하는 게 낫다
for _ in range(q):
    command, t, *detail = input().split()
    if command == '100':  # 초밥 = name: {t: p, t: p} 저장
        x, name = detail
        t, x = int(t), int(x)
        sushi[name][t] = x
    elif command == '200':  # 손님 = name: [t, p, 남은 할당량] 저장
        x, name, n = detail
        t, x, n = int(t), int(x), int(n)
        customer[name].append(t)
        customer[name].append(x)
    else:
        t = int(t)
    commands.append((command, t))

# 손님 = name: [t, p, 남은 할당량] 저장
for name, val in customer.items():
    ct, cp = val
    exit_time = 0  # 손님이 exit하는 time은, 초밥이 들어온 st 순서대로가 아닌, 최종적으로 먹히게 되는 ft를 고려해야 함
    for st in sushi[name]:
        if st <= ct:  # 초밥 놓은 다음 사람 옴
            np = (sushi[name][st] + (ct - st)) % l  # ct일 때, 초밥의 위치
            # np -> cp 가려면 기다려야 하는 시간
            wait = (cp - np) % l
            # 회전하며 최종적으로 먹히는 시간
            ft = wait + ct
        else:  # 사람 온 다음에 초밥 놓음
            np = sushi[name][st]
            # sushi[name][st] -> cp 가려면 기다려야 하는 시간
            wait = (cp - sushi[name][st]) % l
            # 회전하며 최종적으로 먹히는 시간
            ft = wait + st
        commands.append(("111", ft ))  # ft에 del sushi[name][st] 초밥 제거
        exit_time = max(exit_time, ft)

    commands.append(("222", exit_time))  # 가장 마지막 ft에 손님 제거

commands.sort(key=lambda x: (x[1], x[0]))  # 먹고 초밥/손님 제거하는 명령 추가했기 때문에, 시간 순, 명령번호 순 정렬
for c, t in commands:
    if c == '100':
        scount += 1
    elif c == '111':  # 초밥 제거
        scount -= 1
    elif c == '200':
        ccount += 1
    elif c == '222':  # 손님 제거
        ccount -= 1
    else:
        print(ccount, scount)