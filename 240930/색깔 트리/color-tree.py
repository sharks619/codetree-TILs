def addnodes(nodes_info_, abs_node_num, id_, p_id_, c_, dmax_):
    # 부모 노드의 깊이를 바로 가져오는 방식으로 중복 계산 최소화
    if p_id_ == -1:
        node_info_ = [abs_node_num, 1, id_, p_id_, c_, dmax_]
    else:
        parent_depth = next((depth for _, depth, node_id, _, _, _ in nodes_info_ if node_id == p_id_), 0)
        node_info_ = [abs_node_num, parent_depth + 1, id_, p_id_, c_, dmax_]

    nodes_info_.append(node_info_)
    return nodes_info_


def change_color(nodes_info_, id_child_id, pid_, color_):
    # 자식 노드 리스트에 대해 색상을 한 번에 변경
    for n, node_info in enumerate(nodes_info_):
        if node_info[2] in id_child_id[pid_]:
            nodes_info_[n][4] = color_  # 색상만 변경
    return nodes_info_


def calculate_dict_id_child_id(nodes_info_):
    id_child_id = {id_: set([id_]) for _, _, id_, _, _, _ in nodes_info_}

    for _, _, id_, pid_, _, _ in nodes_info_:
        if pid_ != -1:
            id_child_id[pid_].update(id_child_id[id_])

    return id_child_id


def calculate_dict_id_child_color(nodes_info_):
    id_child_color = {id_: set([color]) for _, _, id_, _, color, _ in nodes_info_}

    for _, _, id_, pid_, color, _ in nodes_info_:
        if pid_ != -1:
            id_child_color[pid_].update(id_child_color[id_])

    return id_child_color


def calculate_score(id_child_color):
    score = sum(len(colors) ** 2 for colors in id_child_color.values())
    return score


nodes_info = list()
q = int(input())

for x in range(q):
    cmds, *args = list(map(int, input().split()))

    if cmds == 100:
        p_id = args[1]
        nodes_info = addnodes(nodes_info, x, *args)

    elif cmds == 200:
        id_child_id = calculate_dict_id_child_id(nodes_info)
        nodes_info = change_color(nodes_info, id_child_id, *args)

    elif cmds == 300:
        color = next((c for _, _, id_, _, c, _ in nodes_info if id_ == args[0]), None)
        print(color)

    elif cmds == 400:
        id_child_color = calculate_dict_id_child_color(nodes_info)
        score = calculate_score(id_child_color)
        print(score)