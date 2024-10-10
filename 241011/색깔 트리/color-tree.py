from collections import defaultdict

parent = defaultdict(int)
children = defaultdict(list)
color_info = defaultdict(int)
depth_info = defaultdict(int)
root = []
color_sets = defaultdict(set)  # 각 노드의 서브트리 색상 집합 캐싱

def color_change(id, c):
    color_info[id] = c
    color_sets.clear()  # 색상 변경 시 캐시 초기화

    # 자식들의 색상도 변경
    stack = [id]
    while stack:
        node = stack.pop()
        color_info[node] = c
        for child in children[node]:
            stack.append(child)

def calculate_subtree_colors(node_id):
    stack = [node_id]
    visited = set()

    while stack:
        node = stack[-1]
        if node in visited:
            stack.pop()
            color_sets[node].add(color_info[node])
            for child in children[node]:
                color_sets[node] |= color_sets[child]
        else:
            visited.add(node)
            for child in children[node]:
                stack.append(child)

def check_score():
    # 모든 루트의 서브트리 색상 계산
    total_score = 0
    for r in root:
        calculate_subtree_colors(r)
        for node in color_sets:
            total_score += len(color_sets[node]) ** 2
    print(total_score)

# 입력 처리 및 명령 수행
q = int(input())
for _ in range(q):
    cmd, *args = list(map(int, input().split()))

    if cmd == 100:
        m_id, p_id, color, max_depth = args
        if p_id == -1:
            root.append(m_id)
        else:
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