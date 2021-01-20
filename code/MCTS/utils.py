import pisqpipe as pp
import re
import numpy as np

width = pp.width
height = pp.height


def get_free_around(step, board):
    """获取所给位置的空闲8-neighbour

    Args:
        step: (x, y)
        board: game board, a matrix

    Returns:
        stepList: a list with (x, y)

    """
    x, y = step
    stepList = []
    for i in range(max(0, x - 1), min(width, x + 2)):
        for j in range(max(0, y - 1), min(height, y + 2)):
            if board[i][j] == 0:
                stepList.append((i, j))
    if step in stepList:
        stepList.remove(step)
    return stepList


def isFive(s):
    """判断所给数字字符串中是否有五连珠

    Args:
        s: a string like '011111000000'

    Returns:
        bool: True iff there is a 5-in-row

    """
    if len(re.findall('1{5}|2{5}', s)):
        return True
    else:
        return False


def isTerminate(board):
    """判断是否有五子连珠

    Args:
        board: a matrix, the game board

    Returns:
        bool, True iff there is at least a 5-in-row in the board

    """
    # 检查行
    for row in board:
        num2str = ''.join([str(i) for i in row])
        if isFive(num2str):
            return True

    # 检查列
    for j in range(width):
        num2str = ''.join([str(board[i][j]) for i in range(height)])
        if isFive(num2str):
            return True
    array = np.array(board)

    # 检查对角线/斜对角线
    for k in range(-width + 1, width):
        diag1 = np.diagonal(array, offset=k)
        # 斜对角线
        diag2 = np.diagonal(np.fliplr(array), offset=k)
        num2str = ''.join([str(x) for x in diag1])
        if isFive(num2str):
            return True
        num2str = ''.join([str(x) for x in diag2])
        if isFive(num2str):
            return True
    return False


# heuristic pattern
# 以下pattern中含有4567是因为后续程序中该位置上0可能会被更改，但该位置仍需要被标记为空位
# f1 : patterns, indicate that four-in-a-row is occurred in player1's side
f1_1 = '1111[04567]'
f1_2 = '[04567]1111'
# f2 : patterns, indicate that four-in-a-row is occurred in player2's side
f2_1 = '2222[04567]'
f2_2 = '[04567]2222'
# t1 : patterns, indicate that three-in-a-row is occurred in player1's side
t1_1 = '[04567]111[04567]'
t1_2 = '[04567]1112'
t1_3 = '2111[04567]'
# t2 : patterns, indicate that three-in-a-row is occurred in player2's side
t2_1 = '[04567]222[04567]'
t2_2 = '[04567]2221'
t2_3 = '1222[04567]'

# 经过替换的新heuristic pattern, 以便识别heuristic的存在及类型
# new_f1 : new patterns, indicate that a four-in-a-row is occurred in player1's side
new_f1_1 = '11114'
new_f1_2 = '41111'
# new_f2 : new patterns, indicate that a four-in-a-row is occurred in player2's side
new_f2_1 = '22225'
new_f2_2 = '52222'
# new_t1 : new patterns, indicate that a three-in-a-row is occurred in player1's side
new_t1_1 = '61116'
new_t1_2 = '61112'
new_t1_3 = '21116'
# new_t2 : new patterns, indicate that a three-in-a-row is occurred in player2's side
new_t2_1 = '72227'
new_t2_2 = '72221'
new_t2_3 = '12227'

# heuristic pattern 优先级
# 1 : four-in-a-row in my side
# 2 : four-in-a-row in opposite side
# 3 : three-in-a-row in my side
# 4 : three-in-a-row in opposite side

# 以下是list of pairs (pattern, new pattern), 不同player有不同顺序
# pair in pairs 出现的顺序意味着pattern替换的顺序，pattern优先级越高出现位置越靠后，因为可能存在覆盖现象
# player1, 2先换
pair1 = [(t2_1, new_t2_1), (t2_2, new_t2_2), (t2_3, new_t2_3), (t1_1, new_t1_1),
         (t1_2, new_t1_2), (t1_3, new_t1_3), (f2_1, new_f2_1), (f2_2, new_f2_2),
         (f1_1, new_f1_1), (f1_2, new_f1_2)]
# player2, 1先换
pair2 = [(t1_1, new_t1_1), (t1_2, new_t1_2), (t1_3, new_t1_3), (t2_1, new_t2_1),
         (t2_2, new_t2_2), (t2_3, new_t2_3), (f1_1, new_f1_1), (f1_2, new_f1_2),
         (f2_1, new_f2_1), (f2_2, new_f2_2)]


def color(s, player=1):
    """如果所给数字字符串中有heuristic pattern, 将它们替换为新pattern, 过程类似染色

    Args:
        s: a string like '011110222'
        player: current player

    Returns:
        a new string after substitution(coloring)

    """
    if player == 1:
        for pair in pair1:
            s = re.sub(pair[0], pair[1], s)
    elif player == 2:
        for pair in pair2:
            s = re.sub(pair[0], pair[1], s)
    return str(s)


def gen_heuristic(board, player=1):
    """对board 进行替换, 得到heuristic

    Args:
        player: current player
        board: current board state

    Returns:
        heuristic :[list_f1, list_f2, list_t1, list_t2]
            eg: list_f1 中元素为 four-in-a-row(1) 两侧的空闲位置(x, y)

    """
    b = np.array(board)
    heuristic = [[], [], [], []]  # 初始为空
    # [four1, four2, three1, three2]
    #    0      1      2       3       序号
    #    4      5      6       7       对应的0-替换(染色)

    # substitute process
    # 行替换
    for i in range(height):
        s = ''.join(map(str, b[i]))
        s = color(s, player)
        b[i] = list(map(int, list(s)))
    # 列替换
    for j in range(width):
        s = ''.join(map(str, b[:, j]))
        s = color(s, player)
        b[:, j] = list(map(int, list(s)))
    # 对角线/斜对角线替换
    for k in range(-width + 1, width):
        s = ''.join(map(str, np.diagonal(b, offset=k)))
        s = color(s, player)
        newDiag = list(map(int, list(s)))
        if k == 0:
            b[range(width), range(width)] = newDiag
        elif k > 0:
            b[range(width - k), range(k, width)] = newDiag
        else:
            b[range(-k, width), range(width + k)] = newDiag
        # 斜对角线
        s = ''.join(map(str, np.diagonal(np.fliplr(b), offset=k)))
        s = color(s, player)
        newDiag = list(map(int, list(s)))
        if k == 0:
            b[range(width), range(width - 1, -1, -1)] = newDiag
        elif k > 0:
            b[range(width - k), range(width - k - 1, -1, -1)] = newDiag  # 再仔细看看
        else:
            b[range(-k, width), range(width - 1, -k - 1, -1)] = newDiag

    # 产生heuristic
    for i in range(height):
        for j in range(width):
            if b[i, j] > 3:
                heuristic[b[i, j] - 4].append((i, j))
    return heuristic


"""
if __name__ == '__main__':
    a = [[0 for i in range(height)] for j in range(width)]
    a[1][3] = 2
    a[1][4] = 2
    a[1][5] = 2
    a[1][6] = 2
    a[1][7] = 1
    for i in range(4, 9):
        a[i][i] = 2
    print(a)
    b = gen_heuristic(a)
    print(b)
    print(isTerminate(a))
"""
