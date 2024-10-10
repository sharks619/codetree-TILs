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

def check(id, score):
    c_colors = set([color_info[id]])
    for child in children[id]:
        child_colors, score = check(child, score)
        c_colors |= child_colors
    score += len(c_colors)**2
    return c_colors, score

def check_score():
    total_score = 0
    for r in root:
        _, score = check(r,0)
        total_score += score
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