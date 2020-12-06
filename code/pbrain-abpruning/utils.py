import pisqpipe as pp
import random

# interface part
pp.infotext = 'name="pbrain-abpruning", author="Jeansix", version="1.0",country="Chine"'

MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = -1  # do tiny changes, 2 for original
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_turn():
    if pp.terminateAI:
        return
    i = 0
    while True:
        x = random.randint(0, pp.width)
        y = random.randint(0, pp.height)
        i += 1
        if pp.terminateAI:
            return
        if isFree(x, y):
            break
    if i > 1:
        pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
    pp.do_mymove(x, y)


def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


# scores for certain patterns
FiveInRow = [1, 1, 1, 1, 1]
LiveFour = [[0, 1, 1, 1, 1], [1, 1, 1, 1, 0]]
DeadFour = [[-1, 1, 1, 1, 1], [1, 1, 1, 1, -1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1]]
LiveThree = [[0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [1, 0, 1, 1, 0], [1, 1, 0, 1, 0], [0, 1, 1, 0, 1]]
DeadThree = [[-1, 1, 1, 1, 0], [0, 1, 1, 1, -1], [-1, 1, 1, 0, 1], [1, 0, 1, 1, -1], [1, 0, 0, 1, 1], [1, 1, 0, 0, 1]]
LiveTwo = [[0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0]]
DeadTwo = [[-1, 1, 1, 0, 0], [0, 0, 1, 1, -1], [0, 0, -1, 1, 1], [1, 1, -1, 0, 0], [0, -1, 1, 1, 0], [0, 1, 1, -1, 0],
           [-1, 1, 0, 1, 0], [0, 1, 0, 1, -1], [0, -1, 1, 0, 1], [1, 0, 1, -1, 0]]

stoneShapes = [FiveInRow, LiveFour, DeadFour, LiveThree, DeadThree, LiveTwo, DeadTwo]
scoreDict = {'FiveInRow': 1e6, 'LiveFour': 1e5, 'DeadFour': 1e4, 'LiveThree': 1e3, 'DeadThree': 1e2, 'LiveTwo': 1e1,
             'DeadTwo': 1}
classDict = {0: 'FiveInRow', 1: 'LiveFour', 2: 'DeadFour', 3: 'LiveThree', 4: 'DeadThree', 5: 'LiveTwo',
             6: 'DeadTwo'}


def get_all_around(pos):
    """Get all positions around the given pos.

    Args:
        pos:current position

    Returns:
        list of around positions

    """
    x, y = pos
    return [(nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1]]


def get_board_state(board):
    row = pp.width
    col = pp.height
    isStart = True
    my_stones = set()
    opp_stones = set()
    for i in range(row):
        for j in range(col):
            # my stone
            if board[i][j] == 1:
                my_stones.add((i, j))
                isStart = False
            elif board[i][j] == -1:
                opp_stones.add((i, j))
                isStart = False
    if isStart is True:
        return None
    else:
        my_len = len(my_stones)
        opp_len = len(opp_stones)
        if my_len == opp_len:
            playing = 0
        else:
            playing = 1
        stones = [opp_stones, my_stones]
        state = (stones, playing)
        return state
