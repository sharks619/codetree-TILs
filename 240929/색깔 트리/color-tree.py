from collections import defaultdict

MAX_COLOR = 5
ADD_NODE = 100
CHANGE_COLOR = 200
RETRIEVE_COLOR = 300
RETRIEVE_SCORE = 400
PARENT = 1

class Node:
    def __init__(self, node_id, color=0, max_depth=0, parent=-1):
        self.node_id = node_id
        self.color = color
        self.max_depth = max_depth
        self.parent = parent
        self.children = []

nodes = {}
check_root = defaultdict(int)

# Create the root node with infinite depth
nodes[0] = Node(0, color=0, max_depth=float('inf'), parent=-1)

def check_make_child(cur_node, depth):
    if cur_node.node_id == 0:
        return True
    if cur_node.max_depth <= depth:
        return False
    return check_make_child(nodes[cur_node.parent], depth + 1)

def add_node(m_id, p_id, color, max_depth):
    if p_id == -1:
        check_root[m_id] = PARENT
    if check_root[m_id] == PARENT or (p_id in nodes and check_make_child(nodes[p_id], 1)):
        nodes[m_id] = Node(m_id, color, max_depth, 0 if check_root[m_id] == PARENT else p_id)
        if check_root[m_id] != PARENT:
            nodes[p_id].children.append(m_id)

def dfs(node_id, color):
    nodes[node_id].color = color
    for child_id in nodes[node_id].children:
        dfs(child_id, color)

def change_color(m_id, color):
    dfs(m_id, color)

def retrieve_color(m_id):
    print(nodes[m_id].color)

def calculate(cur_node, color_count):
    temp_color_count = [0] * (MAX_COLOR + 1)
    temp_color_count[cur_node.color] = 1

    sum_score = 0
    for child_id in cur_node.children:
        child = nodes[child_id]
        child_color_count = [0] * (MAX_COLOR + 1)
        score = calculate(child, child_color_count)

        for i in range(1, MAX_COLOR + 1):
            temp_color_count[i] += child_color_count[i]

        sum_score += score

    count = sum(1 for i in range(1, MAX_COLOR + 1) if temp_color_count[i])
    sum_score += count ** 2

    for i in range(1, MAX_COLOR + 1):
        color_count[i] += temp_color_count[i]

    return sum_score

def get_score():
    total_score = 0
    color_count = [0] * (MAX_COLOR + 1)
    for node_id, root_check in check_root.items():
        if root_check == PARENT:
            total_score += calculate(nodes[node_id], color_count)
    return total_score

def retrieve_score():
    print(get_score())

# Process the input and generate outputs
output_data = []
Q = int(input())

for _ in range(Q):
    cmds = list(map(int, input().split()))
    command = cmds[0]

    if command == ADD_NODE:
        m_id, p_id, color, max_depth = cmds[1:]
        add_node(m_id, p_id, color, max_depth)

    elif command == CHANGE_COLOR:
        m_id, color = cmds[1:]
        change_color(m_id, color)

    elif command == RETRIEVE_COLOR:
        m_id = cmds[1]
        retrieve_color(m_id)

    elif command == RETRIEVE_SCORE:
        retrieve_score()