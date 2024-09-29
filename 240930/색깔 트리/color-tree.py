q = int(input())


def addnodes0(nodes_info_, abs_node_num, depth, id_, p_id_, c_, dmax_):

    node_info_ = [abs_node_num, depth, id_, p_id_, c_, dmax_]
    # print(node_info_)
    nodes_info_.append(node_info_)

    return nodes_info_

def addnodes(nodes_info_, abs_node_num, id_, p_id_, c_, dmax_):
    # if abs_node_num == 5:
        # print(id_, p_id_, c_, dmax_)

    tmp_p_id = p_id_
    stop = 0
    count = 0

    while (stop != 1 and tmp_p_id != -1):
        for _, depth, id, pid, _, dmax in nodes_info_:
            if id == tmp_p_id:
                count += 1
                if count == 1:
                    p_id_depth = depth

                # if abs_node_num == 5:
                        # print('0',tmp_p_id)
                if (p_id_depth+1) - depth < dmax:
                    tmp_p_id = pid
                    # if abs_node_num == 5:
                        # print('1',tmp_p_id)
                else:
                    stop = 1
                    # if abs_node_num == 5:
                        # print('2', tmp_p_id)
                break

    node_info_ = [abs_node_num, p_id_depth + 1, id_, p_id_, c_, dmax_]

    if tmp_p_id == -1:
        nodes_info_.append(node_info_)

    return nodes_info_

def change_color(nodes_info_, id_child_id, pid_, color_):
    for n, [abs_node_num, depth, id, pid, c, dmax] in enumerate(nodes_info_):
        if id in id_child_id[pid_]:
            nodes_info_[n] = [abs_node_num, depth, id, pid, color_, dmax]

    return nodes_info_

def search_color(nodes_info_, id_):
    for abs_node_num, depth, id, _, c, _ in nodes_info_:
        if id == id_:
            return c


def calculate_dict_id_child_id(nodes_info_):
    nodes_info_ = sorted(nodes_info_, reverse=True)
    for i, x in enumerate(zip(*nodes_info_)):
        if i == 2:
            node_list = list(x)
        elif i == 3:
            pid_list = list(x)
        elif i == 4:
            color_list = list(x)
            break

    id_child_id = dict()
    for id in node_list:
        id_child_id[id] = [id]

    # print('node_list:', node_list)
    # print('pid_list:', pid_list)
    # print('color_list:', color_list)
    # print('dmax_list:', dmax_list)

    for id, pid, color in zip(node_list, pid_list, color_list):
        if pid == -1:
            continue
        else:
            x = [j for j in id_child_id[pid]]
            # print(x)
            x.extend(id_child_id[id])
            # print(x)
            id_child_id[pid] = list(set(x))

    # print('id_child_id:', id_child_id)
    # print('id_child_color:', id_child_color)

    return id_child_id

def calculate_dict_id_child_color(nodes_info_):
    nodes_info_ = sorted(nodes_info_, reverse=True)
    for i, x in enumerate(zip(*nodes_info_)):
        if i == 2:
            node_list = list(x)
        elif i == 3:
            pid_list = list(x)
        elif i == 4:
            color_list = list(x)
            break


    id_child_color = dict()
    for id, color in zip(node_list, color_list):
        id_child_color[id] = [color]

    for id, pid, color in zip(node_list, pid_list, color_list):
        if pid == -1:
            continue
        else:
            x = [j for j in id_child_color[pid]]
            # print(x)
            x.extend(id_child_color[id])
            # print(x)
            id_child_color[pid] = list(set(x))

    # print('id_child_id:', id_child_id)
    # print('id_child_color:', id_child_color)

    return id_child_color

def calculate_score(id_child_color):
    score = 0
    for k, v in id_child_color.items():
        # print(k,v)
        score += len(v)**2

    return score


nodes_info = list()
for x in range(q):
    # print('iter: ', x+1)
    cmds, *args = list(map(int, input().split()))
    # print('nodes_info:', nodes_info)
    if cmds == 100:
        _, p_id, _, _ = [*args]
        if x > 0 and p_id != -1:
            nodes_info = addnodes(nodes_info, x, *args,)
        elif p_id == -1:
            nodes_info = addnodes0(nodes_info, x, 1, *args,)

    elif cmds == 200:
        id_child_id = calculate_dict_id_child_id(nodes_info)
        nodes_info = change_color(nodes_info, id_child_id, *args)

    elif cmds == 300:
        color = search_color(nodes_info, *args)
        print(color)

    elif cmds == 400:
        id_child_color = calculate_dict_id_child_color(nodes_info)
        score = calculate_score(id_child_color)
        print(score)


    # print(nodes_info)