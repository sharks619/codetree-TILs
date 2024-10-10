from collections import defaultdict

parent = defaultdict(int)
children = defaultdict(list)
color_info = defaultdict(int)
depth_info = defaultdict(int)
root = []

def color_change(id, c):
    color_info[id] = c

    for child in children[id]:
        color_info[child] = c
        color_change(child, c)

def check(id):
    stack = [(id, False)]  # (노드 ID, 방문 완료 여부)
    color_sets = defaultdict(set)  # 각 노드의 색상 집합
    score = 0

    while stack:
        node, visited = stack.pop()

        if visited:
            # 자식들을 모두 방문한 후, 해당 노드의 점수 계산
            color_sets[node].add(color_info[node])
            score += len(color_sets[node]) ** 2
            # 부모 노드에 색상 집합 합치기
            if parent[node] != 0:
                color_sets[parent[node]] |= color_sets[node]
        else:
            # 노드를 다시 스택에 넣고 자식들을 스택에 추가
            stack.append((node, True))
            for child in children[node]:
                stack.append((child, False))

    return score

def check_score():
    total_score = 0
    for r in root:
        total_score += check(r)
    print(total_score)


q = int(input())

for _ in range(q):
    cmd, *args = list(map(int, input().split()))

    if cmd == 100:
        m_id, p_id, color, max_depth = args
        if p_id == -1:
            root.append(m_id)

        if p_id != -1:
            parent_depth = depth_info[p_id]

            if parent_depth <= 1:
                continue

            if max_depth > parent_depth - 1:
                max_depth = parent_depth - 1

        parent[m_id] = p_id
        children[p_id].append(m_id)
        color_info[m_id] = color
        depth_info[m_id] = max_depth

    elif cmd == 200:
        m_id, color = args
        color_change(m_id, color)

    elif cmd == 300:
        m_id = args[0]
        print(color_info[m_id])

    elif cmd == 400:
        check_score()